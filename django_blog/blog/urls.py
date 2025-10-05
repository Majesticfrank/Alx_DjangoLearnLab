from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CommentUpdateView, CommentDeleteView





urlpatterns=[
    path("", views.home, name="home"),   # 👈 root URL
    path("register/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("profile/", views.profile_view, name="profile"),
    path("post/new/", views.CreatePostView.as_view(), name="CreateblogPost"),
    path("listpostview/", views.ListPostView.as_view(), name="listblogPost"),

    path("post-detail/<int:pk>/", views.DetailPostView.as_view(), 
    name="post-detail"),

    path("post/<int:pk>/update/", views.UpdatePostView.as_view(), name="update-post" ),

    path("post/<int:pk>/delete/", views.DeletePostView.as_view(), 
  name="delete-post" ),
           # ✅ Comment routes
     path('post/<int:pk>/comments/new/', views.add_comment, name='add-comment'),


    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='edit-comment'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete-comment'),



    path("logout/", views.logout_view, name="logout"),
]