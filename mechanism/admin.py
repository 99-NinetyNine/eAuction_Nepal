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
    list_display = ['email', 'username',"profile_pic","phone_num","is_inventory_incharge","is_admin_A","is_admin_B","is_admin_C", ]
    model = User
    list_editable = ("phone_num","is_inventory_incharge","is_admin_A","is_admin_B","is_admin_C", )
    
    

admin.site.register(User, BidUserAdmin)
admin.site.register(Rating)