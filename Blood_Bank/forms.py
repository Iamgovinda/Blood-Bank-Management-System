from tkinter import Widget
from django import forms
from Blood_Bank.models import Campaign
from django.contrib.admin.widgets import AdminDateWidget,AdminTimeWidget

class CampaignForm(forms.ModelForm):
    # event_name=forms.CharField(max_length=20)
    # date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    # time=forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}))
    # location=forms.CharField(max_length=50)
    # contact=forms.IntegerField()
    class Meta:
        model = Campaign
        fields = ['event_name','date','time','location','contact']
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
            'time': forms.TimeInput(attrs={'type':'time'})
        }




