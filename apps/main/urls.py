from rest_framework.routers import DefaultRouter
from rest_framework import permissions 
from apps.main.views.author import AuthorViewSet, AuthorUpdateView, AuthorDeleteView
from apps.main.views.book import BookViewSet, GenreViewSet, BookUpdateView, BookDeleteView
from apps.main.views.fav_book import FavoriteBookViewSet, FavoriteBookUpdateView, FavoriteBookDeleteView

from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



# Создаем роутер и регистрируем наши ViewSet
router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'books', BookViewSet, basename='book')
router.register(r'favorite-books', FavoriteBookViewSet, basename='favoritebook')
router.register(r'genres', GenreViewSet, basename='genre')

# Схема документации с использованием drf_yasg
schema_view = get_schema_view(
    openapi.Info(
        title="Library API",
        default_version='v1',
        description="API for managing books and authors",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="library@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

# Подключаем URL-ы, включая роутер для API и документацию Swagger
urlpatterns = [
    path('', include(router.urls)),  # Все API эндпоинты через роутер
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Документация Swagger
    # Роуты для редактирования и удаления книг
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),

    # Роуты для редактирования и удаления авторов
    path('authors/<int:pk>/update/', AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', AuthorDeleteView.as_view(), name='author-delete'),

    path('favorite-books/<int:pk>/update/', FavoriteBookUpdateView.as_view(), name='favoritebook-update'),
    path('favorite-books/<int:pk>/delete/', FavoriteBookDeleteView.as_view(), name='favoritebook-delete'),
    
]
