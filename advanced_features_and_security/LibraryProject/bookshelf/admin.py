from django.contrib import admin
from .models import Book

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    # Show these fields in the list view
    list_display = ('title', 'author', 'publication_year')

    # Add filters (sidebar)
    list_filter = ('publication_year', 'author')

    # Add a search bar
    search_fields = ('title', 'author')

   
    list_editable = ('author', 'publication_year')

    

# Register with custom configuration
admin.site.register(Book, BookAdmin)