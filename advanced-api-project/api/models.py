from django.db import models

class Author(models.Model):
    name= models.CharField(max_length=225)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=255)  # Book’s title
    publication_year = models.IntegerField()  # Year of publication
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,   # If author is deleted, delete their books
        related_name="books"        # Access books via author.books.all()
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"