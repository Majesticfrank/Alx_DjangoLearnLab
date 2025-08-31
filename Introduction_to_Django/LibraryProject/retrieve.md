 from bookshelf.models import Book

In [2]: retrieved_book = Book.objects.get(id=2)
In [4]: print(retrieved_book.title, retrieved_book.author)
1984 George Orwell
<!-- comment:Successfully retrieved: 1984 by George Orwell -->