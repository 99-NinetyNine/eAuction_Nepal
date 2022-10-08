from django.urls import path

from . import views
urlpatterns = [
    path('suggestions/', views.suggestion, name='suggestion'),
    path('explore/',views.explore,name='explore'),
   
    
]