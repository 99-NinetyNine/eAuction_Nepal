from django.urls import path,include

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    #path('logi')
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/<uuid:pk>',views.ProfileDetailView.as_view(),name='profile_view'),
    path('account/settings/',views.AccountSettingView.as_view(),name='account_settings'),
    path('change/profile/',views.ProfileEditView.as_view(),name='change_profile'),
    
    path('rate/user/',views.RateUser,name="rate_user"),
    path('verify/phone/',views.VerifyPhone.as_view(),name='verify_phone'),
    path('search/',views.SearchUser.as_view(),name='search_user'),

]