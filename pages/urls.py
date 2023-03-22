from django.urls import path,include

from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    
    ##bidder profile
    path('profile/',views.ProfileDetailView.as_view(),name='profile_view'),
    
    ##my bids
    path('my/bids',views.MyBidsListView.as_view(),name='my_bids'),
    ## my resechiel auction
    path('to/reschedule',views.ToRescheduleListView.as_view(),name='to_reschedule'),

    path('change/profile/',views.ProfileEditView.as_view(),name='change_profile'),
    
    path('rate/user/',views.RateUser,name="rate_user"),
    path('verify/phone/',views.VerifyPhone.as_view(),name='verify_phone'),
    
    #contact
    path('contact/',views.contact_view,name='contact_view'),
    #search user
    path('search/',views.SearchUser.as_view(),name='search_user'),


    
    
]   