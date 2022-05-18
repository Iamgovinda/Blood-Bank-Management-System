from django.http import HttpResponse
from django.shortcuts import render,redirect
import random
from User.forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from Blood import models
from Blood.models import Stock


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
def AdminDash(request):
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

def UpdateView(request):
    if request.method=="POST":
        bloodgroup = request.POST.get('bloodgroup')
        unit = request.POST.get('unit')
        Stock.objects.filter(bloodgroup=bloodgroup).unit = unit
        Stock.objects.filter(bloodgroup=bloodgroup).save()
        
        
        return redirect('/admin/blood-stock/')
