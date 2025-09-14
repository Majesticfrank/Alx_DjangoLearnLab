In [1]: from bookshelf.models import Book
In [8]: retrieved_book=Book.objects.get(id=2)

In [9]: retrieved_book.delete()
Out[9]: (1, {'bookshelf.Book': 1})


<!-- comment: successfully deleted -->