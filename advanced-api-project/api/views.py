from rest_framework import generics, serializers, filters as drf_filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer
# from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters


# List all books (anyone can access)
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read for all, write requires login
    filter_backends = [filters.DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]

    # Filtering by specific fields
    filterset_fields = ['title', 'author__name', 'publication_year']

    # Searching (partial match)
    search_fields = ['title', 'author__name']

    # Ordering (sort results)
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering



# Retrieve one book by ID (anyone can access)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Create a new book (only authenticated users)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        title = serializer.validated_data.get("title")
        if Book.objects.filter(title=title).exists():
            raise serializers.ValidationError(
                {"title": "Book with this title already exists"}
            )
        serializer.save()


# Update an existing book (only authenticated users)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# Delete a book (only authenticated users)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]



# BookListView:
# - Supports filtering by title, author, and publication_year
# - Supports searching (partial matches) on title and author name
# - Supports ordering by title and publication_year
# Example queries:
#   /books/?search=Python
#   /books/?author__name=John Doe
#   /books/?ordering=-publication_year