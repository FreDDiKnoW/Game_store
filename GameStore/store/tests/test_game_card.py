import pytest
from django.urls import reverse
from rest_framework import status
from store.models import Game
from decimal import Decimal

pytestmark = pytest.mark.django_db


class TestGameApiRead:

    def test_get_game_list(self, api_client, game):
        url = reverse('game-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) >= 1
        assert response.json()[0]['title'] == game.title

    def test_get_game_detail(self, api_client, game):
        url = reverse('game-detail', args=[game.id])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['title'] == game.title

    def test_get_game_detail_not_found(self, api_client):
        url = reverse('game-detail', args=[999])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestGameApiWrite:

    @pytest.fixture
    def game_payload(self, developer, genre):
        return {
            'title': 'Cyberpunk 2077',
            'slug': 'cyberpunk-2077-test',
            'price': 29.99,
            'shortDescription': 'A futuristic RPG.',
            'platforms': 'PC, PS5',
            'developer': developer.id,
            'genres': [genre.id]
        }

    def test_create_game_admin(self, admin_client, game_payload):
        url = reverse('game-list')
        response = admin_client.post(url, data=game_payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['title'] == game_payload['title']
        assert Game.objects.filter(title=game_payload['title']).exists()

    def test_create_game_no_auth(self, api_client, game_payload):
        url = reverse('game-list')
        response = api_client.post(url, data=game_payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_game_auth_user(self, authenticated_client, game_payload):
        url = reverse('game-list')
        response = authenticated_client.post(url, data=game_payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_game_bad_data(self, admin_client, genre):
        url = reverse('game-list')
        payload = {
            'price': 10.00,
            'platforms': 'PC',
            'developer': 999,
            'genres': [genre.id]
        }
        response = admin_client.post(url, data=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_game_admin(self, admin_client, game):
        url = reverse('game-detail', args=[game.id])
        payload = {
            'title': 'The Witcher 3 - Updated',
            'slug': game.slug,
            'price': game.price,
            'shortDescription': 'An updated short description.',
            'platforms': game.platforms,
            'developer': game.developer.id,
            'genres': [g.id for g in game.genres.all()]
        }
        response = admin_client.put(url, data=payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['title'] == 'The Witcher 3 - Updated'
        assert response.json()['shortDescription'] == 'An updated short description.'
        game.refresh_from_db()
        assert game.title == 'The Witcher 3 - Updated'

    def test_partial_update_game_admin(self, admin_client, game):
        url = reverse('game-detail', args=[game.id])
        payload = {'price': 24.99}
        response = admin_client.patch(url, data=payload)

        assert response.status_code == status.HTTP_200_OK
        game.refresh_from_db()
        assert game.price == Decimal('24.99')

    def test_update_game_no_auth(self, api_client, game):
        url = reverse('game-detail', args=[game.id])
        payload = {
            'title': 'Hacked',
            'slug': game.slug,
            'price': game.price,
            'shortDescription': game.shortDescription,
            'platforms': game.platforms,
            'developer': game.developer.id,
            'genres': [g.id for g in game.genres.all()]
        }
        response = api_client.put(url, data=payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_game_auth_user(self, authenticated_client, game):
        url = reverse('game-detail', args=[game.id])
        payload = {
            'title': 'Hacked',
            'slug': game.slug,
            'price': game.price,
            'shortDescription': game.shortDescription,
            'platforms': game.platforms,
            'developer': game.developer.id,
            'genres': [g.id for g in game.genres.all()]
        }
        response = authenticated_client.put(url, data=payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_game_admin(self, admin_client, game):
        url = reverse('game-detail', args=[game.id])
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Game.objects.filter(id=game.id).exists()

    def test_delete_game_no_auth(self, api_client, game):
        url = reverse('game-detail', args=[game.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Game.objects.filter(id=game.id).exists()

    def test_delete_game_auth_user(self, authenticated_client, game):
        url = reverse('game-detail', args=[game.id])
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Game.objects.filter(id=game.id).exists()

    def test_delete_game_not_found(self, admin_client):
        url = reverse('game-detail', args=[999])
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
