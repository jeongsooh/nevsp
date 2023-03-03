from django.urls import path, include
from .views import *

app_name = 'engineer'

urlpatterns = [
    path('',engineerHome),
    path('list/',engineerEvchargerListView.as_view()),
    path('register/',engineerEvchargerRegisterView.as_view()),
    path('<int:pk>/reset/',ResetView.as_view())
]