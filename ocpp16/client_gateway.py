
import uuid
from datetime import datetime

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from clients.models import Clients


def get_cardtag(cpnumber,userid):
    response_timeout =10
    vendorId = "gresystem"
    messageId = "uvStartCardRegMode"
    msg = {
        "memberId" : userid,
        "targetcp" : cpnumber
    }
    ocpp_req = {
        "msg_direction" : 2,
        "connection_id" : str(uuid.uuid4()),
        "msg_name" : "DataTransfer",
        "msg_content" : {'vendorId':vendorId,'messageId' :messageId,'data':msg},
    }

    message = [2,ocpp_req['connection_id'],ocpp_req['msg_name'],ocpp_req['msg_content']]
    print('data transfer req: ' , message)
    queryset = Clients.objects.filter(cpnumber=cpnumber).values()
    channel_name = queryset[0]['channel_name']

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(
        channel_name,
        {
            'type' : 'ocpp16_message',
            'message' : message
        }
    )

def reset_evcharger(cpnumber):
    ocpp_req = {
        "msg_direction" : 2,
        "connection_id" : '',
        "msg_name" : "Reset",
        "msg_content" : {},
    }
    ocpp_request_to_cp(cpnumber,ocpp_req)

def update_evcharger(cpnumber):
    ocpp_req = {
        "msg_direction" : 2,
        "connection_id" : '',
        "msg_name" : "UpdateFirmware",
        "msg_content" : {},
    }
    ocpp_request_to_cp(cpnumber,ocpp_req)

def clearcache_evcharger(cpnumber):
    ocpp_req = {
        "msg_direction" : 2,
        "connection_id" : "",
        "msg_name": "ClearCache",
        "msg_content": {},
    }
    ocpp_request_to_cp(cpnumber, ocpp_req)

def remotestart_evcharger(cpnumber,idTag):
    ocpp_req = {
        "msg_direction": 2,
        "connection_id": "",
        "msg_name": "RemoteStartTransaction",
        "msg_content": {'idTag' : idTag},
    }
    ocpp_request_to_cp(cpnumber, ocpp_req)

def remotestop_evcharger(cpnumber):
    ocpp_req = {
        "msg_direction" : 2,
        "connection_id" : "",
        "msg_name": "RemoteStopTransaction",
        "msg_content": {},
    }
    ocpp_request_to_cp(cpnumber, ocpp_req)

def unlock_connector(cpnumber):
    ocpp_req = {
        "msg_direction" : 2,
        "connection_id" : "",
        "msg_name": "UnlockConnector",
        "msg_content": {},
    }
    ocpp_request_to_cp(cpnumber, ocpp_req)

def get_conf(cpnumber):
    ocpp_req = {
        "msg_direction" : 2,
        "connection_id" : "",
        "msg_name": "GetConfiguration",
        "msg_content": {},
    }
    ocpp_request_to_cp(cpnumber, ocpp_req)

def set_conf(cpnumber):
    ocpp_req = {
        "msg_direction" : 2,
        "connection_id" : "",
        "msg_name": "ChangeConfiguration",
        "msg_content": {},
    }
    ocpp_request_to_cp(cpnumber, ocpp_req)

def send_request(cpnumber, message):
    print('Ocpp Mesaage : Send to {} : {}' .format(cpnumber ,message))
    queryset = Clients.objects.filter(cpnumber=cpnumber).values()
    channel_name = queryset[0]['channel_name']
    channel_layer=get_channel_layer()
    async_to_sync(channel_layer.send)(
        channel_name,
        {
            'type' : 'ocpp16_message',
            'message' : message
        }
    )

    

def connectionid_logging(cpnumber, connection_id, msg_name):
    queryset = Clients.objects.filter(cpnumber=cpnumber).values()

    if queryset.count()==0:
        client = Clients(
            cpnumber=cpnumber,
            connection_id=connection_id,
            channel_status=msg_name
        )
        client.save()
        print('connection_id saved successfully')

    else:
        if not (queryset[0]['connection_id'] == connection_id):
            Clients.objects.filter(cpnumber=cpnumber).update(connection_id=connection_id, channel_status=msg_name)
            print('connection_id updated successfully')

