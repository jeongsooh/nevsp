from django.shortcuts import render
from django.views.generic import ListView
from .models import Ocpp16
from datetime import datetime,date,timedelta
from django.db.models import Q
# Create your views here.
class Ocpp16List(ListView):
    model = Ocpp16
    template_name = 'ocpp16.html'
    context_object_name = 'ocpp16List'
    paginate_by = 10
    queryset = Ocpp16.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.session['user']
        query = self.request.GET.get("q",None)
        page = self.request.GET.get('page')
        start_dttm = self.request.GET.get('start_dttm')
        end_dttm = self.request.GET.get('end_dttm')
        context['loginuser'] = user_id
        context['q'] = query
        context['page']=page
        context['start_dttm'] = start_dttm
        context['end_dttm'] =end_dttm
        return context
    def get_queryset(self) :
        queryset = Ocpp16.objects.all()
        query = self.request.GET.get("q",None)
        start_dttm = self.request.GET.get('start_dttm','')
        end_dttm = self.request.GET.get('end_dttm','')
        if query:
            queryset = queryset.filter(
                Q(cpnumber__icontains=query)
            )
        if start_dttm != '':
            start_dttm = datetime.strptime(start_dttm,"%Y-%m-%dT%H:%M")
        else :
            start_dttm = datetime(2000,1,1)
        if end_dttm != '':    
            end_dttm = datetime.strptime(end_dttm,"%Y-%m-%dT%H:%M")
            end_dttm = end_dttm+timedelta(days=1)
        else :
            end_dttm = datetime.now()
        q = Q()
        q.add(Q(register_dttm__range=(start_dttm, end_dttm)),q.AND)
        queryset = queryset.filter(q) 
        return queryset

        