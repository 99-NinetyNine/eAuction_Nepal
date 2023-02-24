from django.urls import reverse_lazy
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


from django.contrib.auth import get_user_model
User=get_user_model()

from .forms import *
class SignUp(generic.CreateView):
    form_class = BidderCreationForm
    success_url = reverse_lazy('login')
    template_name = 'auth/signup.html'

# Create your views here.
from django.contrib.auth.views import LogoutView
class MyLogoutView(LogoutView):
    template_name = "auth/home.html"
    extra_context = {"form": "logout"}

