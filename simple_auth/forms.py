from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


from django.contrib.auth import get_user_model
User=get_user_model()

class BidderCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

class BidderChangeForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields
    