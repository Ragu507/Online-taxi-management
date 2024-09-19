from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import *

class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class PassengerProfileForm(forms.ModelForm):
    class Meta:
        model = PassengerProfile
        fields = ['preferred_payment_method'] 

class DriverProfileForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = ['license_number', 'vehicle_type', 'vehicle_model', 'vehicle_number', 'vehicle_image']
