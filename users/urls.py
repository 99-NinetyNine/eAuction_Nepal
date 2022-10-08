from django.urls import path

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/<slug:uuid>',views.ProfileDetailView.as_view(),name='profile_view'),
    path('rate/user/<uuid:pk>',views.RateUser,name="rate_user"),
    path('verify/phone/',views.VerifyPhone,name='verify_phone'),

]