from django.urls import path
from .views import Ocpp16List
app_name = 'ocpp16'

urlpatterns = [
    path('',Ocpp16List.as_view()),

]