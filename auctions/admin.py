from django.contrib import admin
from .models import Estate,Notification,Bids,EstateImage

admin.site.register(Estate)
admin.site.register(Bids)
admin.site.register(Notification)
admin.site.register(EstateImage)

