from django.shortcuts import render,redirect
from django.views.generic import ListView,View,FormView
from django.views.generic.edit import UpdateView
from cardinfo.models import Cardinfo
from ocpp16.client_gateway import get_cardtag
from evuser.models import Evuser
from charginginfo.models import Charginginfo
from evcharger.models import Evcharger
from django.db.models import Q
from datetime import datetime,timedelta,date
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import mypageUserDeleteForm, mypageupdateForm,passwordChangeForm ,mypageCardCreateForm,mypageCardEditForm,mypageCardDeleteForm,mypageCardManualForm,mypageCardreEditForm
from geopy.geocoders import Nominatim
import requests, json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import check_password,make_password
import re
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


class MypageListView(ListView):
    
    model = Charginginfo
    template_name = 'mypage_charging.html'
    context_object_name = 'mypageList'
    paginate_by = 10
    
    def get_queryset(self) :
        user_id = self.request.session['user']
        if(user_id == None):
            msg = 'loginfail'
            return render(self.request,'mypage.html',{'msg':msg})
        queryset = Charginginfo.objects.filter(userid=user_id)
        query = self.request.GET.get("q",None)
        if query:
            queryset = queryset.filter(
                Q(cpnumber__icontains=query)
            )
        
        start_dttm = self.request.GET.get('start_dttm','')
        end_dttm = self.request.GET.get('end_dttm','')
        if start_dttm != '':
            start_dttm = datetime.strptime(start_dttm,"%Y-%m-%d")
        else :
            if queryset.count() != 0:
                start_dttm = queryset.values().first()['start_dttm']
            else :
                start_dttm = datetime.now().date()
        if end_dttm != '':    
            end_dttm = datetime.strptime(end_dttm,"%Y-%m-%d")
            
        else :
            if queryset.count() != 0:
                end_dttm = queryset.values().last()['end_dttm']
            else :
                end_dttm = datetime.now().date()

        q = Q()
        q.add(Q(start_dttm__range=(start_dttm, end_dttm)),q.AND)
        q.add(Q(end_dttm__range=(start_dttm,end_dttm)),q.AND)
        queryset = queryset.filter(q)    
        return queryset
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs) 
        user_id = self.request.session['user']
        if(user_id == None):
            msg = 'loginfail'
            return render(self.request,'mypage.html',{'msg':msg})
        queryset = Charginginfo.objects.filter(userid=user_id)
        start_dttm = self.request.GET.get('start_dttm','')
        end_dttm = self.request.GET.get('end_dttm','')
        if start_dttm != '':
            start_dttm = datetime.strptime(start_dttm,"%Y-%m-%d")
        else :
            if queryset.count() != 0:
                start_dttm = queryset.values().first()['start_dttm']
            else :
                start_dttm = datetime.now().date()
        if end_dttm != '':    
            end_dttm = datetime.strptime(end_dttm,"%Y-%m-%d")
        else :
            if queryset.count() != 0:
                end_dttm = queryset.values().last()['end_dttm']
            else :
                end_dttm = datetime.now().date()
        totalamount = 0
        q = Q()
        q.add(Q(start_dttm__range=(start_dttm, end_dttm)),q.AND)
        q.add(Q(end_dttm__range=(start_dttm,end_dttm)),q.AND)
        queryset = queryset.filter(q)
        for a in range(queryset.count()):
            totalamount += queryset.values()[a]['amount']
        context['start_dttm'] = start_dttm
        context['end_dttm'] = end_dttm 
        context['totalamount'] = totalamount
        context['loginuser'] = user_id
        return context


def usermain(request):
    user_id = request.session.get('user')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    return render(request,'mypage.html',{
        'loginuser' : user_id
    })

def mypagecard(request):
    user_id = request.session.get('user')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    cardinfo = Cardinfo.objects.filter(userid=user_id)

    return render(request,'mypage_card.html',{
        'cardinfo' : cardinfo,
        'loginuser' : user_id
    })

