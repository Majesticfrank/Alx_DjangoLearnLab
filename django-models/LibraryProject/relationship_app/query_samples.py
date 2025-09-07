import os 
import django
from django.apps import apps

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


# 1. Query all books
books = Book.objects.all()
for book in books:
    print(book.title, book.author)


# 2. Books by specific author 
author = Author.objects.get(name=author_name)
specific_author = Book.objects.filter(author=author)
for book in specific_author:
    print(book.title)


# 3. Books in Library
library = Library.objects.get(name=library_name)
for book in library.books.all():
    print(book.title)


# 4. Librarian of a library 
librarian = Librarian.objects.get(library)
librarian =library.librarian 
print(librarian.name)