from django.urls import path
from .views import *

app_name = 'charginginfo'

urlpatterns=  [
    path('',CharginginfoListView.as_view()),
]