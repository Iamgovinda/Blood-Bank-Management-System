from ctypes import create_string_buffer
from email import message
from queue import PriorityQueue
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from Blood_Bank.models import Campaign
from User.decorators import role_required
from .forms import UserRegistrationForm,UserLoginForm,UserProfileForm,UserUpdateForm
from Blood.forms import BloodRequestForm,DonationRequestForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group,User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from User import models as U_model
from Blood import models as B_model
from User.models import Profile
from Blood.models import BloodRequest,DonationRequest,Stock

# Create your views here.
def UserRegistration(request):
    if request.method=='POST':
        clientform = UserRegistrationForm(request.POST)
        
        # usergroup = Group.objects.get(name='Client')
        if clientform.is_valid():
            data = clientform.cleaned_data
            if data['password1']==data['password2']:
                if User.objects.filter(username=data['username']).exists():
                    messages.error(request,"Username Taken")
                    return redirect('/client/registration/')
                elif User.objects.filter(email=data['email']).exists():
                    messages.error(request,"Email Taken")
                    return redirect('/client/registration/')
                else:
                    # client = User.objects.create(username=data['username'],email=data['email'],first_name=data['first_name'],last_name=data['last_name'])
                    
                    clientform.save()
                    # usergroup.user_set.add(client)
                    messages.success(request,"User created")
                    return redirect('/client/login')
            else:

                messages.info(request,"Password not matching")
                return redirect('/client/registration/')
        messages.error(request,"Form is not valid")
    cregform=UserRegistrationForm()
    return render(request,'User/user_registration.html',{"cregform":cregform})


def UserLogin(request):
    if request.method=="POST":
        clientform = UserLoginForm(request.POST)
        requestfrom = request.POST.get('loginform',"clientloginform")
        print(requestfrom)
        if requestfrom == "clientloginform":
            usergroup = Group.objects.get(name='Client')
            homepage = '/client/client-dash/'
            redirecturl = "/client/login/"
        else:
            usergroup = Group.objects.get(name='Blood Bank Manager')
            homepage = '/admin/admin-dash/'
            redirecturl = "/admin/login/"

        
        
        if clientform.is_valid():
            print(clientform.is_valid())
            data = clientform.cleaned_data
            client = authenticate(username=data['username'],password=data['password'])
            print(data)
            print(client)
            if client is not None:
                if client.groups.filter(name=usergroup):
                    login(request,client)
                    messages.success(request,"Successfully logged in!")
                    return redirect(homepage)
                else:
                    messages.error(request,"Invalid User Group")
                    return redirect(redirecturl)
            else:
                messages.error(request,'Invalid Credential !!!')
                return redirect(redirecturl)
        else:
            messages.info(request,'Form not valid')
    else:
        clientloginform = UserLoginForm()
    return render(request, "User/user_login.html", {"cloginform":clientloginform})



def UserLogout(request):
    logout(request)
    messages.success(request,"You have been logged out successfully")
    return redirect('/')

@login_required(login_url="/client/login/")
@role_required(allowed_roles=['Client'],redirect_route='/admin/admin-dash/')
def UserHome(request):
    client = Profile.objects.get(user_id = request.user.id)
    context = {
        'br_pending': BloodRequest.objects.all().filter(request_by_client=client).filter(status='Pending').count(),
        'br_approved': BloodRequest.objects.all().filter(request_by_client=client).filter(status='Approved').count(),
        'br_rejected': BloodRequest.objects.all().filter(request_by_client=client).filter(status='Rejected').count(),
        'br_total': BloodRequest.objects.all().filter(request_by_client=client).count(),
        'dr_pending': DonationRequest.objects.all().filter(request_by_client=client).filter(status='Pending').count(),
        'dr_approved': DonationRequest.objects.all().filter(request_by_client=client).filter(status='Approved').count(),
        'dr_rejected': DonationRequest.objects.all().filter(request_by_client=client).filter(status='Rejected').count(),
        'dr_total': DonationRequest.objects.all().filter(request_by_client=client).count(),
    }
    return render(request,'User/client_dashboard.html',context)

@login_required(login_url='/client/login/')
@role_required(allowed_roles=['Blood Bank Manager','Client'],redirect_route='/')
def profile(request,pk): 
    if request.method == "POST":
        user = User.objects.get(id=pk)
        u_form = UserUpdateForm(request.POST,instance = user)
        p_form = UserProfileForm(request.POST,request.FILES,instance = user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,"Profile Info Updated Successfully!")
            return redirect('/user/profile/'+str(pk))
    
    user = User.objects.get(id=pk)
    u_form = UserUpdateForm(instance = user)
    p_form = UserProfileForm(instance = user.profile)

    # userrole = request.user_role
    # print("yesko role: ", userrole)
    # extendbase = ""
    # if userrole == "Client":
    #     extendbase = "{% extends 'User/client_dash_base.html' %}"
    # elif userrole == "Blood Bank Manager":
    #     extendbase = "{% extends 'Admin/admin_dash_base.html' %}"
    # else:
    #     extendbase = "Blood_Bank/base.html"
        
    context = {
        'u_form':u_form,
        'p_form':p_form,
        'user': user,
    }
    return render(request,'User/profile.html',context)



