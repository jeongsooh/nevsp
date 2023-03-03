from django import forms
from django.contrib.auth.hashers import check_password
from .models import Evuser
import re 
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm



class LoginForm(forms.Form):
    userid = forms.CharField(
        error_messages={'required' : '아이디를 입력하세요'},max_length=64 ,label='아이디')
    password = forms.CharField(
        error_messages={'required' : '비밀번호를 입력하세요'},widget=forms.PasswordInput,label='비밀번호')
    
    def clean(self):
        cleaned_data =  super().clean()
        userid = cleaned_data.get('userid')
        password = cleaned_data.get('password')

        if userid and password:
            try :
                evuser = Evuser.objects.get(userid=userid)
            except Evuser.DoesNotExist:
                self.add_error('userid' ,'아이디가 존재하지 않습니다')
                return
            if not check_password(password,evuser.password):
                self.add_error('password','패스워드가 일치하지않습니다')
            else : 
                self.user_id = evuser.userid
                
                

class RegisterForm(forms.ModelForm):
    userid = forms.CharField(error_messages={'required' : '아이디를 입력하세요'},max_length=64, label='아이디')
    password = forms.CharField(error_messages={'required' : '비밀번호를 입력하세요'},widget=forms.PasswordInput, max_length=128,label='비밀번호')
    password1 = forms.CharField(error_messages={'required' : '비밀번호를 입력하세요'},widget=forms.PasswordInput,max_length=128, label='비밀번호 확인')
    name = forms.CharField(error_messages={'required' : '이름을 입력하세요'},max_length=64,label='이름')
    email = forms.EmailField(error_messages={'required' : '이메일을 입력하세요'},max_length=128,label='이메일')
    phone = forms.CharField(error_messages={'required' : '핸드폰 번호를 입력하세요'},max_length=64,label='핸드폰번호')
    postcode = forms.CharField(max_length=64,label='우편번호')
    jibunAddress = forms.CharField(max_length=400,label='지번주소', required=False,widget=forms.TextInput(attrs={'readonly':'readonly'}))
    roadAddress = forms.CharField(max_length=400,label='도로명주소',required=False)
    detailaddress = forms.CharField(max_length=400,label='상세주소')
    extraaddress = forms.CharField(max_length=400,label='참고항목',required=False)
    
    class Meta:
        model = Evuser
        fields = ['userid','password','password1','name','email','phone','postcode','roadAddress','jibunAddress','detailaddress','extraaddress']
        def __init__(self, *args,**kwargs):
            super(RegisterForm,self).__init__(*args,**kwargs)
            self.fields['jibunAddress'].widget.attrs.update({
                'readonly' : 'True',
            })
            self.fields['roadAddress'].widget.attrs.update({
                'readonly' : 'True',
            })
            self.fields['extraaddress'].widget.attrs.update({
                'readonly' : 'True',
            })

    def clean(self):
        cleaned_data = super().clean()
        userid = cleaned_data.get('userid')
        password = cleaned_data.get('password')
        password1 = cleaned_data.get('password1')
        phone = cleaned_data.get('phone')
        if userid and password:
            userid_regex = re.compile("^[A-Za-z0-9]+$")
            user_vaildation = userid_regex.search(userid)
            if user_vaildation == None:
                self.add_error('userid','아이디는 영어 대소문자와 숫자만 가능합니다.')
            phone_regex = re.compile("\d{2,3}[- ]?\d{3,4}[- ]?\d{4}")
            phone_vaildation = phone_regex.search(phone)
            if phone_vaildation ==None:
                self.add_error('phone','핸드폰번호를 정확하게 입력해주세요')
            if password != password1:
                self.add_error('password','비밀번호가 서로 다릅니다')
                self.add_error('password1','비밀번호가 서로 다릅니다')
            if len(password) < 8:
                self.add_error('password','비밀번호는 8글자 이상입니다.')
                self.add_error('password1','비밀번호는 8글자 이상입니다.')
            try : 
                Evuser.objects.get(userid=userid)
                self.add_error('userid','이미 가입된 아이디입니다.')
            except:
                pass
            
class passwordChangeForm(forms.Form):
    pass

class EvuserupdateForm(forms.ModelForm):
    
    
    class Meta:
        model = Evuser
        fields = ['userid','name','email','phone','category','status','level','postcode','roadAddress' ,'jibunAddress','detailaddress','extraaddress']
        
    def __init__(self,*args,**kwargs):
        super(EvuserupdateForm,self).__init__(*args,**kwargs)
        self.fields['userid'].widget.attrs.update({
            'readonly' : 'True',
        })
        self.fields['name'].widget.attrs.update({
            'readonly' : 'True',
        })
        self.fields['postcode'].required = False
        self.fields['postcode'].widget.attrs.update({
            'readonly' : 'True',
        })
        self.fields['jibunAddress'].required = False
        self.fields['jibunAddress'].widget.attrs.update({
            'readonly' : 'True',
        })
        self.fields['extraaddress'].required = False
        self.fields['extraaddress'].widget.attrs.update({
            'readonly' : 'True',
        })
        self.fields['roadAddress'].widget.attrs.update({
            'readonly' : 'True',
        })

class RecoveryIdForm(forms.Form):
    name = forms.CharField(error_messages={'required' : '이름을 입력해주세요'},max_length=64,label='이름')
    email = forms.EmailField(error_messages={'required' : '이메일을 입력해주세요'},max_length=128,label='이메일')

    class Meta:
        fields = ['name','email']

    def __init__(self,*args,**kwargs):
        super(RecoveryIdForm,self).__init__(*args,**kwargs)
        self.fields['name'].widget.attrs.update({
            'class' : 'form-control',
            'id' : 'form_name',
        })
        self.fields['email'].widget.attrs.update({
            'class' : 'form-control',
            'id' : 'form_email'
        })

class EvuserDeleteForm(forms.Form):
    pass