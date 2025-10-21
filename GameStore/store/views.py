from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import ProtectedError
from rest_framework.permissions import IsAdminUser, AllowAny

from .models import Game, Developer, Genre
from .serializers import (
    GameListSerializer,
    GameDetailSerializer,
    GameCreateUpdateSerializer,
    DeveloperSerializer,
    GenreSerializer
)


class DeveloperList(APIView):

    def get(self, request):
        developers = Developer.objects.all()
        serializer = DeveloperSerializer(developers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DeveloperSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeveloperDetail(APIView):
    def get(self, request, pk):
        developer = get_object_or_404(Developer, pk=pk)
        serializer = DeveloperSerializer(developer)
        return Response(serializer.data)

    def put(self, request, pk):
        developer = get_object_or_404(Developer, pk=pk)
        serializer = DeveloperSerializer(developer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        developer = get_object_or_404(Developer, pk=pk)
        try:
            developer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response(
                {"error": "Cannot delete developer with associated games."},
                status=status.HTTP_400_BAD_REQUEST
            )


class GenreList(APIView):
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameList(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request):
        games = Game.objects.all()
        serializer = GameListSerializer(games, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GameCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            detail_serializer = GameDetailSerializer(serializer.instance)
            return Response(detail_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameDetail(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        serializer = GameDetailSerializer(game)
        return Response(serializer.data)

    def put(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        serializer = GameCreateUpdateSerializer(game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            detail_serializer = GameDetailSerializer(serializer.instance)
            return Response(detail_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        serializer = GameCreateUpdateSerializer(game, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            detail_serializer = GameDetailSerializer(serializer.instance)
            return Response(detail_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
