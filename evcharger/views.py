from django.shortcuts import render
from .forms import EvchargerUpdateForm,EvchargerCreateForm,EvchargerDeleteForm
from django.views.generic import ListView, DetailView,View
from django.views.generic.edit import FormView,UpdateView, CreateView, DeleteView
from .models import Evcharger
from django.db.models import Q
# Create your views here.
class EvchargerListView(ListView):
    model = Evcharger
    template_name = 'evcharger.html'
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
        context['loginuser'] = user_id
        context['page']=page
        context['category'] = category
        return context
    def get_queryset(self) :
        queryset = Evcharger.objects.all()
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

class EvchargerDetailView(DetailView):
    template_name = 'evcharger_detail.html'
    context_object_name = 'evcharger'
    queryset = Evcharger.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.session['user']
        context['loginuser'] = user_id
        return context

class EvchargerUpdateView(UpdateView):
    template_name = 'evcharger_update.html'
    form_class = EvchargerUpdateForm
    model = Evcharger
    success_url = '/evcharger'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        return context

class EvchargerDeleteView(DeleteView):
    model = Evcharger
    template_name = 'evcharger_confirm_delete.html'
    success_url = '/evcharger'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        return context
def EvchargerDelete(request,pk):
    user_id = request.session.get('user')
    evcharger = Evcharger.objects.get(id=pk)
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    if request.method =='POST':
        form = EvchargerDeleteForm(request.POST)
        if form.is_valid():
            
            
            evcharger.delete()

            return render(request,'evcharger_confirm_delete.html',{
                'id' : id,
                'form':form,
                'msg':'ok',
            })
        return render(request,'evcharger_confirm_delete.html',{'form':form,'evcharger':evcharger})
    else:
        form = EvchargerDeleteForm()
    return render(request,'evcharger_confirm_delete.html',{'form':form,'evcharger':evcharger})
class EvchargerRegisterView(FormView):
    model = Evcharger
    template_name = 'evcharger_register.html'
    success_url = '/evcharger'
    form_class=EvchargerCreateForm
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
            detailaddress = form.data.get('detailaddress') ,
            extraaddress = form.data.get('extraaddress'),
            engineer = user_id
        )
        evcharger.save()
        
        return super().form_valid(form)



