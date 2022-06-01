from ctypes import create_string_buffer
from queue import PriorityQueue
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from User.decorators import role_required
from .forms import UserRegistrationForm,UserLoginForm,UserProfileForm,UserUpdateForm
from Blood.forms import BloodRequestForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group,User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from User import models as U_model
from Blood import models as B_model
from User.models import Profile
from Blood.models import BloodRequest
# from Blood.forms import BloodRequestForm

# Create your views here.
def UserRegistration(request):
    print("Inside")
    # if request.method=='POST':
    #     first_name=request.POST.get('firstName','default value')
    #     last_name=request.POST.get('lastName')
    #     username=request.POST.get('userName')
    #     password1=request.POST.get('password1')
    #     password2=request.POST.get('password2')
    #     email = request.POST.get('email')
    #     usergroup = Group.objects.get(name='Client')
       

    #     if password1==password2:
    #         if User.objects.filter(username=username).exists():
    #             messages.info(request,"Username Taken")
    #             return redirect('/client/registration/')
    #         elif User.objects.filter(email=email).exists():
    #             messages.info(request,"Email Taken")
    #             return redirect('/client/registration/')
    #         else:
    #             user=User.objects.create(username=username,email=email,first_name=first_name,last_name=last_name)
    #             user.set_password(password2)
    #             usergroup.user_set.add(user)
    #             user.save()
    #             print('user created')
    #             return redirect('/client/login')
                
    #     else:
    #         messages.info(request,"Password not matching")
    #         return redirect('/client/registration/')

    if request.method=='POST':
        clientform = UserRegistrationForm(request.POST)
        
        # usergroup = Group.objects.get(name='Client')
        if clientform.is_valid():
            data = clientform.cleaned_data
            if data['password1']==data['password2']:
                if User.objects.filter(username=data['username']).exists():
                    messages.info(request,"Username Taken")
                    return redirect('/client/registration/')
                elif User.objects.filter(email=data['email']).exists():
                    messages.info(request,"Email Taken")
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

    # if request.method=="POST":
    #     username=request.POST.get('username')
    #     password=request.POST.get('password')
    #     usergroup = Group.objects.get(name='Client')
    #     print(username)
    #     print(password)

    #     user=authenticate(username=username,password=password)
    #     print(user)

    #     if user is not None:
    #         if user.groups.filter(name=usergroup):
    #             login(request,user)
    #             return render(request,'Client/client-home.html')
    #         else:
    #             messages.info(request,"Invalid User Group")
    #             return redirect("/client/login/")   
    #         # login(request,user)
    #         # print(usergroup)
    #         # return HttpResponse('Logged in successfully')
            
    #     else:
    #         messages.info(request,'Invalid credentials')
    #         return redirect("/client/login/")
    # else:
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
                    return redirect(homepage)
                else:
                    messages.error(request,"Invalid User Group")
                    return redirect(redirecturl)
            else:
                messages.info(request,'Invalid Credential !!!')
                return redirect(redirecturl)
        else:
            messages.info(request,'Form not valid')
    else:
        clientloginform = UserLoginForm()
    return render(request, "User/user_login.html", {"cloginform":clientloginform})



def UserLogout(request):
    logout(request)
    return redirect('/')

@login_required(login_url="/client/login/")
def UserHome(request):
    return render(request,'User/client_dashboard.html')

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




def MakeRequest(request):
    if request.method == "POST":
        bloodrequestform = BloodRequestForm(request.POST)
        print(bloodrequestform.is_valid())
        if bloodrequestform.is_valid():
            bloodrequest = bloodrequestform.save(commit=False)
            bloodrequest.request_by_client = Profile.objects.get(user_id = request.user.id)
            bloodrequest.save()
            messages.success(request,"submit successful")
            return redirect('/client/my-request/')
        else:
            print(bloodrequestform.errors)
            messages.error(request,"form is not valid")
            return HttpResponseRedirect('/client/make-request/')
        
    else:
        bloodrequestform = BloodRequestForm()
    return render(request,"User/makerequest.html",{"bloodrequestform":bloodrequestform})


def MyRequest(request):
    client = Profile.objects.get(user_id=request.user.id)
    # blood_request = B_model.BloodRequest.objects.all()
    blood_request = B_model.BloodRequest.objects.filter(request_by_client=client)
    # print(blood_request)
    # print(blood_request)
    return render(request,"User/mybloodrequest.html",{'bloodrequest':blood_request})


['DoesNotExist', 'EMAIL_FIELD', 'Meta', 'MultipleObjectsReturned', 'REQUIRED_FIELDS', 'USERNAME_FIELD', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_default_pk', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_expr_references', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_password', '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', 'check', 'check_password', 'clean', 'clean_fields', 'date_error_message', 'date_joined', 'delete', 'email', 'email_user', 'first_name', 'from_db', 'full_clean', 'get_all_permissions', 'get_deferred_fields', 'get_email_field_name', 'get_full_name', 'get_group_permissions', 'get_next_by_date_joined', 'get_previous_by_date_joined', 'get_session_auth_hash', 'get_short_name', 'get_user_permissions', 'get_username', 'groups', 'has_module_perms', 'has_perm', 'has_perms', 'has_usable_password', 'id', 
'is_active', 'is_anonymous', 'is_authenticated', 'is_staff', 'is_superuser', 'last_login', 'last_name', 'logentry_set', 'natural_key', 'normalize_username', 'objects', 'password', 'pk', 'prepare_database_save', 'profile', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'set_password', 'set_unusable_password', 'unique_error_message', 'user_permissions', 'username', 'username_validator', 'validate_unique']