from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from rest_framework import status

from apps.main.models import Book, Author, Genre


# Create your tests here.

class BookAPITestCase(APITestCase):
    
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Получаем токен для этого пользователя
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        # Устанавливаем заголовок с токеном для клиента
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Создаем авторов
        author1 = Author.objects.create(first_name='Author', last_name='One', biography='Some bio', date_of_birth='1980-01-01')
        author2 = Author.objects.create(first_name='Author', last_name='Two', biography='Another bio', date_of_birth='1975-01-01')

        # Создаем жанры
        genre1 = Genre.objects.create(name="Fiction")
        genre2 = Genre.objects.create(name="Drama")

        # Создаем книгу с жанрами и авторами
        self.book = Book.objects.create(
            title="Book 1", 
            summary="Summary 1", 
            isbn="123456789", 
            publication_date=date(2020, 1, 1)
        )
        self.book.authors.add(author1, author2)
        self.book.genres.add(genre1, genre2)

    def test_get_books(self):
        url = reverse('book-list')  # Замените на имя вашего эндпоинта
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book 1')

    def test_create_book(self):
        url = reverse('book-list')  # Замените на имя вашего эндпоинта
        genre = Genre.objects.create(name="Adventure")  # Создайте жанр перед созданием книги

        data = {
            'title': 'New Book',
            'summary': 'New summary',
            'isbn': '987654321',
            'publication_date': '2024-01-01',
            'genres': [genre.id],  # Передаем список жанров
            'authors': [1],  # Предполагаем, что автор с ID 1 существует
        }

        response = self.client.post(url, data, format='json')  # Отправляем POST-запрос

        # Проверяем, что ответ успешный
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)  # Убедимся, что книга создана


class BookUpdateTestCase(APITestCase):
    def setUp(self):
        # Создаем авторов
        author1 = Author.objects.create(name="Author 1")
        author2 = Author.objects.create(name="Author 2")
        
        # Создаем книгу
        self.book = Book.objects.create(
            title="Test Book",
            description="Test Description",
            publish_date="2024-11-01"
        )
        
        # Назначаем авторов через set()
        self.book.authors.set([author1, author2])  # Используем метод set() для связи ManyToMany
        self.book.save()