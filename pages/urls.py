from django.urls import path,include

from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    
    path('profile/',views.ProfileDetailView.as_view(),name='profile_view'),
    path('account/settings/',views.AccountSettingView.as_view(),name='account_settings'),
    path('change/profile/',views.ProfileEditView.as_view(),name='change_profile'),
    
    path('rate/user/',views.RateUser,name="rate_user"),
    path('verify/phone/',views.VerifyPhone.as_view(),name='verify_phone'),
    
    #contact
    path('contact/',views.contact_view,name='contact_view'),
    #search user
    path('search/',views.SearchUser.as_view(),name='search_user'),

    
    
]   