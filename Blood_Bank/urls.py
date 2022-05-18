from django.urls import path,include
from Blood_Bank import views

urlpatterns = [
    path('login/',views.AdminLogin,name="admin_login"),
    path('admin-dash/',views.AdminDash,name="admin_dashboard"),
    path('blood-stock/',views.StockView,name="stock_view"),
    path('blood-update/',views.UpdateView,name="blood_update"),
]
