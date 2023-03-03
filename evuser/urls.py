from django.urls import path

from .views import *

app_name = 'evuser'

urlpatterns= [
    path('<int:pk>/',EvuserDetailView.as_view()),
    path('<int:pk>/delete/',EvuserDelete),
    path('register/',EvuserCreateView.as_view()),
    path('<int:pk>/update',EvuserUpdateView.as_view(),name='update'),
    path('',EvuserListView.as_view()),
    path('<int:pk>/password/',EvuserPasswordChange,name='password'),
]