from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.conf import settings
from django.db import models

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "date_of_birth", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")

    # Organize fields in the form
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("date_of_birth", "profile_photo")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active")}
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)

    class Profile(models.Model):
     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
     bio = models.TextField()

    def __str__(self):
        return f"{self.user.email}'s profile"