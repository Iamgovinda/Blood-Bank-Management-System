from email import message
from xhtml2pdf import pisa
from django.views import View
from django.template.loader import get_template
from io import BytesIO
from tokenize import group
from traceback import print_tb
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import render, redirect
import random
from User.forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from Blood import models
from Blood.models import Stock
from User.decorators import role_required
from Blood_Bank.forms import CampaignForm
from django.contrib import messages
from User.models import Profile
from django.contrib.auth.models import User, Group
from User.forms import *
from Blood_Bank.models import Campaign
from Blood.models import BloodRequest, DonationRequest
from Blood.models import Stock
from datetime import datetime
from Blood.forms import DonationRequestForm,BloodRequestForm
from django.core.mail import send_mail
# Create your views here.


def home(request):
    quote = ["“Blood Donation Is A Great Act Of Kindness.”", "“Blood Donation Is A Small Act Of Kindness That Does Great And Big Wonders.”", "“Blood Donation Costs You Nothing, But It Can Mean The World To Someone In Need.”",
             "“Donate Blood Because You Never Know How Helpful It Might Be To Someone.”", "“Donate Blood So That You Can Say That You Have Served Mankind.”", " “Donate Blood For The Sake Of God’s Pleasure And For Mankind’s Welfare.”"]
    index = random.randint(0, 5)
    context = {"quote": quote[index]}
    return render(request, 'Blood_Bank/home.html', context)


def AdminLogin(request):
    if request.method == 'GET':
        admin_login = UserLoginForm()
        context = {'aloginform': admin_login}
        return render(request, 'Admin/admin_login.html', context)


@login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route="/client/client-dash/")
def AdminDash(request):
    # user = User.objects.get(id=2)
    # print(user.username)
    # print(type(user))
    # print(type(user.username))
    x = models.Stock.objects.all()
    print(x)
    if len(x) == 0:
        blood1 = models.Stock()
        blood1.bloodgroup = "A+"
        blood1.save()

        blood2 = models.Stock()
        blood2.bloodgroup = "A-"
        blood2.save()

        blood3 = models.Stock()
        blood3.bloodgroup = "B+"
        blood3.save()

        blood4 = models.Stock()
        blood4.bloodgroup = "B-"
        blood4.save()

        blood5 = models.Stock()
        blood5.bloodgroup = "AB+"
        blood5.save()

        blood6 = models.Stock()
        blood6.bloodgroup = "AB-"
        blood6.save()

        blood7 = models.Stock()
        blood7.bloodgroup = "O+"
        blood7.save()

        blood8 = models.Stock()
        blood8.bloodgroup = "O-"
        blood8.save()

    context = {
        'A1': str(models.Stock.objects.get(bloodgroup="A+").unit) + ' ML',
        'A2': str(models.Stock.objects.get(bloodgroup="A-").unit) + ' ML',
        'B1': str(models.Stock.objects.get(bloodgroup="B+").unit) + ' ML',
        'B2': str(models.Stock.objects.get(bloodgroup="B-").unit) + ' ML',
        'AB1': str(models.Stock.objects.get(bloodgroup="AB+").unit) + ' ML',
        'AB2': str(models.Stock.objects.get(bloodgroup="AB-").unit) + ' ML',
        'O1': str(models.Stock.objects.get(bloodgroup="O+").unit) + ' ML',
        'O2': str(models.Stock.objects.get(bloodgroup="O-").unit) + ' ML',
        'dr_total':DonationRequest.objects.all().count(),
        'dr_pending':DonationRequest.objects.all().filter(status="Pending").count(),
        'dr_approved':DonationRequest.objects.all().filter(status="Approved").count(),
        'dr_rejected':DonationRequest.objects.all().filter(status="Rejected").count(),
        'br_total':BloodRequest.objects.all().count(),
        'br_pending':BloodRequest.objects.all().filter(status="Pending").count(),
        'br_approved':BloodRequest.objects.all().filter(status="Approved").count(),
        'br_rejected':BloodRequest.objects.all().filter(status="Rejected").count()
    }
    return render(request, "Admin/admin_dashboard.html", context)


