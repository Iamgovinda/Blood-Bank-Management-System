from urllib import response
from django.db import models
from django.contrib.auth.models import User
from User import models as U_models

from User.constants import BLOODGROUP_CHOICES,GENDER_CHOICES
# Create your models here.

class Stock(models.Model):
    bloodgroup=models.CharField(max_length=10)
    unit=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.bloodgroup
class BloodRequest(models.Model):
    request_by_client = models.ForeignKey(U_models.Profile,null=True,on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=30)
    patient_age = models.PositiveIntegerField()
    patient_gender = models.IntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    patient_bloodgroup = models.CharField(max_length=10, choices=BLOODGROUP_CHOICES)
    email = models.EmailField(max_length=100,null=True)
    mobile = models.CharField(default='+9779800000000',null=True,max_length=15)
    unit = models.PositiveIntegerField(default=0)
    medical_report = models.ImageField(default="blood-sample.jpg",upload_to='requistion_forms/')
    status=models.CharField(max_length=20,default="Pending")
    request_date=models.DateField(auto_now=True)
    response_message = models.CharField(max_length=1000,default="")
    response_date = models.DateTimeField(max_length=30,auto_now=True)

    def __str__(self):
        return self.patient_bloodgroup 



class DonationRequest(models.Model):
    request_by_client = models.ForeignKey(U_models.Profile,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100,null=True)
    mobile = models.CharField(default='+9779800000000',null=True,max_length=15)
    age = models.PositiveIntegerField()
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    bloodgroup = models.CharField(choices=BLOODGROUP_CHOICES,max_length=10)
    address = models.CharField(max_length=100,null=True)
    campaignid = models.IntegerField(default=0)
    request_date=models.DateField(auto_now=True)
    disease = models.CharField(max_length=200,default="No Diesease")
    status = models.CharField(max_length=20,default="Pending")
    response_message = models.CharField(max_length=200,default="")
    response_date = models.DateTimeField(auto_now=True)
    unit = models.PositiveIntegerField(default=0)
    def __str__(self) -> str:
        return self.bloodgroup




# Textual month, day and year	
# d2 = today.strftime("%B %d, %Y")
# print("d2 =", d2)