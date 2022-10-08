from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import BidUserCreationForm
from .models import BidUser,Rating

class SignUp(generic.CreateView):
    form_class = BidUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class ProfileDetailView(generic.DetailView):
    model=BidUser
    template_name='templates/user_profile_view.html'

class RateUser(generic.CreateView):
    model=Rating
    template_name='templates/rate_user.html'

    fields=[
        'rating',

    ]


class VerifyPhone(generic.CreateView):
    model=BidUser

    template_name='templates/verify_phone.html'

    fields=[
        'phone_verified',
    ]
