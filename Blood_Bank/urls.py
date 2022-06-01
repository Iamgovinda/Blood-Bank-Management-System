from django.urls import path,include
from Blood_Bank import views

urlpatterns = [
    path('login/',views.AdminLogin,name="admin_login"),
    path('admin-dash/',views.AdminDash,name="admin_dashboard"),
    path('blood-stock/',views.StockView,name="stock_view"),
    path('blood-update/',views.UpdateView,name="blood_update"),
    path('create-campaign/',views.CreateCampaign,name="Create_Campaign"),
    path('view-clients/',views.ViewClients,name="view_client"),
    path('edit-campaign/<int:pk>/',views.EditCampaign,name="edit_campaign"),
    path('delete-campaign/<int:pk>/',views.DeleteCampaign,name="delete_campaign"),
    path('update-client/<int:pk>/',views.UpdateClient,name="update_client"),
    path('delete-client/<int:pk>/',views.DeleteClient,name="delete_client"),
    
]
