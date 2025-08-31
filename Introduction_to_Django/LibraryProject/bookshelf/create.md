from bookshelf.models import Book 

In [2]: book= Book.objects.create(
   ...: title="1984",
   ...: author="George Orwell",
   ...: publication_year="1946"
   ...: )
In [3]: book
Out[3]: <Book: Book object (2)>

In [2]: Book.objects.all()
Out[2]: <QuerySet [<Book: 1984 by George Orwell in 1946>]>
<!--  Expected Output: A new `Book` instance is created successfully and displayed as <Book: 1984>
``` -->