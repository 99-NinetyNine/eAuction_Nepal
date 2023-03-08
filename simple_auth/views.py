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

from django.http import Http404, HttpResponseRedirect
from django.views.generic import (
    View,
)

from django.contrib.auth import get_user_model,authenticate
User=get_user_model()


from django.contrib.auth import login as auth_login

from .forms import *

from django.contrib.auth import views as auth_views
class ErrorLoginView(auth_views.LoginView):
    template_name = "auth/login.html"
    extra_context = {"login_form": LoginForm()}


class SignUp(View):
    def get(self,*args,**kwargs):
        return render(self.request,"auth/signup.html",{"signup_form":SignUpForm()})
    def post(self,*args,**kwargs):
        form=SignUpForm(self.request.POST)
        if(form.is_valid()):
            user=form.save()
            if(user):
                messages.add_message(self.request, messages.SUCCESS, "Signup successful.")
                auth_login(self.request,user,'django.contrib.auth.backends.ModelBackend')
                return HttpResponseRedirect(reverse("login"))
            else:
                messages.add_message(self.request, messages.SUCCESS, "Signup failed.")
                return HttpResponseRedirect(reverse("signup"))
        
        error=form.get_err_msg()
        messages.add_message(self.request,  messages.ERROR, error)
        return HttpResponseRedirect(reverse("signup"))
signup_view=SignUp.as_view()


class SimpleLogin(View):
    def get(self,*args,**kwargs):
        return render(self.request,"auth/login.html",{"login_form":LoginForm()})
    
    def post(self,*args,**kwargs):
        
        form=LoginForm(self.request.POST)
        if(form.is_valid()):
            user=form.save()
            if(not user):
                messages.add_message(self.request,  messages.ERROR, "User not found.")
                return HttpResponseRedirect(reverse("login"))
            
            some_return_value=authenticate(username=user.username,password=form.cleaned_data["password"])
            print("asasa",some_return_value)
            if(some_return_value is False):
                messages.add_message(self.request, messages.SUCCESS, "Login Failed.")
                return HttpResponseRedirect(reverse("login"))
        
            else:
                if(user.is_authenticated is False):
                    print("login err")
                
                messages.add_message(self.request, messages.SUCCESS, "Login successful.")
                return HttpResponseRedirect(reverse("home"))
        
        error=form.get_err_msg()
        messages.add_message(self.request,  messages.ERROR, error)
        return HttpResponseRedirect(reverse("login"))

login_view=SimpleLogin.as_view()
# Create your views here.
from django.contrib.auth.views import LogoutView
class MyLogoutView(LogoutView):
    template_name = "auth/home.html"
    extra_context = {"form": "logout"}

