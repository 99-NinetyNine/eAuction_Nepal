from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from simple_auth.forms import BidderCreationForm, BidderChangeForm

from .models import (
    User,
    Rating,
)

class BidUserAdmin(UserAdmin):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    add_form = BidderCreationForm
    form = BidderChangeForm
    #list_display = ['email', 'username',]
    model = User

admin.site.register(User, BidUserAdmin)
admin.site.register(Rating)