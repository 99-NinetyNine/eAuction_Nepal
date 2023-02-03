from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .forms import BidUserCreationForm, BidUserChangeForm

from .models import (
    BidUser,
    Rating,
)

class BidUserAdmin(UserAdmin):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    add_form = BidUserCreationForm
    form = BidUserChangeForm
    #list_display = ['email', 'username',]
    model = BidUser

admin.site.register(BidUser, BidUserAdmin)
admin.site.register(Rating)