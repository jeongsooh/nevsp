from django.db import models

# Create your models here.


class Mypage(models.Model):
    cpnumber = models.CharField(max_length=64,verbose_name='충전기번호')
    userid = models.CharField(max_length=64, verbose_name='회원아이디')
    energy = models.IntegerField(verbose_name='충전량')
    amount = models.IntegerField(verbose_name='충전금액')
    start_dttm = models.DateTimeField(null=True,verbose_name='충전시작일시')
    end_dttm = models.DateTimeField(null=True,verbose_name='충전완료일시')

    class Meta:
        db_table = 'nevsp_mypage'
        verbose_name = '충전정보'
        verbose_name_plural = '충전정보'