def ocpp_request_to_cp(cpnumber,ocpp_req):
    global Job_List

    ocpp_req['msg_direction'] = 2
    ocpp_req['connection_id'] = str(uuid.uuid4())

    if ocpp_req['msg_name'] == 'Reset':
        ocpp_req['msg_content'] = {
            'type':'Soft',
        }
        message = [ocpp_req['msg_direction'], ocpp_req['connection_id'], ocpp_req['msg_name'], ocpp_req['msg_content']]
        send_request(cpnumber, message)
        connectionid_logging(cpnumber, ocpp_req['connection_id'], ocpp_req['msg_name'])

    elif ocpp_req['msg_name'] == 'UpdateFirmware':
        ocpp_req['msg_content']={
            'location' : 'http://127.0.0.1:8000/SW_FileDownload/skb_firmware_v1.1.6.bin',
            'retrieveDate' : datetime.now().strftime("%Y-%m-%dT%H:%M:%S")+"Z",
            'retries' : 1,
            'retryInterval' : 1
        }
        message = [ocpp_req['msg_direction'], ocpp_req['connection_id'], ocpp_req['msg_name'], ocpp_req['msg_content']]
        send_request(cpnumber, message)
        connectionid_logging(cpnumber, ocpp_req['connection_id'], ocpp_req['msg_name'])
    
    elif ocpp_req['msg_name'] == 'ClearCache':
        ocpp_req['msg_content'] = {}
        message = [ocpp_req['msg_direction'], ocpp_req['connection_id'], ocpp_req['msg_name'], ocpp_req['msg_content']]
        send_request(cpnumber, message)
        connectionid_logging(cpnumber, ocpp_req['connection_id'], ocpp_req['msg_name'])
    
    elif ocpp_req['msg_name'] == 'RemoteStartTransaction':
        ocpp_req['msg_content'] ={
            'idTag' : ocpp_req['msg_content']['idTag']
        }
        message = [ocpp_req['msg_direction'], ocpp_req['connection_id'], ocpp_req['msg_name'], ocpp_req['msg_content']]
        send_request(cpnumber, message)
        connectionid_logging(cpnumber, ocpp_req['connection_id'], ocpp_req['msg_name'])

    elif ocpp_req['msg_name'] == 'RemoteStopTransaction':
        ocpp_req['msg_content'] ={
            'transactionId' : 1
        }
        message = [ocpp_req['msg_direction'], ocpp_req['connection_id'], ocpp_req['msg_name'], ocpp_req['msg_content']]
        send_request(cpnumber, message)
        connectionid_logging(cpnumber, ocpp_req['connection_id'], ocpp_req['msg_name'])
    
    elif ocpp_req['msg_name'] == 'UnlockConnector':
        ocpp_req['msg_content'] = {
            'connectorId' : 1
        }
        message = [ocpp_req['msg_direction'], ocpp_req['connection_id'], ocpp_req['msg_name'], ocpp_req['msg_content']]
        send_request(cpnumber, message)
        connectionid_logging(cpnumber, ocpp_req['connection_id'], ocpp_req['msg_name'])
    
    elif ocpp_req['msg_name'] == 'GetConfiguration':
        ocpp_req['msog_content'] = {
            'key':['MeterValueSampleInterval','ClockAlignedDataInterval']
        }
        message = [ocpp_req['msg_direction'], ocpp_req['connection_id'], ocpp_req['msg_name'], ocpp_req['msg_content']]
        send_request(cpnumber, message)
        connectionid_logging(cpnumber, ocpp_req['connection_id'], ocpp_req['msg_name'])
    elif ocpp_req['msg_name'] == 'ChanegeConfiguration':
        ocpp_req['msg_content'] = {
            'key' : 'MeterValueSampleInterval',
            'value' : 0,
            # 'key': 'ClockAlignedDataInterval',
            # 'value': 300
        }
        message = [ocpp_req['msg_direction'], ocpp_req['connection_id'], ocpp_req['msg_name'], ocpp_req['msg_content']]
        send_request(cpnumber, message)
        connectionid_logging(cpnumber, ocpp_req['connection_id'], ocpp_req['msg_name'])
    else:
        pass

