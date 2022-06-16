from django import forms
from Blood.models import BloodRequest,DonationRequest

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ("patient_name","patient_age","patient_gender","patient_bloodgroup","unit","medical_report","email","mobile")


class DonationRequestForm(forms.ModelForm):
    class Meta:
        model = DonationRequest
        fields = ("name","email","mobile","address","age","gender","bloodgroup","disease")

