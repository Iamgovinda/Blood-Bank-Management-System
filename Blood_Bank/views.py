from tokenize import group
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import render,redirect
import random
from User.forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from Blood import models
from Blood.models import Stock
from User.decorators import role_required
from Blood_Bank.forms import CampaignForm
from django.contrib import messages
from User.models import Profile
from django.contrib.auth.models import User,Group
from User.forms import *
from Blood_Bank.models import Campaign
from Blood_Bank.forms import CampaignForm
from Blood.models import BloodRequest
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
@role_required(allowed_roles=['Blood Bank Manager'],redirect_route="/client/client-dash/")
def AdminDash(request):
    # user = User.objects.get(id=2)
    # print(user.username)
    # print(type(user))
    # print(type(user.username))
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
@role_required(allowed_roles=['Blood Bank Manager'],redirect_route="/admin/admin-dash/")
def CreateCampaign(request):
    campaigns = Campaign.objects.all()
    if request.method == "POST":
        campaignform = CampaignForm(request.POST)
        if campaignform.is_valid():
            campaignform.save()
            return redirect('Create_Campaign')
        else:
            messages.error(request,"Form is not valid")
            return redirect('Create_Campaign')
    else:
        campaignform = CampaignForm()
        print(campaignform)
    return render(request,'Admin/create_campaign.html',{'campaignform':campaignform,'campaigns':campaigns})

login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'],redirect_route="/admin/admin-dash/")
def ViewClients(request):
    # usergroup = Group.objects.get(name='Client')
    # client = User.groups.filter(name=usergroup)
    clients = []
    userprofiles = Profile.objects.all()
    for profile in userprofiles:
        if profile.user.groups.filter(name='Client'):
            clients.append(profile)
    
    return render(request,"Admin/viewclient.html",{'client':clients})

login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'],redirect_route="/admin/admin-dash/")
def UpdateClient(request,pk):
    if request.method == "POST":
        user = User.objects.get(id=pk)
        u_form = UserUpdateForm(request.POST,instance = user)
        p_form = UserProfileForm(request.POST,request.FILES,instance = user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,"Profile Info Updated Successfully!")
            return redirect('/admin/update-client/'+str(pk))
    
    user = User.objects.get(id=pk)
    u_form = UserUpdateForm(instance = user)
    p_form = UserProfileForm(instance = user.profile)


    if request.user_role == "Client":
        extendbase = "User/client_dash_base.html"
    else:
        extendbase = "Admin/admin_dash_base.html"


    context = {
        'u_form':u_form,
        'p_form':p_form,
        'user': user,
        'extendbase':extendbase
    }

    return render(request,'Admin/updateclient.html',context)

def DeleteClient(request,pk):
    user = User.objects.get(id=pk)
    user.delete()
    return redirect('/admin/view-clients/')

def DeleteCampaign(request,pk):
    Campaign.objects.filter(id=pk).delete()
    return redirect('/admin/create-campaign/')

def EditCampaign(request,pk):
    campaign = Campaign.objects.get(id=pk)
    campaigns = Campaign.objects.all()
    if request.method == "POST":
        campaignform = CampaignForm(request.POST,instance=campaign)
        print("Here")
        if campaignform.is_valid():
            campaignform.save()
            return redirect('/admin/create-campaign/')
        else:
            return HttpResponse('Form not valid')
    else:
        campaignform = CampaignForm(instance=campaign)
    return render(request,"Admin/edit_campaign.html",{'campaignform':campaignform,'campaigns':campaigns,'id':pk})

    
def ViewBloodRequests(request):
    bloodrequests = BloodRequest.objects.all()
    for br in bloodrequests:
        print(br.status)
        if br.status == "Approved":
            status = "Approved"
        elif br.status == "Rejected":
            status = "Rejected"
        else:
            status = "Pending"
    return render(request,"Admin/view-blood-request.html",{"bloodrequests":bloodrequests,"status":status})


def ApproveBloodRequest(request,pk):
    br = BloodRequest.objects.get(id=pk)
    bloodgroup = br.patient_bloodgroup
    requestedbloodunit = br.unit
    stockblood = Stock.objects.get(bloodgroup=bloodgroup)
    stockbloodunit=stockblood.unit
    print(stockbloodunit,requestedbloodunit)

    if stockbloodunit>requestedbloodunit:
        stockblood.unit = stockbloodunit-requestedbloodunit
        br.status = "Approved"
        stockblood.save()
        br.save()
    else:
        return HttpResponse("Stock has no enough blood")
    return redirect("/admin/view-bloodrequests/")

def RejectBloodRequest(request,pk):
    return redirect("/admin/view-bloodrequests/")
