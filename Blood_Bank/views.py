from django.http import HttpResponse
from django.shortcuts import render,redirect
import random
from User.forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from Blood import models
from Blood.models import Stock
from User.decorators import role_required
from Blood_Bank.forms import CampaignForm


# Create your views here.

def home(request):
    quote = ["“Blood Donation Is A Great Act Of Kindness.”","“Blood Donation Is A Small Act Of Kindness That Does Great And Big Wonders.”","“Blood Donation Costs You Nothing, But It Can Mean The World To Someone In Need.”","“Donate Blood Because You Never Know How Helpful It Might Be To Someone.”","“Donate Blood So That You Can Say That You Have Served Mankind.”"," “Donate Blood For The Sake Of God’s Pleasure And For Mankind’s Welfare.”"]
    index = random.randint(0,5)
    context = {"quote":quote[index]}
    return render(request,'Blood_Bank/home.html',context)

def AdminLogin(request):
    if request.method=='GET':
            admin_login = UserLoginForm()
            context={'aloginform':admin_login}
            return render(request,'Admin/admin_login.html',context)

@login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'],redirect_route="/client/client-dash/")
def AdminDash(request):
    x=models.Stock.objects.all()
    print(x)
    if len(x)==0:
        blood1=models.Stock()
        blood1.bloodgroup="A+"
        blood1.save()

        blood2=models.Stock()
        blood2.bloodgroup="A-"
        blood2.save()

        blood3=models.Stock()
        blood3.bloodgroup="B+"
        blood3.save()        

        blood4=models.Stock()
        blood4.bloodgroup="B-"
        blood4.save()

        blood5=models.Stock()
        blood5.bloodgroup="AB+"
        blood5.save()

        blood6=models.Stock()
        blood6.bloodgroup="AB-"
        blood6.save()

        blood7=models.Stock()
        blood7.bloodgroup="O+"
        blood7.save()

        blood8=models.Stock()
        blood8.bloodgroup="O-"
        blood8.save()

    context={
        'A1':str(models.Stock.objects.get(bloodgroup="A+").unit) + ' ML',
        'A2':str(models.Stock.objects.get(bloodgroup="A-").unit) + ' ML',
        'B1':str(models.Stock.objects.get(bloodgroup="B+").unit) + ' ML',
        'B2':str(models.Stock.objects.get(bloodgroup="B-").unit) + ' ML',
        'AB1':str(models.Stock.objects.get(bloodgroup="AB+").unit) + ' ML',
        'AB2':str(models.Stock.objects.get(bloodgroup="AB-").unit) + ' ML',
        'O1':str(models.Stock.objects.get(bloodgroup="O+").unit) + ' ML',
        'O2':str(models.Stock.objects.get(bloodgroup="O-").unit) + ' ML',
        }
    return render(request,"Admin/admin_dashboard.html",context)

@login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'],redirect_route="/client/client-dash/")
def StockView(request):
    context={
        'A1':str(models.Stock.objects.get(bloodgroup="A+").unit) + ' ML',
        'A2':str(models.Stock.objects.get(bloodgroup="A-").unit) + ' ML',
        'B1':str(models.Stock.objects.get(bloodgroup="B+").unit) + ' ML',
        'B2':str(models.Stock.objects.get(bloodgroup="B-").unit) + ' ML',
        'AB1':str(models.Stock.objects.get(bloodgroup="AB+").unit) + ' ML',
        'AB2':str(models.Stock.objects.get(bloodgroup="AB-").unit) + ' ML',
        'O1':str(models.Stock.objects.get(bloodgroup="O+").unit) + ' ML',
        'O2':str(models.Stock.objects.get(bloodgroup="O-").unit) + ' ML',
        }
    return render(request,"Admin/blood_stock.html",context)

login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'],redirect_route="/client/client-dash/")
def UpdateView(request):
    if request.method=="POST":
        bloodgroup = request.POST.get('bloodgroup')
        unit = request.POST.get('unit')
        blood = Stock.objects.get(bloodgroup=bloodgroup)
        blood.unit = unit
        blood.save()
        return redirect('/admin/blood-stock/')

login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'],redirect_route="/client/client-dash/")
def CreateCampaign(request):
    campaignform = CampaignForm()
    print(campaignform)
    return render(request,'Admin/create_campaign.html',{'campaignform':campaignform})

