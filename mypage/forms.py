
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.contrib.auth.hashers import check_password
from evuser.models import Evuser
from evcharger.models import Evcharger

from django.contrib.auth.forms import SetPasswordForm

class mypageupdateForm(forms.ModelForm):
    class Meta:
        model = Evuser
        fields = ['email','phone','postcode','roadAddress' ,'jibunAddress','detailaddress','extraaddress']
    def __init__(self, *args,**kwargs):
        super(mypageupdateForm,self).__init__(*args,**kwargs)
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
class passwordChangeForm(forms.Form):
    pass

class mypageCardCreateForm(forms.Form):
    cardname = forms.CharField(max_length=64,label='카드이름')
    cpnumber = forms.CharField(max_length=64,label='충전기번호')
    def clean(self):
        cleaned_data =  super().clean()
        cardname = cleaned_data.get('cardname')
        cpnumber = cleaned_data.get('cpnumber')

        if cardname and cpnumber:
            try:
                evcharger = Evcharger.objects.get(cpnumber=cpnumber)
            except Evcharger.DoesNotExist:
                self.add_error('cpnumber','충전기 번호가 잘못되었습니다.')

        # self.cpnumber = evcharger.id
        self.cardname = cardname

class mypageCardManualForm(forms.Form):
    cardname = forms.CharField(max_length=64,label='카드이름')
    cardnum1 = forms.CharField(max_length=4)
    cardnum2 = forms.CharField(max_length=4)
    cardnum3 = forms.CharField(max_length=4)
    cardnum4 = forms.CharField(max_length=4)
    def clean(self):
        cleaned_data =  super().clean()
        cardname = cleaned_data.get('cardname')
        cardnum1 = cleaned_data.get('cardnum1')
        cardnum2 = cleaned_data.get('cardnum2')
        cardnum3 = cleaned_data.get('cardnum3')
        cardnum4 = cleaned_data.get('cardnum4')


class mypageCardreEditForm(forms.Form):
    cpnumber = forms.CharField(max_length=64,label='충전기번호')
    def clean(self):
        return super().clean()

class mypageCardEditForm(forms.Form):
    newcardname = forms.CharField(max_length=16,label='카드이름')
    def clean(self):
        return super().clean()

class mypageCardDeleteForm(forms.Form):
    pass

class mypageUserDeleteForm(forms.Form):
    pass
