from django.contrib import admin
from .models import Place,Estate,Notification,Bids

admin.site.register(Estate)
admin.site.register(Bids)
admin.site.register(Notification)
admin.site.register(Place)

