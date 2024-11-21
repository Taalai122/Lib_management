from rest_framework import serializers
from apps.main.models import Book, Author, Genre

class BookSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True)  # Для отображения имен авторов
    genres = serializers.StringRelatedField(many=True)  # Для отображения имен жанров

    class Meta:
        model = Book
        fields = ['id', 'title', 'summary', 'isbn', 'authors', 'publication_date', 'genres']

class BookCreateUpdateSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Book
        fields = ['title', 'summary', 'isbn', 'authors', 'publication_date', 'genres']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']