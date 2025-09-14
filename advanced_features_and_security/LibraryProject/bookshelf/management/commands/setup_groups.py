from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps

class Command(BaseCommand):
    help = "Set up groups and assign custom permissions"

    def handle(self, *args, **kwargs):
        Book = apps.get_model("bookshelf", "Book")

        # Get permissions
        can_view = Permission.objects.get(codename="can_view", content_type__app_label="bookshelf")
        can_create = Permission.objects.get(codename="can_create", content_type__app_label="bookshelf")
        can_edit = Permission.objects.get(codename="can_edit", content_type__app_label="bookshelf")
        can_delete = Permission.objects.get(codename="can_delete", content_type__app_label="bookshelf")

        # Create groups
        viewers, _ = Group.objects.get_or_create(name="Viewers")
        editors, _ = Group.objects.get_or_create(name="Editors")
        admins, _ = Group.objects.get_or_create(name="Admins")

        # Assign permissions
        viewers.permissions.set([can_view])
        editors.permissions.set([can_view, can_create, can_edit])
        admins.permissions.set([can_view, can_create, can_edit, can_delete])

        self.stdout.write(self.style.SUCCESS("Groups and permissions created successfully!"))
