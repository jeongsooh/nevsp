from django.urls import path,reverse_lazy
from .views import *
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView
app_name = 'mypage'

urlpatterns= [
    path('',usermain),
    path('charge/',MypageListView.as_view()),
    path('card/',mypagecard),
    path('etc/',mypageETC),
    path('station/',chargeStations.as_view()),
    path('detail/',mypageDetail), 
    path('<int:pk>/',mypageUpdateView.as_view()), 
    path('cardregi/',card_reg,name='card_reg'),      
    path('cardmanual/',mypagecardreg_manual,name='card_reg_manual'),
    path('<int:pk>/edit',cardedit),
    path('<int:pk>/delete',carddelete),
    path('<int:pk>/re/',cardreedit),
    path('delete/',mypageUserDelete),
    path('payment/',mypagePayment),
    
]