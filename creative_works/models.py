from django.db import models
from accounts import models as accounts_model

class Genre(models.Model):
    genre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.genre


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    uploader = models.ForeignKey(accounts_model.UserProfile, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    content = models.TextField()
    path = models.TextField()    

    def __str__(self):
        return self.title


class GenreBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('book', 'genre')

    def __str__(self):
        return f"{self.book.title} - {self.genre.genre}"