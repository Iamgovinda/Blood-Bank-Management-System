from ctypes import create_string_buffer
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserRegistrationForm,UserLoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group,User
from django.contrib import messages

# Create your views here.
def UserRegistration(request):
    print("Inside")
    cregform=UserRegistrationForm()
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
        print(clientform.is_valid())
        usergroup = Group.objects.get(name='Client')
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
                    client = User.objects.create(username=data['username'],email=data['email'],first_name=data['first_name'],last_name=data['last_name'])
                    client.set_password(data['password1'])
                    usergroup.user_set.add(client)
                    client.save()
                    messages.success(request,"User created")
                    return redirect('/client/login')
            else:
                messages.info(request,"Password not matching")
                return redirect('/client/registration/')
    return render(request,'User/user_registration.html',{"cregform":cregform})


def UserLogin(request):
    clientloginform = UserLoginForm()
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
            homepage = 'User/client_dashboard.html'
            redirecturl = "/client/login/"
        else:
            usergroup = Group.objects.get(name='Blood Bank Manager')
            homepage = 'Admin/admin_home.html'
            redirecturl = "/admin/login/"

        
        print(clientform.is_valid())
        if clientform.is_valid():
            print(clientform.is_valid())
            data = clientform.cleaned_data
            client = authenticate(username=data['username'],password=data['password'])
            print(client)
            if client is not None:
                if client.groups.filter(name=usergroup):
                    login(request,client)
                    return render(request,homepage)
                else:
                    messages.info(request,"Invalid User Group")
                    return redirect(redirecturl)
            else:
                messages.info(request,'Invalid credentials')
                return redirect(redirecturl)
        else:
            messages.info(request,'Form not valid')
    return render(request, "User/user_login.html", {"cloginform":clientloginform})



def UserLogout(request):
    logout(request)
    return redirect('/')