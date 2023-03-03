from django import forms
from .models import Evcharger


class EvchargerUpdateForm(forms.ModelForm):
    class Meta:
        model = Evcharger  # Specify the model here
        fields = ['cpnumber', 'cpname', 'cpstatus', 'partner_id','cpversion' ,'postcode','roadAddress' ,'jibunAddress','detailaddress','extraaddress']
    def __init__(self,*args,**kwargs):
        super(EvchargerUpdateForm,self).__init__(*args,**kwargs)
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

class EvchargerCreateForm(forms.ModelForm):
    class Meta:
        model = Evcharger
        fields = ['cpnumber','cpname','postcode','roadAddress' ,'jibunAddress','detailaddress','extraaddress']

    def __init__(self,*args,**kwargs):
        super(EvchargerCreateForm,self).__init__(*args,**kwargs)
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

    def clean(self):
        
        cleaned_data =  super().clean()
        cpnumber = cleaned_data.get('cpnumber')
        cpname = cleaned_data.get('cpname')

        if cpnumber and cpname:
            try :
                evcharger_cpnumber = Evcharger.objects.get(cpnumber=cpnumber)
                self.add_error('cpnumber','이미 등록된 충전기번호입니다.')
            except:
                pass
            try:
                evcharger_cpname = Evcharger.objects.get(cpname=cpname)
                self.add_error('cpname','이미 등록된 충전기이름입니다.')
            except:
                pass

class EvchargerDeleteForm(forms.Form):
    pass