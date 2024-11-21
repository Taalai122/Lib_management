from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import IsAuthenticated

from apps.main.models import Book, Genre
from apps.main.filters import BookFilter
from apps.main.serializers.book import BookSerializer, BookCreateUpdateSerializer, GenreSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter # Фильтры для книг
    search_fields = ['title', 'authors__last_name'] # Поиск по названию книги фамилии авторов
    ordering_fields = ['publication_date', 'title', 'genre'] # Сортировка

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BookCreateUpdateSerializer
        return BookSerializer
    
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Получаем объект книги по id из url
        obj = super().get_object()
        return obj
    
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Получаем объект книги по id из url
        obj = super().get_object()
        return obj
    
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    