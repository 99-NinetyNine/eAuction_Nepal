from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .forms import BidUserCreationForm, BidUserChangeForm

from .models import BidUser

class BidUserAdmin(UserAdmin):
    add_form = BidUserCreationForm
    form = BidUserChangeForm
    list_display = ['email', 'username',]
    model = BidUser

admin.site.register(BidUser, BidUserAdmin)