from unicodedata import name
from django.urls import path,include
from Blood_Bank import views

urlpatterns = [
    path('login/',views.AdminLogin,name="admin_login"),
    path('admin-dash/',views.AdminDash,name="admin_dashboard"),
    path('blood-stock/',views.StockView,name="stock_view"),
    path('blood-update/',views.UpdateView,name="blood_update"),
    path('create-campaign/',views.CreateCampaign,name="Create_Campaign"),
    path('view-clients/',views.ViewClients,name="view_client"),
    path('view-bloodrequests/',views.ViewBloodRequests,name="view_blood_request"),
    path('view-donationrequests/',views.ViewDonationRequests,name="view_donation_request"),
    path('view-history/',views.ViewHistory,name="view_history"),
    path('add-blood/',views.AddBlood, name="add_blood"),
    path('give-blood/',views.GiveBloodExistingRequest,name="give_blood_e"),
    path('give-blood-new/',views.GiveBloodNewRequest,name="give_blood_n"), 
    path('edit-campaign/<int:pk>/',views.EditCampaign,name="edit_campaign"),
    path('delete-campaign/<int:pk>/',views.DeleteCampaign,name="delete_campaign"),
    path('update-client/<int:pk>/',views.UpdateClient,name="update_client"),
    path('delete-client/<int:pk>/',views.DeleteClient,name="delete_client"),
    path('approve-bloodrequest/<int:pk>',views.ApproveBloodRequest,name="approve_blood_request"),
    path('reject-bloodrequest/<int:pk>/',views.RejectBloodRequest,name="reject_blood_request"), 
    path('approve-donationrequest/<int:pk>',views.ApproveDonationRequest,name="approve_donation_request"),
    path('reject-donationrequest/<int:pk>/',views.RejectDonationRequest,name="reject_donation_request"),
    path('delete-donation-history/<int:pk>/',views.ManageDR,name="delete_dr"),
    path('delete-bloodrequest-history/<int:pk>/',views.ManageBR,name="delete_br"),
    path('send-mail-dr/<int:pk>/',views.SendMailDR,name="sendmail_dr"),
    path('delete-mail-br/<int:pk>/',views.SendMailBR,name="sendmail_br"),
]
