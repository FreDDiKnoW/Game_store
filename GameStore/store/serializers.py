from rest_framework import serializers
from .models import Game, Developer, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ['id', 'name']


class GameListSerializer(serializers.ModelSerializer):
    developer = DeveloperSerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ['id', 'title', 'slug', 'shortDescription', 'price', 'currency',
                  'releaseDate', 'rating', 'developer', 'genres', 'image']


class GameCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['title', 'slug', 'shortDescription', 'fullDescription', 'price',
                  'currency', 'releaseDate', 'rating', 'platforms', 'developer', 'genres']


class GameDetailSerializer(serializers.ModelSerializer):
    developer = DeveloperSerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = '__all__'