def mypagecardreg_manual(request):
    user_id = request.session.get('user')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    if request.method =='POST':
        form = mypageCardManualForm(request.POST)
        if form.is_valid():
            
            cardinfo = Cardinfo(
                cardname = form.data.get('cardname'),
                cardtag = form.data.get('cardnum1')+form.data.get('cardnum2')+form.data.get('cardnum3')+form.data.get('cardnum4'),
                userid = user_id,
                cardstatus = '배포됨'
            )
            cardinfo.save()
            card_msg = 'manualok'
            cardinfo = Cardinfo.objects.filter(userid=user_id)
            return render(request,'mypage_card.html',{
                'card_msg' : card_msg,
                'cardinfo' : cardinfo,
                'loginuser' : user_id
            })
            
    else:
        form = mypageCardManualForm()
    return render(request,'mypage_card_reg_manual.html',{
        'form' : form,
        'userid' : user_id,
        'loginuser' : user_id
    })

def cardedit(request,pk):
    user_id = request.session.get('user')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    if request.method =='POST':
        form = mypageCardEditForm(request.POST)
        if form.is_valid():
            cardname = form.data.get('newcardname')
            id = pk
            Cardinfo.objects.filter(id=id).update(cardname=cardname)
            return render(request,'mypage_card_edit.html',{
                'cardname' : cardname,
                'id' : id,
                'form':form,
                'msg':'ok'
            })
        return render(request,'mypage_card_edit.html',{'form':form})
    else:
        form = mypageCardEditForm()
    return render(request,'mypage_card_edit.html',{'form':form})


def cardreedit(request,pk):
    user_id = request.session.get('user')
    Cardinfo.objects.filter(id=pk).update(cardstatus='처리중',cardtag='')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    if request.method =='POST':
        form = mypageCardreEditForm(request.POST)
        if form.is_valid():
            cpnumber = form.data.get('cpnumber')
            id = pk
            cardinfo = Cardinfo.objects.get(id=id)
            get_cardtag(cpnumber,cardinfo.userid)
            return render(request,'mypage_card_reedit.html',{
                'cardinfo' : cardinfo,
                'form':form,
                'msg':'ok'
            })
        return render(request,'mypage_card_reedit.html',{'form':form})
    else:
        form = mypageCardreEditForm()
    return render(request,'mypage_card_reedit.html',{'form':form})


def carddelete(request,pk):
    cardinfo = Cardinfo.objects.get(id=pk)
    user_id = request.session.get('user')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    if request.method =='POST':
        form = mypageCardDeleteForm(request.POST)
        if form.is_valid():
            if cardinfo.userid != user_id:
                msg = 'idmatchfail'
                return render(request,'mypage_card_delete.html',{
                    'msg' : msg
                })
            cardinfo.delete()
            return render(request,'mypage_card_delete.html',{
                'id' : id,
                'form':form,
                'msg':'ok'
            })
        return render(request,'mypage_card_delete.html',{'form':form,'cardinfo':cardinfo})
    else:
        form = mypageCardDeleteForm()
    return render(request,'mypage_card_delete.html',{'form':form,'cardinfo':cardinfo})


def card_reg(request):
    user_id = request.session.get('user')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    card_msg = ''
    if request.method =='POST':
        form = mypageCardCreateForm(request.POST)
        
        if form.is_valid():
           
            cpnumber = form.data.get('cpnumber')
            cardname = form.data.get('cardname')
            cardinfo = Cardinfo(
                cardname=cardname,
                userid = user_id
            )
            try:
                cardinfo.save()
                get_cardtag(cpnumber,user_id)
                
                card_msg ='ok'
            except:
                card_msg = 'authfail'
                cardinfo = Cardinfo.objects.filter(userid=user_id)
                return render(request,'mypage_card.html',{
                    'card_msg' : card_msg,
                    'cardinfo' : cardinfo,
                    'loginuser' : user_id
                })
                
            cardinfo = Cardinfo.objects.filter(userid=user_id)
            return render(request,'mypage_card.html',{
                    'card_msg' : card_msg,
                    'cardinfo' : cardinfo,
                    'loginuser' : user_id
                })
    else:
        form = mypageCardCreateForm()
    return render(request,'mypage_card_reg.html',{
        'form' : form,
        'userid' : user_id,
        'loginuser' : user_id
    })

