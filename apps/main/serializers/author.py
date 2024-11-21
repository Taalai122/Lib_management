from rest_framework import serializers
from apps.main.models import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 
                    'biography', 'date_of_birth', 'date_of_death']

class AuthorCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'biography', 'date_of_birth', 'date_of_death']
