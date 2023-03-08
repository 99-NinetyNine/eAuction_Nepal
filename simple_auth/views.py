from django.urls import reverse_lazy,reverse
from django.views import generic
from django.template.loader import render_to_string
from django.shortcuts import (
    get_object_or_404,
    render,
)
from django.http import(
        HttpResponse,
        JsonResponse,
) 
from django.contrib import messages


from django.views.generic import (
    View,
)

from django.contrib.auth import get_user_model,authenticate
User=get_user_model()


from django.contrib.auth import login as auth_login

from .forms import *
class SignUp(View):
    def get(self,*args,**kwargs):
        return render(self.request,"auth/signup.html",{"signup_form":SignUpForm()})
    def post(self,*args,**kwargs):
        form=SignUpForm(self.request.POST)
        if(form.is_valid()):
            user=form.save()
            messages.add_message(self.request, messages.SUCCESS, "Signup successful.")
            auth_login(self.request,user)
            return reverse("home")
        
        error=form.get_err_msg()
        messages.add_message(self.request,  messages.ERROR, error)
        return reverse("signup")



class SimpleLogin(View):
    def get(self,*args,**kwargs):
        return render(self.request,"auth/login.html",{"login_form":LoginForm()})
    
    def post(self,*args,**kwargs):
        
        form=LoginForm(self.request.POST)
        if(form.is_valid()):
            user=form.save()
            if(not user):
                messages.add_message(self.request,  messages.ERROR, "User not found.")
                return reverse("login")
            
            if(authenticate(self.request,user,form.cleaned_data["password"])):
                messages.add_message(self.request, messages.SUCCESS, "Login successful.")
                return reverse("home")
            else:
                messages.add_message(self.request, messages.SUCCESS, "Login Failed.")
                return reverse("home")
        
        error=form.get_err_msg()
        messages.add_message(self.request,  messages.ERROR, error)
        return reverse("signup")

# Create your views here.
from django.contrib.auth.views import LogoutView
class MyLogoutView(LogoutView):
    template_name = "auth/home.html"
    extra_context = {"form": "logout"}