@login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route="/client/client-dash/")
def StockView(request):
    if request.method == "GET":
        blooddonationform = DonationRequestForm()
        bloodrequestform = BloodRequestForm()
        approveddonationrequests = DonationRequest.objects.filter(
            status="Approved")
        donors = []
        for donor in approveddonationrequests:
            donors.append(donor)
        approvedbloodrequests = BloodRequest.objects.filter(status="Approved")

        patients = []
        for patient in approvedbloodrequests:
            patients.append(patient)

        context = {
            'A1': str(models.Stock.objects.get(bloodgroup="A+").unit) + ' ML',
            'A2': str(models.Stock.objects.get(bloodgroup="A-").unit) + ' ML',
            'B1': str(models.Stock.objects.get(bloodgroup="B+").unit) + ' ML',
            'B2': str(models.Stock.objects.get(bloodgroup="B-").unit) + ' ML',
            'AB1': str(models.Stock.objects.get(bloodgroup="AB+").unit) + ' ML',
            'AB2': str(models.Stock.objects.get(bloodgroup="AB-").unit) + ' ML',
            'O1': str(models.Stock.objects.get(bloodgroup="O+").unit) + ' ML',
            'O2': str(models.Stock.objects.get(bloodgroup="O-").unit) + ' ML',
            'donors': donors,
            'patients':patients,
            'donationform': blooddonationform,
            'bloodrequestform':bloodrequestform
        }
        return render(request, "Admin/blood_stock.html", context)

    if request.method == "POST":
        donoridd = request.POST.get("donorid")
        if donoridd == "SELECTED":
            messages.error(request,"Please select donor first.")
            return redirect('/admin/blood-stock/')
        unit = request.POST.get("bunit")
        donation = DonationRequest.objects.get(id=donoridd)
        donation.unit = unit
        donation.status = "Donated"
        stock = Stock.objects.get(bloodgroup=donation.bloodgroup)
        stock.unit = int(stock.unit) + int(unit)
        donation.save()
        stock.save()
        messages.info(request,"Blood added successfully")
        return redirect('/admin/blood-stock/')


@login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route="/client/client-dash/")
def UpdateView(request):
    if request.method == "POST":
        bloodgroup = request.POST.get('bloodgroup')
        unit = request.POST.get('unit')
        blood = Stock.objects.get(bloodgroup=bloodgroup)
        blood.unit = unit
        blood.save()
        messages.success(request,f"Stock updated successfully")
        return redirect('/admin/blood-stock/')


@login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route="/client/client-dash/")
def CreateCampaign(request):
    campaigns = Campaign.objects.all()
    if request.method == "POST":
        campaignform = CampaignForm(request.POST)
        if campaignform.is_valid():
            campaignform.save()
            messages.success(request,f"Campaign created successfully")
            return redirect('Create_Campaign')
        else:
            messages.error(request, "Form is not valid")
            return redirect('Create_Campaign')
    else:
        campaignform = CampaignForm()
        print(campaignform)
    return render(request, 'Admin/create_campaign.html', {'campaignform': campaignform, 'campaigns': campaigns})


@login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route="/client/client-dash/")
def ViewClients(request):
    # usergroup = Group.objects.get(name='Client')
    # client = User.groups.filter(name=usergroup)
    clients = []
    userprofiles = Profile.objects.all()
    for profile in userprofiles:
        if profile.user.groups.filter(name='Client'):
            clients.append(profile)

    return render(request, "Admin/viewclient.html", {'client': clients})


