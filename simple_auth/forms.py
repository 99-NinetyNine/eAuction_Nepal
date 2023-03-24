from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from datetime import date, datetime
from django.utils.timezone import is_aware

from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
User=get_user_model()

class BidderCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

class BidderChangeForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields
    
class AgeRestrictedDateField(forms.DateField):
    def validate(self, value):
        super().validate(value)
        if value:
            now = datetime.now()
            age = now.year - value.year - ((now.month, now.day) < (value.month, value.day))
            if age < 21:
                raise forms.ValidationError("You must be at least 21 years old.")
            if not is_aware(value):
                raise forms.ValidationError("Timezone must be aware.")

class SignUpForm(forms.Form):
    first_name              =   forms.CharField(max_length=50,label="Enter your first name")
    last_name               =   forms.CharField(max_length=50,label="Enter your last name")
    username                =   forms.CharField(max_length=50,label="Enter your username")
    email                   =   forms.EmailField(max_length=50,label="Enter your email")
    password                =   forms.CharField(max_length=50,label="Enter your password",widget=forms.PasswordInput)
    phone_num               =   forms.CharField(max_length=50,label="Enter your phone number")
    date_of_birth           =   AgeRestrictedDateField(label="Enter date of birth(Age must be greater than 21 years")
    citizenship_number      =   forms.CharField(max_length=100,label="Fill in your citizenship number")
    
    def clean(self):
        cleaned_data = super().clean()
        
        dob=cleaned_data.get("date_of_birth")
        citizenship=cleaned_data.get("citizenship_number")

        if age <21:
            raise ValidationError(f"Your age must be greater than 21 years to create account.")

    def save(self):
        try:
            user=User.objects.create(
                first_name              =    self.cleaned_data.get("first_name"),
                last_name               =    self.cleaned_data.get("last_name"),
                username                =    self.cleaned_data.get("username"),
                email                   =    self.cleaned_data.get("email"),
                phone_num               =    self.cleaned_data.get("phone_num"),
                date_of_birth           =    self.cleaned_data.get("date_of_birth"),
                citizenship_number      =    self.cleaned_data.get("citizenship_number")
            )
            user.set_password(self.cleaned_data.get("password"))
            user.save()
            return user
        except Exception as e:
            print(e)
        
        return False

    def get_err_msg(self):
        m=""
        for error_list in self.errors.values():
            for error in error_list:
                m+="\n"+error
        return m


class LoginForm(forms.Form):
    username        =   forms.CharField(max_length=50,label="Enter your username")
    password        =   forms.CharField(max_length=50,label="Enter your password",widget=forms.PasswordInput)
    
    
    def save(self):
        try:
            user=User.objects.get(username=self.cleaned_data["username"])
            
            return user
        
        except Exception as e:
            print(e)
        return False
    

    def get_err_msg(self):
        m=""
        for error_list in self.errors.values():
            for error in error_list:
                m+="\n"+error
        return m