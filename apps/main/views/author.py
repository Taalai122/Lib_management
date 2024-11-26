from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.main.serializers.author import AuthorSerializer, AuthorCreateUpdateSerializer
from apps.main.models import Author
from apps.main.filters import AuthorFilter


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AuthorFilter # Фильтры для авторов
    search_fields = ['first_name', 'last_name'] # Поиск по имени и фамилии
    ordering_fields = ['first_name', 'last_name', 'date_of_birth'] # Сортировка

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AuthorCreateUpdateSerializer # Для создания и обновления используем AuthorCreateUpdateSerializer
        return AuthorSerializer                 # Для получения данных используем AuthorSerializer
    

class AuthorUpdateView(generics.UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Получаем объект автора по id из url
        obj = super().get_object()
        return obj
    
class AuthorDeleteView(generics.DestroyAPIView):
    queryset = Author.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Получаем объект автора по id из url
        obj = super().get_object()
        return obj
