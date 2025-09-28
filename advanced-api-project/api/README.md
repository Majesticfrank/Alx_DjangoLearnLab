# Book API (Django REST Framework)

This project demonstrates how to build CRUD operations for a **Book model** using Django REST Framework’s **generic class-based views**.

---

## Views Overview

### 1. **BookListView**

* **Purpose**: Retrieve a list of all books.
* **HTTP Method**: `GET`
* **Endpoint**: `/books/`
* **Implementation**: Extends `ListAPIView`.

### 2. **BookDetailView**

* **Purpose**: Retrieve details of a single book by ID.
* **HTTP Method**: `GET`
* **Endpoint**: `/books/<id>/`
* **Implementation**: Extends `RetrieveAPIView`.

### 3. **BookCreateView**

* **Purpose**: Add a new book.
* **HTTP Method**: `POST`
* **Endpoint**: `/books/create/`
* **Implementation**: Extends `CreateAPIView`.
* **Custom Hook**:

  * Uses `perform_create()` to prevent creating books with duplicate titles.
  * Raises a `ValidationError` if a book with the same title already exists.

### 4. **BookUpdateView**

* **Purpose**: Update an existing book.
* **HTTP Methods**: `PUT`, `PATCH`
* **Endpoint**: `/books/update/<id>/`
* **Implementation**: Extends `UpdateAPIView`.

### 5. **BookDeleteView**

* **Purpose**: Delete a book.
* **HTTP Method**: `DELETE`
* **Endpoint**: `/books/delete/<id>/`
* **Implementation**: Extends `DestroyAPIView`.

---

## Customizations

* **`perform_create()` Hook**:
  Added in `BookCreateView` to check if a book with the same `title` already exists before saving.
  This ensures **data integrity** and prevents duplicates.

---

## How to Test

* Use **Postman** or `curl` to interact with the endpoints.
* Example:

  ```bash
  # Create a new book
  curl -X POST http://127.0.0.1:8000/books/create/ \
       -H "Content-Type: application/json" \
       -d '{"title": "Django for Beginners", "author": "William", "published_date": "2024-01-01"}'
  ```
