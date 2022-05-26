from django.contrib import admin
from Blood.models import Stock, BloodRequest
# Register your models here.
admin.site.register([Stock, BloodRequest])