from django.urls import path
from .views import *

app_name = 'cardinfo'

urlpatterns =[
    path('',CardinfoListView.as_view()),
    path('<int:pk>/',CardinfoDetailView.as_view()),
    path('<int:pk>/update/',CardinfoUpdateView.as_view(),name='cardupdate'),
    path('<int:pk>/delete/',CardinfoDelete),
    path('register/',CardinfoCreateView.as_view()),
    path('registerremote/',CardinfoRemoteCreateView.as_view()),
    


]