@login_required(login_url="/client/login/")
@role_required(allowed_roles=['Client'],redirect_route='/admin/admin-dash/')
def MakeRequest(request):
    if request.method == "POST":
        bloodrequestform = BloodRequestForm(request.POST,request.FILES)
        print(bloodrequestform.is_valid())
        if bloodrequestform.is_valid():
            bloodrequest = bloodrequestform.save(commit=False)
            bloodrequest.request_by_client = Profile.objects.get(user_id = request.user.id)
            bloodrequest.save()
            messages.success(request,"blood request successful")
            return redirect('/client/my-request/')
        else:
            print(bloodrequestform.errors)
            messages.error(request,"form is not valid")
            return HttpResponseRedirect('/client/make-request/')
        
    else:
        bloodrequestform = BloodRequestForm()
    return render(request,"User/makerequest.html",{"bloodrequestform":bloodrequestform})

@login_required(login_url="/client/login/")
@role_required(allowed_roles=['Client'],redirect_route='/admin/admin-dash/')
def MyRequest(request):
    client = Profile.objects.get(user_id=request.user.id)
    # blood_request = B_model.BloodRequest.objects.all()
    blood_request = B_model.BloodRequest.objects.filter(request_by_client=client)
    donation_request = B_model.DonationRequest.objects.filter(request_by_client=client)
    # print(blood_request)
    # print(blood_request)

    return render(request,"User/mybloodrequest.html",{'bloodrequest':blood_request,'donationrequest':donation_request})

@login_required(login_url="/client/login/")
@role_required(allowed_roles=['Client'],redirect_route='/admin/admin-dash/')
def Campaigns(request):
    donationform = DonationRequestForm()
    campaigns = Campaign.objects.all()
    return render(request,"User/donateblood.html",{"campaigns":campaigns})

@login_required(login_url="/client/login/")
@role_required(allowed_roles=['Client'],redirect_route='/admin/admin-dash/')
def DonateBlood(request,pk):
    if request.method=="POST":
        donationform = DonationRequestForm(request.POST,request.FILES)
        if donationform.is_valid():
            df = donationform.save(commit=False)
            df.campaignid = pk
            df.request_by_client = Profile.objects.get(user_id = request.user.id)
            df.save()
            messages.success(request,"Donation Request submitted successfully!")
            return redirect('/client/client-dash/')
        else:
            return HttpResponse("Not Valid")
    else:
            campaign = Campaign.objects.filter(id=pk)
            campaigns = Campaign.objects.all()
            donationform = DonationRequestForm()
    return render(request,"User/blooddonationpage.html",{"campaigns":campaigns,"donationform":donationform,"id":pk})

def view_stock(request):
    
    context= {
        'A1': str(Stock.objects.get(bloodgroup="A+").unit) + ' ML',
        'A2': str(Stock.objects.get(bloodgroup="A-").unit) + ' ML',
        'B1': str(Stock.objects.get(bloodgroup="B+").unit) + ' ML',
        'B2': str(Stock.objects.get(bloodgroup="B-").unit) + ' ML',
        'AB1': str(Stock.objects.get(bloodgroup="AB+").unit) + ' ML',
        'AB2': str(Stock.objects.get(bloodgroup="AB-").unit) + ' ML',
        'O1': str(Stock.objects.get(bloodgroup="O+").unit) + ' ML',
        'O2': str(Stock.objects.get(bloodgroup="O-").unit) + ' ML',
    }
    return render(request,"User/view_stock.html",context)
    

# ['DoesNotExist', 'EMAIL_FIELD', 'Meta', 'MultipleObjectsReturned', 'REQUIRED_FIELDS', 'USERNAME_FIELD', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_default_pk', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_expr_references', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_password', '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', 'check', 'check_password', 'clean', 'clean_fields', 'date_error_message', 'date_joined', 'delete', 'email', 'email_user', 'first_name', 'from_db', 'full_clean', 'get_all_permissions', 'get_deferred_fields', 'get_email_field_name', 'get_full_name', 'get_group_permissions', 'get_next_by_date_joined', 'get_previous_by_date_joined', 'get_session_auth_hash', 'get_short_name', 'get_user_permissions', 'get_username', 'groups', 'has_module_perms', 'has_perm', 'has_perms', 'has_usable_password', 'id', 
# 'is_active', 'is_anonymous', 'is_authenticated', 'is_staff', 'is_superuser', 'last_login', 'last_name', 'logentry_set', 'natural_key', 'normalize_username', 'objects', 'password', 'pk', 'prepare_database_save', 'profile', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'set_password', 'set_unusable_password', 'unique_error_message', 'user_permissions', 'username', 'username_validator', 'validate_unique']