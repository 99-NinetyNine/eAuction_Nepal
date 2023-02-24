from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('a/',include('auctions.urls')),
    path('admin/', admin.site.urls),    
    path('ai/',include('ai.urls')),
    path('auth/',include('simple_auth.urls')), 
    
    path('b/',include('bidding.urls')),
    path('n/',include('notification.urls')),
    path('p/',include('pages.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
