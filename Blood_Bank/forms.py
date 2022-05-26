from django import forms
from Blood_Bank.models import Campaign
from django.contrib.admin.widgets import AdminDateWidget,AdminTimeWidget

class CampaignForm(forms.Form):
    event_name=forms.CharField(max_length=20)
    date=forms.DateField(widget=AdminDateWidget())
    time=forms.TimeField(widget=AdminTimeWidget())
    location=forms.CharField(max_length=50)
    contact=forms.IntegerField()