@login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route="/client/client-dash/")
def UpdateClient(request, pk):
    if request.method == "POST":
        user = User.objects.get(id=pk)
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = UserProfileForm(
            request.POST, request.FILES, instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile Info Updated Successfully!")
            return redirect('/admin/update-client/'+str(pk))

    user = User.objects.get(id=pk)
    u_form = UserUpdateForm(instance=user)
    p_form = UserProfileForm(instance=user.profile)

    if request.user_role == "Client":
        extendbase = "User/client_dash_base.html"
    else:
        extendbase = "Admin/admin_dash_base.html"

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user': user,
        'extendbase': extendbase
    }

    return render(request, 'Admin/updateclient.html', context)


@login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route="/client/client-dash/")
def DeleteClient(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    messages.info(request,f"Client deleted successfully")
    return redirect('/admin/view-clients/')


@login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route="/client/client-dash/")
def DeleteCampaign(request, pk):
    Campaign.objects.filter(id=pk).delete()
    messages.info(request,f"Campaign deleted successfully")
    return redirect('/admin/create-campaign/')


@login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route="/client/client-dash/")
def EditCampaign(request, pk):
    campaign = Campaign.objects.get(id=pk)
    campaigns = Campaign.objects.all()
    if request.method == "POST":
        campaignform = CampaignForm(request.POST, instance=campaign)
        print("Here")
        if campaignform.is_valid():
            campaignform.save()
            return redirect('/admin/create-campaign/')
        else:
            return HttpResponse('Form not valid')
    else:
        campaignform = CampaignForm(instance=campaign)
    return render(request, "Admin/edit_campaign.html", {'campaignform': campaignform, 'campaigns': campaigns, 'id': pk})


@login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route="/client/client-dash/")
def ViewBloodRequests(request):
    bloodrequests = BloodRequest.objects.all()
    stock = Stock.objects.all()
    context = {"bloodrequests": bloodrequests, "stock": stock}
    return render(request, "Admin/view-blood-request.html", context)


@login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route="/client/client-dash/")
def ApproveBloodRequest(request, pk):
    br = BloodRequest.objects.get(id=pk)
    bloodgroup = br.patient_bloodgroup
    requestedbloodunit = br.unit
    stockblood = Stock.objects.get(bloodgroup=bloodgroup)
    stockbloodunit = stockblood.unit

    if stockbloodunit > requestedbloodunit:
        # stockblood.unit = stockbloodunit-requestedbloodunit
        br.status = "Approved"
        br.response_date = datetime.now()
        print(br.status)
        stockblood.save()
        br.save()
    else:
        messages.error(request,"Stock has no enough blood.")
        return redirect('/admin/view-bloodrequests/')
    return redirect("/admin/view-bloodrequests/")


@login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route="/client/client-dash/")
def RejectBloodRequest(request, pk):
    if request.method == "POST":
        br = BloodRequest.objects.get(id=pk)
        br.status = "Rejected"
        br.response_message = request.POST.get('RejectionMessage')
        br.response_date = datetime.now()
        br.save()
        return redirect("/admin/view-bloodrequests/")


@login_required(login_url='admin_login')
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route="/client/client-dash/")
def ViewHistory(request):
    bloodrequests = BloodRequest.objects.exclude(status='Pending')
    donationrequests = DonationRequest.objects.exclude(status='Pending')
    context = {"bloodrequests": bloodrequests,
               "donationrequests": donationrequests}
    return render(request, "Admin/view_history.html", context)

@login_required(login_url="/admin/login/")
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route='/admin/admin-dash/')
def ManageDR(request,pk):
    if request.method=="GET":
        dr = DonationRequest.objects.get(id=pk)
        dr.delete()
        messages.success(request,'Donation Request Deleted Successfully!')
        return redirect('/admin/view-history/')

@login_required(login_url="/admin/login/")
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route='/admin/admin-dash/')
def ManageBR(request,pk):
    if request.method=="GET":
        BloodRequest.objects.filter(id=pk).delete()
        return redirect('/admin/view-history/')

