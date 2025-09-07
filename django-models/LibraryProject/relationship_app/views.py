from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from .models import Library
from django.views.generic import DetailView

# Create your views here.
def book_list(request): 
    books = Book.objects.all()
    output = "<h1> Books</h1> <ul>"
    for book in books:
        output += f"<li>{book.title} by {book.author} </li>"
    output += "</ul>"
    return HttpResponse(output)

# Detailed view 
class LibraryDetailView(DetailView):
    model = Library
    template_name ="relationship_app/library_detail.html"
    context_object_name ="library"




