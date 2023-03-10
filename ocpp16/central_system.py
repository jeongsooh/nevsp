import logging
from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from cardinfo.models import Cardinfo
from evcharger.models import Evcharger
from variables.models import Variables
from clients.models import Clients
from charginginfo.models import Charginginfo
from charginginfo.kepco_tariff import calculate_price
from evuser.models import Evuser

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('ocpp')

global Job_List

def ocpp_request(ocpp_req):
    unique_id = None  
    cpnumber = ocpp_req['cpnumber']
    if ocpp_req['msg_name'] == 'Authorize':
        logging.info('===== Got an Authorize Req =====')
        id_tag = ocpp_req['msg_content']['idTag']

        queryset = Cardinfo.objects.filter(cardtag=id_tag).values()
        if queryset.count==0:
            status = 'Invalid'
        else:
            if queryset[0]['cardstatus'] == '배포됨':
                status = 'Accepted'
                Clients.objects.filter(cpnumber=cpnumber).update(authorized_tag=id_tag)
            else:
                status = queryset[0]['cardstatus']
                print('cardinfo: %s' % queryset[0]['cardstatus'])
        ocpp_conf = [3,ocpp_req['connection_id'],
        {
            "idTagInfo" :{
                'parentIdTag':id_tag,'status':status
            }
        }]
        return ocpp_conf
    elif ocpp_req['msg_name'] == 'BootNotification':
        logging.info('===== Got a Boot Notification =====')
        cpnumber = ocpp_req['cpnumber']

        queryset = Evcharger.objects.filter(cpnumber=cpnumber).values()
        if queryset.count==0:
            status = "Rejected"
        else :
            status = "Accepted"

        queryset = Variables.objects.filter(group='group0').values()
        if queryset.count==0:
            interval =480
        else:
            interval = queryset[0]['interval']

        ocpp_conf = [3,ocpp_req['connection_id'],
            {
                'currentTime' : datetime.now().strftime('%Y-%m-%dT%H:%M:%S')+"Z",
                'interval' : interval,
                'status' : status
            }
        ]
        return ocpp_conf

    elif ocpp_req['msg_name'] == 'Heartbeat':
        logging.info('===== Got a Heartbeat =====')
        cpnumber = ocpp_req['cpnumber']

        queryset = Evcharger.objects.filter(cpnumber =cpnumber).values()
        if queryset.count() ==0:
            status = 'Rejected'
        else:
            status = 'Accepted'
        
        ocpp_conf = [3,ocpp_req['connection_id'],
            {
                'currentTime' : datetime.now().strftime('%Y-%m-%dT%H:%M:%S') +'Z',
            }
        ]
        return ocpp_conf
    elif ocpp_req['msg_name'] == 'StatusNotification':
        logging.info('===== Got a StatusNotification Req =====')
        cpnumber = ocpp_req['cpnumber']
        queryset = Evcharger.objects.filter(cpnumber=cpnumber).values()
        if queryset.count() ==0:
            print('Ocpp Message Error : Cp is not available')
        else:
            if ocpp_req['msg_content']['connectorId'] ==0:
                Evcharger.objects.filter(cpnumber=cpnumber).update(connector_id_0_status=ocpp_req['msg_content']['status'])
            if ocpp_req['msg_content']['connectorId'] ==1:
                Evcharger.objects.filter(cpnumber=cpnumber).update(connector_id_1_status=ocpp_req['msg_content']['status'])
                if ocpp_req['msg_content']['status'] == 'Faulted':
                    Evcharger.objects.filter(cpnumber=cpnumber).update(cpstatus=ocpp_req['msg_content']['errorCode'])
            else :
                pass

        ocpp_conf = [3,ocpp_req['connection_id'],{}]
        return ocpp_conf

    elif ocpp_req['msg_name'] == 'DataTransfer':
        logging.info('===== Got a DataTransfer =====')
        if ocpp_req['msg_content']['messageId'] == "uvStartCardRegMode":
            targetcp = ocpp_req['msg_content']['data']['targetcp']
            queryset = Clients.objects.filter(cpnumber=targetcp).values()
            Clients.objects.filter(cpnumber=ocpp_req['cpnumber']).update(connection_id=ocpp_req['connection_id'])
            channel_name = queryset[0]['channel_name']
            message = [2,ocpp_req['connection_id'],ocpp_req['msg_name'],ocpp_req['msg_content']]
            print('OCPP Conf in central_system : Send To {} : {}'.format(targetcp,message))
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.send)(channel_name,{
                "type" : "ocpp16_message",
                "message" : message
            })

        elif ocpp_req['msg_content']['messageId'] == "uvCardRegStatus":
            if ocpp_req['msg_content']['data']['status'] == "CardAuthMode":
                ocpp_conf = [3, ocpp_req['connection_id'],
                {
                    "status":"Accepted"
                }
            ]
            return ocpp_conf
        elif ocpp_req['msg_content']['messageId'] == "uvCardReg":
            print('Cardtag = ' , ocpp_req['msg_content'])
            Cardinfo.objects.filter(userid=ocpp_req['msg_content']['data']['memberId'], cardstatus="처리중").update(cardtag=ocpp_req['msg_content']['data']['token'], cardstatus='배포됨')
            ocpp_conf = [3, ocpp_req['connection_id'],
            {
                "status" : "Accepted"
            }
            ]        
            return ocpp_conf

    elif ocpp_req['msg_name'] == 'DiagnosticsStatusNotification':
        logging.info('===== Got a Diagnostics Status Notification =====')
        return call_result.DiagnosticsStatusNotification()

    elif ocpp_req['msg_name'] == 'FirmwareStatusNotification':
        logging.info('===== Got a Firmware Status Notification =====')
        return call_result.FirmwareStatusNotification()

    elif ocpp_req['msg_name'] == 'MeterValues':
        logging.info('===== Got a MeterValue Req =====')
        ocpp_conf = [3,ocpp_req['connection_id'],{}]
        return ocpp_conf

    elif ocpp_req['msg_name'] == 'StartTransaction':
        logging.info('===== Got a StartTransaction Req =====')

        queryset = Cardinfo.objects.filter(cardtag=ocpp_req['msg_content']['idTag']).values()
        charginginfo = Charginginfo(
            cpnumber = cpnumber,
            userid = queryset[0]['userid'],
            energy = ocpp_req['msg_content']['meterStart'],
            amount = 0,
            start_dttm = datetime.strptime(ocpp_req['msg_content']['timestamp'],'%Y-%m-%dT%H:%M:%SZ'),
            end_dttm = datetime.strptime(ocpp_req['msg_content']['timestamp'],'%Y-%m-%dT%H:%M:%SZ'),
        )
        charginginfo.save()
        
        Evuser.objects.filter(userid=queryset[0]['userid']).update(last_use_dttm = datetime.now())
        ocpp_conf = [3,ocpp_req['connection_id'],
            {
                "transactionId" : 1,
                "idTagIngo" : {'parentIdTag' : ocpp_req['msg_content']['idTag'],
                    'status' : 'Accepted'}
            }
        ]
        return ocpp_conf

        
    elif ocpp_req['msg_name'] == 'StopTransaction':
        logging.info('========== Got a StopTransaction Req ==========')
        queryset = Cardinfo.objects.filter(cardtag = ocpp_req['msg_content']['idTag']).values()
        userid = queryset[0]['userid']
        charginginfo = Charginginfo.objects.filter(cpnumber=cpnumber,userid=userid).values().last()
        print("charginginfo :" , charginginfo)
        energy = ocpp_req['msg_content']['meterStop'] - charginginfo['energy']
        end_dttm = ocpp_req['msg_content']['timestamp']    
        start_dttm = charginginfo.get('start_dttm')
        print('startdttm : ',type(start_dttm) , start_dttm)
        print('enddttm :', type(end_dttm) , end_dttm)
        energy_kw = energy/1000
        usage_amount ,base_amount = calculate_price(start_dttm,end_dttm,energy_kw)
        amount = usage_amount + base_amount
        print('energy : {}, amount : {}, end_dttm: {}'.format(energy,amount,end_dttm))

        end_time = datetime.strptime(end_dttm, '%Y-%m-%dT%H:%M:%SZ')

        Charginginfo.objects.filter(id=charginginfo['id']).update(energy=energy,amount=amount,end_dttm=end_time)

        ocpp_conf = [3,ocpp_req['connection_id'],
            {
                'idTagInfo' : {'parentIdTag' : ocpp_req['msg_content']['idTag'],
                    'status' : 'Accepted'}
            }
        ]
        return ocpp_conf

    else:
        pass

