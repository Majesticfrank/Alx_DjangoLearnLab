from django.urls import path 
from .views import list_books, LibraryDetailView
from . import views
from django.contrib.auth import views as auth_views


urlpatterns =[
    path("", views.index, name="index"),
    path("books/", list_books, name="list_books"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library-detail"),
    path("register/", views.register_view, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="relationship_app/login.html"),
        name="login"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="relationship_app/logout.html"),
        name="logout"
    ),

    path("admin-view/", views.admin_view, name="admin_view"),
    path("librarian-view/", views.librarian_view, name="librarian_view"),
    path("member-view/", views.member_view, name="member_view"),
    # path("books/", views.book_list, name="book_list"),
    path("add_book/", views.add_book, name="add_book"),
    path("edit_book/<int:pk>/", views.edit_book, name="edit_book"),
    path("books/<int:pk>/delete/", views.delete_book, name="delete_book"),
]
