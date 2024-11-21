from django.contrib import admin
from .models import Author, Book, FavoriteBook, Genre

# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    search_fields = ('first_name', 'last_name', 'biography')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'display_genres')  # Используем метод display_genres
    list_filter = ('publication_date', 'genres')  # Фильтр по ManyToManyField
    search_fields = ('title', 'isbn')  # Поиск по названию и ISBN
    filter_horizontal = ('authors', 'genres')  # Удобное управление авторами и жанрами

    def display_genres(self, obj):
        """
        Метод для отображения жанров книги в админке.
        """
        return ", ".join([genre.name for genre in obj.genres.all()])
    display_genres.short_description = 'Genres'  # Название колонки для отображения жанров


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Показываем только название жанра
    search_fields = ('name',)  # Добавляем возможность поиска по имени жанра

@admin.register(FavoriteBook)
class FavoriteBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book')
    search_fields = ('user__username', 'book__title')