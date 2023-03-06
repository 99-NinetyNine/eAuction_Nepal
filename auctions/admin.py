from django.contrib import admin
from mechanism.notification import Notification
from mechanism.bidding import Bid
from mechanism.auction import Auction
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Notification)
