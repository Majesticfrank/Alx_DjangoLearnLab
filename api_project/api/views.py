from django.shortcuts import render

from rest_framework import generics, viewsets, permissions
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Book instances.
    Provides: list, create, retrieve, update, partial_update, and destroy.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
       permission_classes = [permissions.IsAuthenticated]  # only logged-in users