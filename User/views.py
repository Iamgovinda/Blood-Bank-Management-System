from ctypes import create_string_buffer
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

    context = {
        'u_form':u_form,
        'p_form':p_form,
        'user': user
    }

    return render(request,'User/profile.html',context)



    



def MakeRequest(request):
    if request.method == "POST":
        bloodrequestform = BloodRequestForm(request.POST)
        print(bloodrequestform.is_valid())
        if bloodrequestform.is_valid():
            bloodrequestform.save()
            messages.success(request,"submit successful")
            return redirect('/client/make-request/')
        else:
            print(bloodrequestform.errors)
            messages.error(request,"form is not valid")
            return HttpResponseRedirect('/client/make-request/')
        
    else:
        bloodrequestform = BloodRequestForm()
    return render(request,"User/makerequest.html",{"bloodrequestform":bloodrequestform})


def MyRequest(request):
    client = U_model.Profile.objects.get(user=request.user)
    print(client)
    # blood_request = B_model.BloodRequest.objects.all()
    blood_request = B_model.BloodRequest.objects.filter(request_by_client=client)
    # print(blood_request)
    # print(blood_request)
    return render(request,"User/mybloodrequest.html",{'bloodrequest':blood_request})