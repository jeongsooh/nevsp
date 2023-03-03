
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import LoginForm,RegisterForm,EvuserupdateForm,passwordChangeForm,RecoveryIdForm,EvuserDeleteForm
from django.contrib.auth import get_user_model ,authenticate 
from django.contrib.auth.hashers import make_password ,check_password
from django.views.generic.edit import FormView,UpdateView,DeleteView,CreateView
from django.views.generic import ListView,DetailView,View
from .models import Evuser
import re
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from evuser.models import Evuser
from django.contrib import auth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.serializers.json import DjangoJSONEncoder
from cardinfo.models import Cardinfo

# Create your views here.
def index(request):
    if 'user' in request.session:

        username = request.session['user']
        evuser = Evuser.objects.get(userid = username)
        level = evuser.level
        if level == 'admin':
                return redirect('/evmain')
        elif level == 'Engineer':
            return redirect('/engineer/')
        else :
            return redirect('/mypage')

    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.data.get('userid')
            password = form.data.get('password')
            user = auth.authenticate(request,username=username,password=password)
            request.session['user'] = username
            evuser = Evuser.objects.get(userid = username)
            level = evuser.level
            pk = evuser.id
            request.session['id'] =  pk
            
            if level == 'admin':
                return redirect('/evmain')
            elif level == 'Engineer':
                return redirect('/engineer/')
            else :
                return redirect('/mypage')


    else:
        form = LoginForm()
    
    return render(request,'index.html',{'form':form})


def login(request):
    
    if request.method=='POST':
        id = request.POST.get('userid')
        pw = request.POST.get('password')
        
        result = authenticate(request,username = id ,password = pw)

        if result:
            login(request,result)
            return render(request,'/evmain')
        else :
            return render(request,'/index')

    return render(request,'/index')

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])
    
    return redirect('/')


class EvuserRegisterView(FormView):
    form_class = RegisterForm
    template_name = 'register.html'

    success_url='/'
    
    def form_valid(self, form):
        evuser = Evuser(
            userid = form.data.get('userid'),
            password = make_password(form.data.get('password')),
            name = form.data.get('name'),
            email = form.data.get('email'),
            phone = re.sub(r"[^0-9]","",form.data.get('phone')),
            postcode = form.data.get('postcode'),
            roadAddress = form.data.get('roadAddress'),
            jibunAddress = form.data.get('jibunAddress'),
            detailaddress = form.data.get('detailaddress') ,
            extraaddress = form.data.get('extraaddress')
        )
        evuser.save()
        
        return super().form_valid(form)



class EvuserCreateView(FormView):
  form_class = RegisterForm
  template_name = 'evuser_register.html'
  
  success_url = '/evuser'
  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        return context
  def form_valid(self, form):
        evuser = Evuser(
            userid = form.data.get('userid'),
            password = make_password(form.data.get('password')),
            name = form.data.get('name'),
            email = form.data.get('email'),
            phone = re.sub(r"[^0-9]","",form.data.get('phone')),
            postcode = form.data.get('postcode'),
            roadAddress = form.data.get('roadAddress'),
            jibunAddress = form.data.get('jibunAddress'),
            detailaddress = form.data.get('detailaddress') ,
            extraaddress = form.data.get('extraaddress')
        )
        evuser.save()
        return super().form_valid(form)

class EvuserDetailView(DetailView):
    template_name = 'evuser_detail.html'
    queryset = Evuser.objects.all()
    context_object_name = 'evuser'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user_id = self.request.session['user']
        context['loginuser'] = user_id
        return context

class EvuserListView(ListView):
    template_name = 'evuser.html'
    model = Evuser
    context_object_name = 'evuserList'
    paginate_by = 10
    queryset = Evuser.objects.all()
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        queryset = Evuser.objects.all()
        query = self.request.GET.get("q", None)
        user_id = self.request.session['user']
        page = self.request.GET.get('page')
        category = self.request.GET.get('category')
        context['q'] = query
        context['category'] = category
        context['loginuser'] = user_id
        context['page']=page
        return context
    def get_queryset(self) :
        queryset = Evuser.objects.all()
        query = self.request.GET.get("q", None)
        category = self.request.GET.get('category')
        if query:
            if category=='all':
                queryset = queryset.filter(
                    Q(userid__icontains=query) |
                    Q(name__icontains=query) |
                    Q(phone__icontains=query)|
                    Q(roadAddress__icontains=query)|
                    Q(status__icontains=query)|
                    Q(category__icontains=query)
                )
            elif category=='userid':
                queryset = queryset.filter(           
                    Q(userid__icontains=query))
            elif category=='name':
                queryset = queryset.filter(           
                    Q(name__icontains=query))
            elif category=='phone':
                queryset = queryset.filter(           
                    Q(phone__icontains=query))
            elif category=='roadAddress':
                queryset = queryset.filter(           
                    Q(roadAddress__icontains=query))
            elif category=='status':
                queryset = queryset.filter(           
                    Q(status__icontains=query))
            elif category=='category':
                queryset = queryset.filter(           
                    Q(category__icontains=query))
        return queryset

