from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormView,UpdateView,DeleteView
from .models import Charginginfo
from django.db.models import Q
from evuser.models import Evuser
from datetime import datetime,timedelta,date
# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin

class CharginginfoListView(ListView):
    model=Charginginfo
    template_name = 'charginginfo.html'
    context_object_name='charginginfoList'
    paginate_by = 10
    queryset = Charginginfo.objects.all()
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        queryset = Charginginfo.objects.all()
        query = self.request.GET.get("q", None)
        user_id = self.request.session['user']
        page = self.request.GET.get('page')
        start_dttm = self.request.GET.get('start_dttm')
        end_dttm = self.request.GET.get('end_dttm')
        category = self.request.GET.get('category')
        context['q'] = query
        context['loginuser'] = user_id
        context['page']=page
        context['start_dttm'] = start_dttm
        context['end_dttm'] =end_dttm
        context['category'] = category
        
        return context
    def get_queryset(self) :
        queryset = Charginginfo.objects.all()
        query = self.request.GET.get("q", None)
        if query:
            queryset = queryset.filter(
                Q(userid__icontains=query) |
                Q(energy__icontains=query) |
                Q(amount__icontains=query)
            )
        category = self.request.GET.get('category')
        start_dttm = self.request.GET.get('start_dttm','')
        end_dttm = self.request.GET.get('end_dttm','')
        
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
        if category == 'all':
            q.add(Q(start_dttm__range=(start_dttm, end_dttm)),q.AND)
            q.add(Q(end_dttm__range=(start_dttm,end_dttm)),q.AND)
        elif category =='start_time':
            q.add(Q(start_dttm__range=(start_dttm, end_dttm)),q.AND)
        elif category =='end_time':
            q.add(Q(end_dttm__range=(start_dttm,end_dttm)),q.AND)
        queryset = queryset.filter(q)    
        return queryset


class CharginginfoCreateView(FormView):
    model = Charginginfo
    success_url="/charginginfo"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        return context
    def form_valid(self, form): 
        userid = form.data.get('userid'),
        charginginfo = Charginginfo(
            cpnumber = form.data.get('cpnumber'),
            userid = form.data.get('userid'),
            energy = form.data.get('energy'),
            amount = form.data.get('amount')
        )
        charginginfo.save()
        Evuser.objects.filter(userid=userid).update(last_use_dttm = datetime.now())
        return super().form_valid(form)