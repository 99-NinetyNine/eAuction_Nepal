from django.contrib import admin
from .models import Auction,Notification,Bids,AuctionImage

admin.site.register(Auction)
admin.site.register(Bids)
admin.site.register(Notification)
admin.site.register(AuctionImage)