def ocpp_conf_from_cp(cpnumber, ocpp_conf):
    queryset = Clients.objects.filter(cpnumber=cpnumber).values()
    if ocpp_conf['connection_id'] == queryset[0]['connection_id']:
        ocpp_conf['msg_name'] = queryset[0]['channel_status']

    if ocpp_conf['msg_name'] == 'Reset':
        print("===================================")
        print("Reset is accepted")
        print("===================================")

    elif ocpp_conf['msg_name'] == 'ChangeAvailability':
        print("===================================")
        print("ChangeAvilability is accecpted")
        print("===================================")
        
    elif ocpp_conf['msg_name'] == 'ChangeConfiguration':
        print("===================================")
        print("ChangeConfiguration is accpeted")
        print("===================================")

    elif ocpp_conf['msg_name'] == 'ClearCache':
        print("===================================")
        print("ClearCache is accepted")
        print("===================================")

    elif ocpp_conf['msg_name'] == 'DataTransfer':
        print("===================================")
        print("DataTransfer is accepted")
        print("===================================")

    elif ocpp_conf['msg_name'] == 'GetConfiguration':
        print("===================================")
        print("GetConfiguration is accepted")
        print("===================================")

    elif ocpp_conf['msg_name'] == 'RemoteStartTransaction':
        if ocpp_conf['msg_content']['status'] == 'Accepted':
            print("===================================")
            print("RemoteStartTransaction is accepted")
            print("===================================")
        else:
            print("===================================")
            print("UpdateFirmware is {}".format(ocpp_conf['msg_content']['status']))
            print("===================================")
    
    elif ocpp_conf['msg_name'] == 'RemoteStopTransaction':
        if ocpp_conf['msg_content']['status'] == 'Accepted':
            print("===================================")
            print("RemoteStopTransaction is accepted")
            print("===================================")
        else:
            print("===================================")
            print("UpdateFirmware is {}".format(ocpp_conf['msg_content']['status']))
            print("===================================")

    elif ocpp_conf['msg_name'] == 'TriggerMessage':
        print("===================================")
        print("TriggerMessage is accepted")
        print("===================================")

    elif ocpp_conf['msg_name'] == 'GetDiagnostics':
        print("===================================")
        print("GetDiagnostics is accepted")
        print("===================================")

    elif ocpp_conf['msg_name'] == 'UpdateFirmware':
        print("===================================")
        print("UpdateFirmware is accepted")
        print("===================================")

    elif ocpp_conf['msg_name'] == 'UnlockConnector':
        if ocpp_conf['msg_content']['status'] == 'Accepted':
            print("===================================")
            print("UpdateFirmware is accepted")
            print("===================================")
        else:
            print("===================================")
            print("UpdateFirmware is {}".format(ocpp_conf['msg_content']['status']))
            print("===================================")

    else:
        print("{} message is confirmed".format(ocpp_conf['msg_name']))



