from django.urls import path
from .views import *
app_name = 'clients'

urlpatterns = [
    path('',ClientsList.as_view()),
    path('<int:pk>/clearcache/',ClientsClearcacheView.as_view()),
    path('<int:pk>/remo_scs_cpf/',RemoStartChargeView.as_view()),
    path('<int:pk>/remo_stop_cs/',RemoStopChargeView.as_view()),
    path('<int:pk>/unlock_connector/',UnlockConnView.as_view()),
    path('<int:pk>/getconf/',GetConfView.as_view()),
    path('<int:pk>/setconf/',SetConfView.as_view()),
    path('<int:pk>/reset/',ResetView.as_view()),
    path('<int:pk>/delete/',ClientsDelete),
    path('confirm/',clientsConfirm),
]