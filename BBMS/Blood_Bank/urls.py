from django.urls import path,include
from Blood_Bank import views

urlpatterns = [
    path('login/',views.AdminLogin,name="admin_login"),
]
