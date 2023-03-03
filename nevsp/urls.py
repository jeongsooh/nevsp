"""nevsp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from evuser.views import (
    index, logout, id_check, ajax_find_id_view,
    EvuserRegisterView, RecoveryIdView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('logout/',logout,name='logout'),
    path('evuser/',include('evuser.urls')),
    path('register/',EvuserRegisterView.as_view(),name='register'),
    path('evmain/',include('evmain.urls')),
    path('evcharger/',include('evcharger.urls')),
    path('charginginfo/',include('charginginfo.urls')),
    path('cardinfo/',include('cardinfo.urls')),
    path('logout/',logout),
    path('variables/',include('variables.urls')),
    path('ocpp16/',include('ocpp16.urls')),
    path('clients/',include('clients.urls')),
    path('mypage/',include('mypage.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('id_check/',id_check,name='id_check'),
    path('recovery/id/',RecoveryIdView.as_view(),name='recovery_id'),
    path('recovery/id/find/',ajax_find_id_view,name='ajax_id'),
    path('engineer/',include('engineer.urls')),
]
