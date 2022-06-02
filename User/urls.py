from django.urls import path, include
from . import views


urlpatterns = [
    path('registration/',views.UserRegistration,name='User_Registration'),
    path('login/',views.UserLogin,name='User_Login'),
    path('logout/',views.UserLogout,name="User_Logout"),
    path('client-dash/',views.UserHome,name="Client_Dashboard"),
    path('make-request/',views.MakeRequest, name="Make_Request"),
    path('my-request/',views.MyRequest,name="My_Requests"),
    path('donate-blood/',views.DonateBlood,name="DonateBlood")
    
]
