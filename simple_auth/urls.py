
from django.urls import path,include

from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm
urlpatterns = [
    path(
        "login/",
        views.ErrorLoginView.as_view(),name="login",
    ),
    path("logout/", views.MyLogoutView.as_view(), name="logout",),
    

    #path('login')
    path('signup/', views.signup_view, name='signup'),
]
