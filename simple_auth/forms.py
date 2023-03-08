from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


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
    

class SignUpForm(forms.Form):
    first_name      =   forms.CharField(max_length=50,label="Enter your first name")
    last_name       =   forms.CharField(max_length=50,label="Enter your last name")
    username        =   forms.CharField(max_length=50,label="Enter your username")
    password        =   forms.CharField(max_length=50,label="Enter your password")
    phone_num       =   forms.CharField(max_length=50,label="Enter your phone number")
    date_of_birth   =   forms.CharField(max_length=50,label="Enter your date of birth")

    
    def save(self):
        try:
            user=User.objects.create(
                first_name     =    self.cleaned_data.get("first_name"),
                last_name      =    self.cleaned_data.get("last_name"),
                username       =    self.cleaned_data.get("username"),
                password       =    self.cleaned_data.get("password"),
                phone_num      =    self.cleaned_data.get("phone_num"),
                date_of_birth  =    self.cleaned_data.get("date_of_birth"),
            )
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


class LogInForm(forms.Form):
    username        =   forms.CharField(max_length=50,label="Enter your username")
    password        =   forms.CharField(max_length=50,label="Enter your password")
    
    
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