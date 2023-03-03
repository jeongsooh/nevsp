from django.urls import path
from .views import EvmainListView, EvmainDelete

app_name = 'evmain'

urlpatterns = [
    path('', EvmainListView.as_view()),
    path('<int:pk>/delete/', EvmainDelete),
]