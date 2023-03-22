from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from simple_auth.forms import BidderCreationForm, BidderChangeForm

from .models import *

class BidUserAdmin(UserAdmin):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    add_form = BidderCreationForm
    form = BidderChangeForm
    list_display = ['email', 'username',"profile_pic","phone_num","is_inventory_incharge","is_admin_A","is_admin_B","is_admin_C", ]
    model = User
    list_editable = ("phone_num","is_inventory_incharge","is_admin_A","is_admin_B","is_admin_C", )
    
    

admin.site.register(User, BidUserAdmin)




@admin.action(description='Move selected to live')
def move_to_live(modeladmin, request, queryset):
    for auction in queryset:
        auction.move_to_live()

@admin.action(description='Move selected to admin waiting')
def move_to_admin_waiting(modeladmin, request, queryset):
    for auction in queryset:
        auction.move_to_admin_waiting()

@admin.action(description='Move selected to not settled')
def move_to_not_settled(modeladmin, request, queryset):
    for auction in queryset:
        auction.move_to_not_settled()

@admin.action(description='Move selected to settled')
def move_to_settled(modeladmin, request, queryset):
    for auction in queryset:
        auction.move_to_settled()

@admin.action(description='Move selected to re-schedule')
def move_to_reschedule(modeladmin, request, queryset):
    for auction in queryset:
        auction.move_to_reschedule()

class AuctionAdmin(admin.ModelAdmin):
    actions = [
        move_to_live,
        move_to_admin_waiting,
        move_to_not_settled,
        move_to_settled,
        move_to_reschedule,
    ]

admin.site.register(Auction, AuctionAdmin)






admin.site.register(LiveAuction)
admin.site.register(AdminWaitingAuction)
admin.site.register(NotSettledAuction)
admin.site.register(SettledAuction)
admin.site.register(RescheduleAuction)
admin.site.register(Bid)
admin.site.register(LiarBidder)