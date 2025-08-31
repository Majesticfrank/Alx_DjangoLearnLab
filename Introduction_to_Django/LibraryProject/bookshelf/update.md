 retrieved_book = Book.objects.get(id=2)

In [6]: retrieved_book.title ="Nineteen Eighty-Four"

In [7]: retrieved_book.save()

<!-- Successfully updated: {book.title} by {book.author}") -->