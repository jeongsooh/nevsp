from django import forms

from evmain.models import Evmain
from datetime import datetime,date,timedelta
from evcharger.models import Evcharger
from charginginfo.models import Charginginfo
from evuser.models import Evuser


def EvmainCreate():
    startday = datetime.combine(date.today(),datetime.min.time()) -timedelta(days=1)
    endday = startday+timedelta(days=1)-timedelta(seconds=1)
    today = datetime.now()-timedelta(days=1)
    if Evmain.objects.filter(systemday__range=(startday,endday)).count() ==0:
        energy = Charginginfo.objects.filter(start_dttm__range=(startday,endday))
        totalenergy=0  
        totalamount=0
        for a in range(energy.count()):
            totalenergy += energy.values()[a]['energy']
            totalamount += energy.values()[a]['amount']

        evmain = Evmain(
            regiCount = Evuser.objects.filter(register_dttm__range=(startday,endday)).count(),
            regiTotal = Evuser.objects.all().count(),
            useCharger = Evcharger.objects.filter(cpstatus='사용중').count(),
            totalCharger = Evcharger.objects.all().count(),
            systemday = today.date(),
            totalenergy = totalenergy,
            totalamount = totalamount
        )
        evmain.save() 
    else :
        Evmain.objects.filter(systemday=today.date()).update(useCharger = Evcharger.objects.filter(cpstatus='사용중').count())

class EvmainDeleteForm(forms.Form):
    pass