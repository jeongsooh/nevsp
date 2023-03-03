from django.db.models import Q
from django.shortcuts import render,redirect
from .models import Evmain
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from evmain.forms import EvmainCreate,EvmainDeleteForm
from evuser.models import Evuser
# Create your views here.

class EvmainListView(ListView):
    model = Evmain
    template_name = 'evmain.html'
    context_object_name = 'evmainList'
    paginate_by = 10
    queryset = Evmain.objects.all()
    ordering = ['-systemday']
    EvmainCreate()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.session['user']
        context['loginuser'] = user_id
        return context
    

def EvmainDelete(request,pk):
    evmain = Evmain.objects.get(id=pk)
    user_id = request.session.get('user')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    if request.method =='POST':
        form = EvmainDeleteForm(request.POST)
        if form.is_valid():
            
            evmain.delete()
            return render(request,'evmain_delete.html',{
                'id' : id,
                'form':form,
                'msg':'ok'
            })
        return render(request,'evmain_delete.html',{'form':form,'evmain':evmain})
    else:
        form = EvmainDeleteForm()
    return render(request,'evmain_delete.html',{'form':form,'evmain':evmain})


