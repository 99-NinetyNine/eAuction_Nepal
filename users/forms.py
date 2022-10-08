from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import BidUser

class BidUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = BidUser
        fields = UserCreationForm.Meta.fields

class BidUserChangeForm(UserChangeForm):
    
    class Meta:
        model = BidUser
        fields = UserChangeForm.Meta.fields