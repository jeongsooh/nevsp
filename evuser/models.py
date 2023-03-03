from django.db import models

# Create your models here.

class Evuser(models.Model):
    userid = models.CharField(max_length=64,verbose_name='회원아이디')
    password = models.CharField(max_length=128,verbose_name='비밀번호')
    name = models.CharField(max_length=64,verbose_name='회원이름')
    email = models.EmailField(max_length=128,verbose_name='이메일')
    phone = models.CharField(max_length=128,verbose_name='전화번호')
    category = models.CharField(max_length=64,choices=[('일반','일반'),('법인','법인'),('기타','기타')],default='일반',verbose_name='회원구분')
    status = models.CharField(max_length=64,choices=[('정상','정상'),('해지','해지'),('유예','유예')],default='정상',verbose_name='회원상태')
    level = models.CharField(max_length=16,choices=[('admin','admin'),('user','user'),('Engineer','Engineer')],verbose_name='등급',default='user')
    register_dttm = models.DateTimeField(auto_now_add=True,verbose_name='등록시간')
    last_use_dttm = models.DateTimeField(auto_now_add=False,null=True,verbose_name='최근사용시간')
    postcode = models.CharField(max_length=64,verbose_name='우편번호')
    jibunAddress = models.CharField(max_length=400,verbose_name='지번주소')
    roadAddress = models.CharField(max_length=400,verbose_name='도로명주소')
    detailaddress = models.CharField(max_length=400,verbose_name='상세주소')
    extraaddress = models.CharField(max_length=400,verbose_name='참고항목')

    def __str__(self):
        return self.userid

    class Meta:
        db_table='nevsp_evuser'
        verbose_name ='회원'
        verbose_name_plural = '회원목록'