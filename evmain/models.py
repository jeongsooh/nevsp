from django.db import models

# Create your models here.


class Evmain(models.Model):
    regiCount = models.IntegerField(verbose_name='금일 가입자')
    regiTotal = models.IntegerField(verbose_name='누적 가입자')
    useCharger = models.IntegerField(verbose_name='사용중인 충전기')
    totalCharger = models.IntegerField(verbose_name='총 충전기')
    totalenergy = models.CharField(max_length=128, verbose_name='금일 누적 충전량')
    totalamount = models.CharField(max_length=128, null=True ,default=0 , verbose_name='금일 충전금액')
    eventcurrent = models.CharField(max_length=128,verbose_name='진행중인 이벤트 현황')
    systemday = models.DateTimeField(auto_now_add=False,null=True,verbose_name='당일날짜')

    class Meta:
        db_table = 'nevsp_evmain'
        verbose_name = '메인화면'
        verbose_name_plural = '메인'