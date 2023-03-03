from django.urls import path
from .views import *

app_name = 'varialbes'

urlpatterns=[
    path('',VariablesList.as_view()),
    path('<int:pk>/',VariablesDetail.as_view()),
    path('<int:pk>/delete/',VariablesDeleteView.as_view()),
    path('register/',VariablesCreateView.as_view()),
    path('<int:pk>/update/',VariablesUpdateView.as_view()),

]