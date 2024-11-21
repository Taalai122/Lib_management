from rest_framework import viewsets, permissions
from apps.main.models import FavoriteBook
from apps.main.serializers.fav_book import FavoriteBookSerializer

from django_filters.rest_framework import DjangoFilterBackend
from apps.main.filters import FavoriteBookFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import DestroyAPIView, UpdateAPIView

class FavoriteBookViewSet(viewsets.ModelViewSet):
    queryset = FavoriteBook.objects.all()
    serializer_class = FavoriteBookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FavoriteBookFilter # Подключаем фильтры
    search_fields = ['book__title'] # Поиск по названию книги
    ordering_fields = ['book__title', 'book__genre'] # Сортировка по названию и жанру


    def get_queryset(self):
        # Возвращаем только избранные книги текущего пользователя
        queryset = self.queryset.filter(user=self.request.user)

        # Используем select_related для оптимизации запросов
        queryset = queryset.select_related('book')

        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        # Сохранение текущего пользователя
        # Метод perform_create корректно устанавливает текущего пользователя при создании записи. 
        # Это нужно, так как пользователь передается через request.user, а не через тело запроса.

class FavoriteBookUpdateView(UpdateAPIView):
    queryset = FavoriteBook.objects.all()
    serializer_class = FavoriteBookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Возвращаем только те записи, которые принадлежат текущему пользователю
        return self.queryset.filter(user=self.request.user)

    def perform_update(self, serializer):
        # Дополнительные действия перед сохранением, если нужно
        serializer.save(user=self.request.user)
    
class FavoriteBookDeleteView(DestroyAPIView):
    queryset = FavoriteBook.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Мы возвращаем только те записи, которые принадлежат текущему пользователю
        return self.queryset.filter(user=self.request.user)