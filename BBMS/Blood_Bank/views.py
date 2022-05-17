from django.shortcuts import render
import random
from User.forms import UserLoginForm
from django.contrib.auth.decorators import login_required

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

def AdminDash(request):
    return render(request,"Admin/admin_dashboard.html")