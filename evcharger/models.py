from django.db import models

# Create your models here.

class Evcharger(models.Model):
    cpname = models.CharField(max_length=64,verbose_name='충전기이름')
    cpnumber = models.CharField(max_length=64, verbose_name='충전기번호')
    partner_id = models.CharField(max_length=128,verbose_name='파트너아이디')
    mainuser_id = models.CharField(max_length=128, verbose_name='사용자아이디')
    public_use = models.BooleanField(default=True , verbose_name='공용')
    cpstatus = models.CharField(max_length=64,verbose_name='충전기상태',default='충전대기')
    connector_id_0 = models.CharField(max_length=64,verbose_name='0번커넥터아이디')
    connector_id_0_status = models.CharField(max_length=64,verbose_name='0번커넥터상태')
    connector_id_1 = models.CharField(max_length=64,verbose_name='1번커넥터아이디')
    connector_id_1_status = models.CharField(max_length=64,verbose_name='1번커넥터상태')
    manager_id = models.CharField(max_length=128,verbose_name='관리자아이디')
    cpversion = models.CharField(max_length=64, verbose_name='충전기버전')
    register_dttm = models.DateTimeField(auto_now_add=True,verbose_name='등록일시')
    last_modified_dttm = models.DateTimeField(auto_now_add=True,verbose_name='최종변경일시')
    fw_version= models.CharField(max_length=64,verbose_name='펌웨어버전')
    postcode = models.CharField(max_length=64,verbose_name='우편번호')
    jibunAddress = models.CharField(max_length=400,verbose_name='지번주소')
    roadAddress = models.CharField(max_length=400,verbose_name='도로명주소')
    detailaddress = models.CharField(max_length=400,verbose_name='상세주소')
    extraaddress = models.CharField(max_length=400,verbose_name='참고항목')
    engineer = models.CharField(max_length=128,verbose_name='엔지니어' ,blank=True)
# 충전기에 group이 있어야되는게 아닌지 vender 도 zipcode
    def __str__(self):
        return self.cpname

    class Meta:
        db_table = 'nevsp_evcharger'
        verbose_name = '충전기'
        verbose_name_plural = '충전기'