@login_required(login_url="/admin/login/")
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route='/admin/admin-dash/')
def SendMailDR(request,pk):
    if request.method=="GET":
        dr = DonationRequest.objects.get(id=pk)
        cp = Campaign.objects.get(id=dr.campaignid)
        donor = dr.name
        cpname = cp.event_name
        Location = cp.location
        Date = cp.date
        Time = cp.time
        contact = cp.contact
        if dr.status == "Approved":
            subjects = "Your donation request has been approved!!!"
            msgs = f"""
                Hello {donor},

                The donation request you have made is approved. We have added you as pre-registered donor in our system.
                Please, visit at the following location on the following date & time.

                Campaign: {cpname}
                Location: {Location}
                Date : {Date}
                Time : {Time}

                if you have any queries please contact us on {contact}.
                """
        elif dr.status == "Rejected":
            subjects = "Your donation request has been Rejected!!!"
            message = dr.response_message
            msgs = f"""
                Hello {donor},

                This is to notify you that the donation request you have made is rejected because, {message}!

                if you have any queries please contact us on hamrobbms.com.
                """
        elif dr.status == "Donated":
            subjects = "Appreciation for the blood donation"
            msgs = f"""
                Hello {donor},

                We really appreciate your work. We are really very thankful for the donation you have made.
                You can download the apreciation certificate from your account.

                if you have any queries please contact us on hamrobbms.com.
                """
        
        else:
            return redirect('/admin/view-history/')
        send_mail(subjects,
        msgs,
        'hamrobbms@gmail.com',
        (dr.email,),
        fail_silently=False
        )
        messages.success(request,"Email sent successfully")
        return redirect('/admin/view-history/')

@login_required(login_url="/admin/login/")
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route='/admin/admin-dash/')
def SendMailBR(request,pk):
    if request.method=="GET":
        br = BloodRequest.objects.get(id=pk)
        patient = br.patient_name
        if br.status == "Approved":
            subjects = "Your blood request has been approved!!!"
            msgs = f"""
                Hello {patient},

                The blood request you have made is approved. We have added you as pre-registered patient in our system.
                Please, visit at the following visit our bloodbank with the copy of approval of bloodrequest.

                if you have any queries please contact us on hamrobbms.com.
                """
        elif br.status == "Rejected":
            subjects = "Your blood request has been Rejected!!!"
            message = br.response_message
            msgs = f"""
                Hello {patient},

                This is to notify you that the blood request you have made is rejected because, {message}!

                if you have any queries please contact us on hamrobbms.com.
                """
        elif br.status == "Given":
            subjects = "Appreciation for the blood donation"
            msgs = f"""
                Hello {patient},
                
                You have recieved {br.unit} ML of {br.patient_bloodgroup} blood. 
                Thank you for giving us opportunity to help you!

                if you have any queries please contact us on hamrobbms.com.
                """
        
        else:
            return redirect('/admin/view-history/')
        send_mail(subjects,
        msgs,
        'hamrobbms@gmail.com',
        (br.email,),
        fail_silently=False
        )
        messages.success(request,"Email sent successfully")
        return redirect('/admin/view-history/')


@login_required(login_url="/admin/login/")
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route='/admin/admin-dash/')
def ViewDonationRequests(request):
    donationrequests = DonationRequest.objects.all()
    stock = Stock.objects.all()
    context = {"donationrequests": donationrequests, "stock": stock}
    return render(request, "Admin/view-donation-request.html", context)

@login_required(login_url="/admin/login/")
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route='/admin/admin-dash/')
def ApproveDonationRequest(request, pk):
    dr = DonationRequest.objects.get(id=pk)
    dr.status = "Approved"
    dr.save()
    return redirect("/admin/view-donationrequests/")

@login_required(login_url="/admin/login/")
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route='/admin/admin-dash/')
def RejectDonationRequest(request, pk):
    if request.method == "POST":
        dr = DonationRequest.objects.get(id=pk)
        dr.response_message = request.POST.get('RejectionMessage')
        dr.response_date = datetime.now()
        dr.status = "Rejected"
        dr.save()
        return redirect('/admin/view-donationrequests')
    return redirect('/admin/view-donationrequests')


