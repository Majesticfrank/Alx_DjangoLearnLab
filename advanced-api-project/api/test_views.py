from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Unit tests for the Book API endpoints.
    Tests CRUD operations, permissions, filtering, search, and ordering.
    """

    def setUp(self):
        # Create a user for authentication tests
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        # Create sample authors and books
        self.author1 = Author.objects.create(name="Chinua Achebe")
        self.author2 = Author.objects.create(name="Wole Soyinka")

        self.book1 = Book.objects.create(title="Things Fall Apart", publication_year=1958, author=self.author1)
        self.book2 = Book.objects.create(title="The Man Died", publication_year=1972, author=self.author2)

        # URLs
        self.list_url = reverse("book-list")
        self.detail_url = reverse("book-detail", args=[self.book1.id])
        self.create_url = reverse("book-create")
        self.update_url = reverse("book-update", args=[self.book1.id])
        self.delete_url = reverse("book-delete", args=[self.book2.id])

    # ---------- LIST & DETAIL ----------
    def test_list_books(self):
        """Ensure we can list all books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_retrieve_book_detail(self):
        """Ensure we can get a single book by ID"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    # ---------- CREATE ----------
    def test_create_book_unauthenticated(self):
        """Unauthenticated users should not be able to create books"""
        data = {"title": "Arrow of God", "publication_year": 1964, "author": self.author1.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        """Authenticated users should be able to create a book"""
        self.client.login(username="testuser", password="testpass123")
        data = {"title": "Arrow of God", "publication_year": 1964, "author": self.author1.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    # ---------- UPDATE ----------
    def test_update_book_authenticated(self):
        """Authenticated users can update an existing book"""
        self.client.login(username="testuser", password="testpass123")
        data = {"title": "Things Fall Apart - Revised", "publication_year": 1958, "author": self.author1.id}
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Things Fall Apart - Revised")

    # ---------- DELETE ----------
    def test_delete_book_authenticated(self):
        """Authenticated users can delete a book"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    # ---------- FILTERING, SEARCH, ORDERING ----------
    def test_filter_books_by_author(self):
        """Test filtering books by author"""
        response = self.client.get(self.list_url, {"author__name": "Chinua Achebe"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Things Fall Apart")

    def test_search_books_by_title(self):
        """Test searching books by title"""
        response = self.client.get(self.list_url, {"search": "Things"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Things Fall Apart")

    def test_order_books_by_publication_year(self):
        """Test ordering books by publication_year"""
        response = self.client.get(self.list_url, {"ordering": "publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, sorted(years))
