import django_filters
from django_filters import rest_framework as filters
from apps.main.models import FavoriteBook, Book, Author, Genre

class FavoriteBookFilter(filters.FilterSet):
    book_title = filters.CharFilter(field_name='book__title', lookup_expr='icontains')  # Поиск по названию книги
    book_genre = filters.CharFilter(field_name='book__genre', lookup_expr='icontains')  # Фильтрация по жанру книги

    class Meta:
        model = FavoriteBook
        fields = ['book_title', 'book_genre']

class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')     # Поиск по части названия
    genre = filters.CharFilter(lookup_expr='icontains')     # Фильтрация по жанру
    publication_date = filters.DateFromToRangeFilter()      # Диапазон дат публикации
    authors = filters.CharFilter(method='filter_authors')   # Фильтрация по авторам

    class Meta:
        model = Book
        fields = ['title', 'genre', 'publication_date', 'authors']

    
    def filter_authors(self, queryset, name, value):
        return queryset.filter(authors__last_name__icontains=value)

class AuthorFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')  # Поиск по имени
    last_name = django_filters.CharFilter(lookup_expr='icontains')  # Поиск по фамилии
    date_of_birth = django_filters.DateFilter(lookup_expr='exact')   # Фильтрация по точной дате

    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'date_of_birth']

class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    genre = filters.ModelChoiceFilter(queryset=Genre.objects.all())  # Фильтр по жанру
    publication_date = filters.DateFromToRangeFilter()

    class Meta:
        model = Book
        fields = ['title', 'genre', 'publication_date']