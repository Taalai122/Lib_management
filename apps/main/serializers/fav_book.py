from rest_framework import serializers
from apps.main.models import FavoriteBook


class FavoriteBookSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = FavoriteBook
        fields = ['id', 'user', 'book_title']
        read_only_fields = ['user'] # Пользователь задается автоматически
