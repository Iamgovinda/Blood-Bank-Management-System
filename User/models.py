from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser,AbstractUser
from User.constants import GENDER_CHOICES,BLOODGROUP_CHOICES

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    # national_id = models.CharField(primary_key=True, unique=True,max_length=20)

    profile_pic= models.ImageField(upload_to='profile_pic/',null=True,blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES)

    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)


    age=models.PositiveIntegerField()
    bloodgroup=models.CharField(choices=BLOODGROUP_CHOICES,max_length=10)
    

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name

