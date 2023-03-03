from django import forms
from clients.models import Clients

class ClientsCheckForm(forms.Form):
  cpnumber = forms.CharField(
    error_messages={
      'required': '충전기번호를 입력하세요.'
    },
    max_length=64, label='충전기번호'
  )

  def clean(self):
    cleaned_data = super().clean()
    cpnumber = cleaned_data.get('cpnumber')

    if cpnumber:
      try:
        clients = Clients.objects.get(cpnumber=cpnumber)
      except Clients.DoesNotExist:
        self.add_error('cpnumber', '충전기번호가 없는 번호입니다.')
        return

      self.cpnumber = clients.id

class ClientsTagCheckForm(forms.Form):
    cpnumber = forms.CharField(error_messages={'required': '충전기번호를 입력하세요.'},max_length=64, label='충전기번호')
    authorized_tag = forms.CharField(error_messages={'required' : '카드태그를 입력하세요'},max_length=64, label='카드태그')

    def clean(self):
        cleaned_data = super().clean()
        cpnumber = cleaned_data.get('cpnumber')
        if cpnumber:
            try:
                clients = Clients.objects.get(cpnumber=cpnumber)
            except Clients.DoesNotExist:
                self.add_error('cpnumber', '충전기번호가 없는 번호입니다.')
                return

        self.cpnumber = clients.id

class ClientsDeleteForm(forms.Form):
  pass