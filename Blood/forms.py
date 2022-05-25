from django import forms
from Blood.models import BloodRequest

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ("patient_name","patient_age","patient_gender","patient_bloodgroup","unit","Requisition_form","email","mobile")
