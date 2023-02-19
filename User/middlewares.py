from django.contrib import messages
from django.http import HttpResponse
class UserRoleMiddleware:
    def __init__(self, get_response):  
        self.get_response = get_response  
      
    def __call__(self, request):  
        response = self.get_response(request)  
        return response  
    @staticmethod
    def process_view(request,view_func,view_args,view_kwargs):
        request.user_role = None
    
        if request and request.user and request.user.is_authenticated:
            groups = request.user.groups.all()
            if groups:
                request.user_role = groups[0].name
                if request.user_role == "Blood Bank Manager":
                    request.is_BBM = True