def mypagePayment(request):
    user_id = request.session.get('user')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    return render(request,'mypage_payment.html',{
        'loginuser' : user_id
    })

@csrf_exempt
def chargeStation(request):
    user_id = request.session.get('user')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    evcharger = Evcharger.objects.values()
    list = []
    for a in range(evcharger.count()):
        list.append(evcharger[a]['roadAddress'])
    
    return render(request,'mypage_station.html',{
        'evcharger' : evcharger,
        'loginuser' : user_id
    })

class chargeStations(ListView):
    model = Evcharger
    template_name = 'mypage_station.html'
    context_object_name = 'evcharger'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        query = self.request.GET.get("q",None)
        user_id = self.request.session['user']
        page = self.request.GET.get('page')
        category = self.request.GET.get('category')
        context['q'] = query
        context['loginuser'] = user_id
        context['page']=page
        context['category'] = category
        return context
    def get_queryset(self):
        queryset = Evcharger.objects.all()
        query = self.request.GET.get("q",None)
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




    
def mypageETC(request):
    user_id = request.session.get('user')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    return render(request,'mypage_etc.html',{
        'loginuser' : user_id
    })

def mypageDetail(request):
    user_id = request.session.get('user')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    evuser = Evuser.objects.get(userid=user_id)
    if request.method == 'POST':
        form = passwordChangeForm(request.POST)
        if form.is_valid():
            oldpassword = form.data.get('oldpassword')
            password1 = form.data.get('password1')
            password2 = form.data.get('password2')
            if not check_password(oldpassword,evuser.password):
                password_reg = "failed1"
            elif oldpassword == password1:
                password_reg = 'failed2'
            elif password1 != password2:
                password_reg = 'failed3'
            elif len(password1) < 8:
                password_reg = 'failed4'
            else:
                password1 = make_password(password1)
                Evuser.objects.filter(userid=user_id).update(password=password1)
                password_reg = 'ok'
            return render(request,'mypage_detail.html',{
            'evuser':evuser,
            'password_reg' : password_reg,
            'loginuser' : user_id
    })
    return render(request,'mypage_detail.html',{
        'evuser':evuser,
        'loginuser' : user_id
    })


# class mypageUpdateView(UpdateView):
#     model = Evuser
#     form_class = mypageupdateForm
#     template_name = 'mypage_update.html'
#     success_url = '/mypage/detail/'

class mypageUpdateView(UpdateView):
    model = Evuser
    form_class = mypageupdateForm
    template_name = 'mypage_update.html'
    success_url = '/mypage/detail'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session['user']
        context['loginuser'] = userid
        return context
    def form_valid(self, form) :
        
        
        user_id = self.request.session['user']
        if(user_id == None):
            msg = 'loginfail'
            return render(self.request,'mypage.html',{'msg':msg})
        evuser = Evuser.objects.filter(userid=user_id)
        email = form.data.get('email')
        phone = re.sub(r"[^0-9]","",form.data.get('phone')),
        print(phone)
        roadAddress = form.data.get('roadAddress')
        jibunAddress = form.data.get('jibunAddress')
        detailaddress = form.data.get('detailaddress') 
        extraaddress = form.data.get('extraaddress')

        

        evuser.update(email=email,phone=phone,roadAddress=roadAddress,jibunAddress=jibunAddress,detailaddress=detailaddress,extraaddress=extraaddress)

        return super().form_valid(form)

def mypageUserDelete(request):
    user_id = request.session.get('user')
    if(user_id == None):
        msg = 'loginfail'
        return render(request,'mypage.html',{'msg':msg})
    request.session['loginuser'] = user_id
    evuser = Evuser.objects.get(userid=user_id)
    if request.method == 'POST':
        form = mypageUserDeleteForm(request.POST)
        cardinfo = Cardinfo.objects.filter(userid =user_id)
        cardinfo.delete()
        evuser.delete()
        del(request.session['user'])

        return redirect('/')
    else :
        form = mypageUserDeleteForm()
    return render(request,'mypage_user_delete.html',{
        'form' : form,
        'loginuser':user_id
    })