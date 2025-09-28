from django.shortcuts import render
from rest_framework import generics, permissions, serializers
from .models import Book
from .serializers import BookSerializer
# Create your views here.
# 📖 ListView → Retrieve all books
class BookListView(generics.ListAPIView):
    """
    Retrieve a list of all books.
    Accessible to everyone (no login required).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# 📖 DetailView → Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieve details of a single book by ID.
    Accessible to everyone (no login required).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# ➕ CreateView → Add a new book
class BookCreateView(generics.CreateAPIView):
    """
    Create a new book.
    Only authenticated users can add.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # ✅ Prevent duplicate titles
    def perform_create(self, serializer):
        title = serializer.validated_data.get("title")
        if Book.objects.filter(title=title).exists():
            raise serializers.ValidationError({"title": "Book with this title already exists"})
        serializer.save()


# ✏️ UpdateView → Modify an existing book
class BookUpdateView(generics.UpdateAPIView):
    """
    Update an existing book.
    Only authenticated users can update.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# ❌ DeleteView → Remove a book
class BookDeleteView(generics.DestroyAPIView):
    """
    Delete a book.
    Only authenticated users can delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]