@login_required(login_url="/admin/login/")
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route='/admin/admin-dash/')
def AddBlood(request):
    if request.method == "POST":
        donationform = DonationRequestForm(request.POST)
        if donationform.is_valid():
            df = donationform.save(commit=False)
            bloodgroup = request.POST.get('bloodgroup')
            unit = request.POST.get('unit')
            stock = Stock.objects.get(bloodgroup=bloodgroup)
            stock.unit = int(stock.unit) + int(unit)
            stock.save()
            print(bloodgroup)
            df.campaignid = 0
            df.request_by_client = Profile.objects.get(user_id=request.user.id)
            df.unit = request.POST.get('unit')
            df.status = "Donated"
            df.save()
            return redirect('/admin/blood-stock/')
        else:
            return HttpResponse("Not Valid")
    else:
        return redirect('/admin/blood-stock/')

@login_required(login_url="/admin/login/")
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route='/admin/admin-dash/')
def GiveBloodExistingRequest(request):
    if request.method == "POST":
        patientidd = request.POST.get("patientid")
        if patientidd == "SELECTED":
            messages.error(request,"Please select the patient first.")
            return redirect('/admin/blood-stock/')
        unit = request.POST.get("bunit")
        blood = BloodRequest.objects.get(id=patientidd)
        blood.unit = unit
        blood.status = "Given"
        stock = Stock.objects.get(bloodgroup=blood.patient_bloodgroup)
        stock.unit = int(stock.unit) - int(unit)
        blood.save()
        stock.save()
        return redirect('/admin/blood-stock/')

@login_required(login_url="/admin/login/")
@role_required(allowed_roles=['Blood Bank Manager'], redirect_route='/admin/admin-dash/')
def GiveBloodNewRequest(request):
    if request.method == "POST":
        bloodform = BloodRequestForm(request.POST)
        if bloodform.is_valid():
            df = bloodform.save(commit=False)
            bloodgroup = request.POST.get('patient_bloodgroup')
            unit = request.POST.get('unit')
            stock = Stock.objects.get(bloodgroup=bloodgroup)
            if int(stock.unit)>int(unit):
                stock.unit = int(stock.unit) - int(unit)
                stock.save()
            else:
                return HttpResponse("Stock Has No enough Blood")
            df.request_by_client = Profile.objects.get(user_id=request.user.id)
            df.unit = unit
            df.status = "Given"
            df.save()
            return redirect('/admin/blood-stock/')
        else:
            return HttpResponse("Not Valid")
    else:
        return redirect('/admin/blood-stock/')




# provide the certificate section


# provide the certificate section


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode()), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


# Opens up page as PDF

@login_required(login_url="/admin/login/")
@role_required(allowed_roles=['Blood Bank Manager',"Client"], redirect_route='/admin/admin-dash/')
def ViewCertificate(request, pk, *args, **kwargs):
    donationrequest = DonationRequest.objects.get(id=pk)
    data = {"name":donationrequest.name,"unit":donationrequest.unit,"bg":donationrequest.bloodgroup}
    pdf = render_to_pdf('Admin/certificate.html', data)
    return HttpResponse(pdf, content_type='application/pdf')
# Opens up page as PDF


@login_required(login_url="/admin/login/")
@role_required(allowed_roles=['Blood Bank Manager',"Client"], redirect_route='/admin/admin-dash/')
def ViewApproval(request, pk, *args, **kwargs):
    bloodrequest = BloodRequest.objects.get(id=pk)
    data = {"name":bloodrequest.patient_name,"unit":bloodrequest.unit,"bg":bloodrequest.patient_bloodgroup}
    pdf = render_to_pdf('Admin/approval.html', data)
    return HttpResponse(pdf, content_type='application/pdf')