from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView

# Create your views here.
def book_list(request): 
    books = Book.objects.all()
    return render(
        request,
        "relationship_app/list_books.html",  # requirement: use this template
        {"books": books}
    )

# Detailed view 
class LibraryDetailView(DetailView):
    model = Library
    template_name ="relationship_app/library_detail.html"
    context_object_name ="library"




