from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView,DeleteView
from .models import Clients
from .forms import ClientsCheckForm, ClientsTagCheckForm,ClientsDeleteForm
from django.db.models import Q
from cardinfo.models import Cardinfo
# Create your views here.


from ocpp16.client_gateway import (reset_evcharger,clearcache_evcharger,
                    remotestop_evcharger,remotestart_evcharger,unlock_connector,get_conf,set_conf)

class ClientsList(ListView):
    model = Clients
    template_name = 'clients.html'
    context_object_name = 'clientsList'
    paginate_by = 5
    queryset = Clients.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.session['user']
        query = self.request.GET.get("q", None)
        page = self.request.GET.get('page')
        context['loginuser'] = user_id
        context['q'] = query
        context['page']=page
        return context
    def get_queryset(self) :
        user_id = self.request.session['user']
        queryset = Clients.objects.all()
        query = self.request.GET.get("q", None)
        if query:
            queryset = queryset.filter(           
                Q(cpnumber__icontains=query)
            )
        return queryset

def ClientsDelete(request,pk):
    clients = Clients.objects.get(id=pk)
    user_id = request.session.get('user')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    if request.method =='POST':
        form = ClientsDeleteForm(request.POST)
        if form.is_valid():
            clients.delete()
            return render(request,'clients_confirm_delete.html',{
                'form' : form,
                'msg' : 'ok',
                'clients' : clients
            })
    else:
        form = ClientsDeleteForm()
    return render(request,'clients_confirm_delete.html',{
        'form' : form,
        'clients' : clients
    })


class ClientsDetail(DetailView):
    template_name = 'clients_detail.html'
    queryset = Clients.objects.all()
    context_object_name ='Clients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        return context

class ClientsClearcacheView(FormView):
    template_name ='clients_check.html'
    form_class = ClientsCheckForm
    success_url = '/clients/confirm/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        return context
    def form_valid(self, form):
        cpnumber = form.data.get('cpnumber')
        clearcache_evcharger(cpnumber)

        return super().form_valid(form)

class RemoStartChargeView(FormView):
    template_name = 'clients_check.html'
    form_class = ClientsCheckForm
    success_url = '/clients/confirm/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        
        return context
    def form_valid(self, form):
        cpnumber = form.data.get('cpnumber')
        userid = self.request.session['user']
        cardinfo = Cardinfo.objects.filter(userid=userid)
        if cardinfo.count() == 0:
            pass
        else:    
            idTag =cardinfo.values()[0]['cardtag']
            remotestart_evcharger(cpnumber,idTag)

        return super().form_valid(form)

class RemoStopChargeView(FormView):
    template_name = 'clients_check.html'
    form_class = ClientsCheckForm
    success_url = '/clients/confirm/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        return context
    def form_valid(self, form):
        cpnumber = form.data.get('cpnumber')
        remotestop_evcharger(cpnumber)

        return super().form_valid(form)

class UnlockConnView(FormView):
    template_name = 'clients_check.html'
    form_class = ClientsCheckForm
    success_url = '/clients/confirm/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        return context
    def form_valid(self, form):
        cpnumber = form.data.get('cpnumber')
        unlock_connector(cpnumber)

        return super().form_valid(form)

class GetConfView(FormView):
    template_name = 'clients_check.html'
    form_class = ClientsCheckForm
    success_url = '/clients/confirm/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        return context
    def form_valid(self, form):
        cpnumber = form.data.get('cpnumber')
        get_conf(cpnumber)
        return super().form_valid(form)

class SetConfView(FormView):
    template_name = 'clients_check.html'
    form_class = ClientsCheckForm
    success_url = '/clients/confirm/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        return context
    def form_valid(self, form):
        cpnumber = form.data.get('cpnumber')
        set_conf(cpnumber)
        return super().form_valid(form)

class ResetView(FormView):
    template_name = 'clients_check.html'
    form_class = ClientsCheckForm
    success_url = '/clients/confirm/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        return context
    def form_valid(self, form):
        cpnumber = form.data.get('cpnumber')
        reset_evcharger(cpnumber)
        return super().form_valid(form)

def clientsConfirm(request):
    user_id = request.session.get('user')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    return render(request,'clients_confirm.html',{
        'loginuser' : user_id,
        'msg' : 'ok'
    })