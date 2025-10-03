from django.urls import path
from django.contrib.auth import views as auth_views
from . import views




urlpatterns=[
    path("", views.home, name="home"),   # 👈 root URL
    path("register/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("profile/", views.profile_view, name="profile"),
    path("logout/", views.logout_view, name="logout"),
]