from django.shortcuts import render
from django.views.generic import ListView ,FormView
from evcharger.models import Evcharger
from django.db.models import Q
from .forms import engineerEvchargerCreateForm
from ocpp16.client_gateway import reset_evcharger
from clients.forms import ClientsCheckForm
# Create your views here.


class engineerEvchargerListView(ListView):
    model = Evcharger
    template_name = 'engineer_evcharger.html'
    context_object_name = 'evchargerList'
    paginate_by = 10
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        queryset = Evcharger.objects.all()
        query = self.request.GET.get("q", None)
        user_id = self.request.session['user']
        page = self.request.GET.get('page')
        category = self.request.GET.get('category')
        context['q'] = query
        context['page']=page
        context['loginuser'] = user_id
        context['category'] = category
        return context
    def get_queryset(self) :
        user_id = self.request.session['user']
        queryset = Evcharger.objects.filter(partner_id=user_id)
        query = self.request.GET.get("q", None)
        category = self.request.GET.get('category')
        if query:
            if category=='all':
                queryset = queryset.filter(           
                    Q(cpname__icontains=query) |
                    Q(roadAddress__icontains=query)|
                    Q(cpstatus__icontains=query)
                )
            elif category=='cpname':
                queryset = queryset.filter(           
                    Q(cpname__icontains=query))
            elif category=='cpstatus':
                queryset = queryset.filter(           
                    Q(cpstatus__icontains=query))
            elif category=='roadAddress':
                queryset = queryset.filter(           
                    Q(roadAddress__icontains=query))
        return queryset

class engineerEvchargerRegisterView(FormView):
    model = Evcharger
    template_name = 'engineer_evcharger_register.html'
    success_url = '/engineer/list'
    form_class=engineerEvchargerCreateForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        return context
    def form_valid(self, form):
        user_id = self.request.session['user']
        evcharger = Evcharger(
            cpnumber = form.data.get('cpnumber'),
            cpname = form.data.get('cpname'),
            postcode = form.data.get('postcode'),
            roadAddress = form.data.get('roadAddress'),
            jibunAddress = form.data.get('jibunAddress'),
            partner_id = user_id,
            detailaddress = form.data.get('detailaddress') ,
            extraaddress = form.data.get('extraaddress')
        )
        evcharger.save()
        
        return super().form_valid(form)

class ResetView(FormView):
    template_name = 'engineer_check.html'
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


def engineerHome(request):
    user_id = request.session.get('user')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    return render(request,'engineer_home.html',{
        'loginuser' : user_id
    })