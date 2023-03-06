
from django.urls import path,include

from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="auth/home.html"),
        name="login",
    ),
    path("logout/", views.MyLogoutView.as_view(), name="logout",),
    

    #path('login')
    path('signup/', views.SignUp.as_view(), name='signup'),
]