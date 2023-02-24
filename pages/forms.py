from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from mechanism.models import (
    Rating,
)

    
class RatingForm(forms.ModelForm):
    class Meta:
        model=Rating
        fields=[
            "rating",
        ]
        labels={
            "rating":"Your rating : "
        }
