from django.shortcuts import render
from .forms import CardinfoCreateForm,CardinfoUpdateForm,CardinfoDeleteForm
from django.views.generic import ListView,FormView,DeleteView,UpdateView,DetailView
from .models import Cardinfo
from django.db.models import Q
# Create your views here.
from ocpp16.client_gateway import get_cardtag

class CardinfoCreateView(FormView):
    template_name = 'cardinfo_register.html'
    form_class = CardinfoCreateForm
    success_url = '/cardinfo'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        return context
    def form_valid(self, form):
        cpnumber = form.data.get('cpnumber')
        userid = form.data.get('userid')

        cardinfo = Cardinfo(
            cardname = form.data.get('cardname'),
            userid = form.data.get('userid'),
        )
        cardinfo.save()
        try:
            get_cardtag(cpnumber,userid)
        except:
            self.request.session['msg'] = 'fail'
        
        return super().form_valid(form)

class CardinfoRemoteCreateView(FormView):
    template_name = 'cardinfo_register_remote.html'
    form_class = CardinfoCreateForm
    success_url = '/cardinfo'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        return context
    def form_valid(self, form):
        userid = form.data.get('userid')
        cpnumber = form.data.get('cpnumber')
        cardinfo = Cardinfo(
            cardname = form.data.get('cardname'),
            userid = form.data.get('userid'),
        )

        cardinfo.save()
        get_cardtag(cpnumber,userid)
        return super().form_valid(form)

class CardinfoUpdateView(UpdateView):
    template_name='cardinfo_update.html'
    model = Cardinfo
    form_class = CardinfoUpdateForm
    success_url = '/cardinfo'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        return context

class CardinfoDetailView(DetailView):
    template_name='cardinfo_detail.html'
    model = Cardinfo
    queryset = Cardinfo.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.session['user']
        context['loginuser'] = user_id
        return context

def CardinfoDelete(request,pk):
    cardinfo = Cardinfo.objects.get(id=pk)
    user_id = request.session.get('user')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    if request.method =='POST':
        form = CardinfoDeleteForm(request.POST)
        if form.is_valid():
            
            cardinfo.delete()
            return render(request,'cardinfo_confirm_delete.html',{
                'id' : id,
                'form':form,
                'msg':'ok'
            })
        return render(request,'cardinfo_confirm_delete.html',{'form':form,'cardinfo':cardinfo})
    else:
        form = CardinfoDeleteForm()
    return render(request,'cardinfo_confirm_delete.html',{'form':form,'cardinfo':cardinfo})

class CardinfoListView(ListView):
    template_name='cardinfo.html'
    model = Cardinfo
    context_object_name = 'cardinfoList'
    queryset = Cardinfo.objects.all()
    paginate_by = 10

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        queryset = Cardinfo.objects.all()
        query = self.request.GET.get("q", None)
        user_id = self.request.session['user']
        page = self.request.GET.get('page')
        category = self.request.GET.get('category')
        context['q'] = query
        context['loginuser'] = user_id
        context['page']=page
        context['category'] = category
        return context
        
    def get_queryset(self) :
        queryset = Cardinfo.objects.all()
        query = self.request.GET.get("q", None)
        category = self.request.GET.get("category")

        if query:
            if category=='all':
                queryset = queryset.filter(
                    Q(userid__icontains=query) |
                    Q(cardtag__icontains=query) |
                    Q(cardstatus__icontains=query)
                )
            elif category=='userid':
                queryset = queryset.filter(
                    Q(userid__icontains=query))
            elif category=='status':
                queryset = queryset.filter(
                    Q(cardstatus__icontains=query))
        return queryset