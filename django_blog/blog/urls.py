from django.urls import path
from django.contrib.auth import views as auth_views
from . import views




urlpatterns=[
    path("", views.home, name="home"),   # 👈 root URL
    path("register/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("profile/", views.profile_view, name="profile"),
    path("createblog/", views.CreatePostView.as_view(), name="CreateblogPost"),
    path("listpostview/", views.ListPostView.as_view(), name="listblogPost"),
    path("post-detail/<int:pk>/", views.DetailPostView.as_view(), name="post-detail"),
    path("update-post/<int:pk>/", views.UpdatePostView.as_view(), name="update-post" ),
    path("Delete-post/<int:pk>/", views.DeletePostView.as_view(), name="delete-post" ),

    path("logout/", views.logout_view, name="logout"),
]