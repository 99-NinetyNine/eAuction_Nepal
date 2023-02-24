from django.contrib import admin
from mechanism.auction import Auction,AuctionImage
from mechanism.notification import Notification
from mechanism.bidding import Bid

admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Notification)
admin.site.register(AuctionImage)

