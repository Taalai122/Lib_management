from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    biography = models.TextField()
    date_of_birth = models.DateField()
    date_of_death = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    isbn = models.CharField(max_length=13, unique=True) # International Standard Book Number (ISBN)
    authors = models.ManyToManyField(Author, related_name='books')
    publication_date = models.DateField()
    genres = models.ManyToManyField('Genre', related_name='books')  # Связь с несколькими жанрами

    def __str__(self):
        return self.title
    
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
        

class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        unique_together = ('user', 'book')  # Пользователь может добавить одну книгу только один раз

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"