from django.urls import path, include
from .views import *

app_name = 'evcharger'

urlpatterns = [
    path('',EvchargerListView.as_view()),
    path('<int:pk>/',EvchargerDetailView.as_view()),
    path('<int:pk>/delete/',EvchargerDelete),
    path('register/',EvchargerRegisterView.as_view()),
    path('<int:pk>/update/',EvchargerUpdateView.as_view(),name='cpupdate'),


]