class EvuserUpdateView(UpdateView):
    model = Evuser
    form_class = EvuserupdateForm
    template_name = 'evuser_update.html'
    success_url = '/evuser'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        return context

    # def form_valid(self, form):
    #     user_id = form.data.get('userid')
    #     evuser = Evuser.objects.filter(userid=user_id)
    #     email = form.data.get('email')
    #     phone = re.sub(r"[^0-9]","",form.data.get('phone')),
    #     roadAddress = form.data.get('roadAddress')
    #     jibunAddress = form.data.get('jibunAddress')
    #     detailaddress = form.data.get('detailaddress') 
    #     extraaddress = form.data.get('extraaddress')
    #     category = form.data.get('category')
    #     status = form.data.get('status')
    #     level = form.data.get('level')
    #     evuser.update(email=email,phone=phone,category=category,status=status,level=level,
    #             roadAddress=roadAddress,jibunAddress=jibunAddress,detailaddress=detailaddress,extraaddress=extraaddress)
        
    #     return super().form_valid(form)

class EvuserDeleteView(DeleteView):
    model = Evuser 
    template_name = 'evuser_confirm_delete.html'
    success_url = '/evuser'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        return context


def EvuserDelete(request,pk):
    evuser = Evuser.objects.get(id=pk)
    user_id = request.session.get('user')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    if request.method =='POST':
        form = EvuserDeleteForm(request.POST)
        if form.is_valid():
            try :
                cardinfo = Cardinfo.objects.get(userid=evuser.userid)
                cardinfo.delete()
            except:pass
            evuser.delete()
            return render(request,'evuser_confirm_delete.html',{
                'id' : pk,
                'form':form,
                'msg':'ok'
            })
        return render(request,'evuser_confirm_delete.html',{'form':form,'evuser':evuser})
    else:
        form = EvuserDeleteForm()
    return render(request,'evuser_confirm_delete.html',{'form':form,'evuser':evuser})


def id_check(request):
    userid = request.POST.get('userid')
    try :
        _id = Evuser.objects.get(userid=userid)
    except Exception as e:
        _id = None
    if _id is not None:
        data = 'exist'
    else:
        data = 'not exist'
        if len(userid) < 4 :
            data = 'lenerror'
        
    context = {
        'result':'success',
        # 'data' : model_to_dict(user)  # console에서 확인
        'data' : data
    }
    return JsonResponse(context)

def EvuserPasswordChange(request,pk):
    user_id = request.session.get('user')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'evuser_detail.html',{'msg':msg})
    request.session['loginuser'] = user_id
    evuser = Evuser.objects.get(id=pk)
    if request.method == 'POST':
        form = passwordChangeForm(request.POST)
        if form.is_valid():
            oldpassword = form.data.get('oldpassword')
            password1 = form.data.get('password1')
            password2 = form.data.get('password2')
            
            if not check_password(oldpassword,evuser.password):
                password_reg = "failed1"
                return render(request,'evuser_password_change.html',{
                    'evuser':evuser ,
                    'password_reg' : password_reg
                    })
            if oldpassword == password1:
                password_reg = 'failed2'
                return render(request,'evuser_password_change.html',{
                    'evuser':evuser ,
                    'password_reg' : password_reg
                    })
            if password1 != password2:
                password_reg = 'failed3'
                return render(request,'evuser_password_change.html',{
                    'evuser':evuser ,
                    'password_reg' : password_reg
                    })
            if len(password1) < 8:
                password_reg = 'failed4'
                return render(request,'evuser_password_change.html',{
                    'evuser':evuser ,
                    'password_reg' : password_reg
                    })
            print(password1,password2,oldpassword)
            password1 = make_password(password1)
            Evuser.objects.filter(id=pk).update(password=password1)
            password_reg = 'ok'
            return render(request,'evuser_detail.html',{
            'evuser':evuser,
            'password_reg' : password_reg
    })
    return render(request,'evuser_password_change.html',{'evuser':evuser})

# @method_decorator(logout_message_required,name='dispatch')
class RecoveryIdView(View):
    template_name = 'recovery_id.html'
    recovery_id = RecoveryIdForm

    def get(self,request):
        if request.method=='GET':
            form = self.recovery_id(None)
        return render(request,self.template_name,{'form':form})

def ajax_find_id_view(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    result_id = Evuser.objects.get(name=name,email=email)

    return HttpResponse(json.dumps({"result_id":result_id.userid},cls=DjangoJSONEncoder), content_type = "application/json")