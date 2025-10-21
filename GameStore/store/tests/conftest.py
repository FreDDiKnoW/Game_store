import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
# ВАЖЛИВО: імпортуй всі три моделі
from store.models import Game, Developer, Genre

User = get_user_model()


@pytest.fixture(scope='function')
def api_client():
    yield APIClient()


@pytest.fixture(scope='function')
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='testuser',
        password='testpassword'
    )


@pytest.fixture(scope='function')
def admin_user(django_user_model):
    return django_user_model.objects.create_superuser(
        username='adminuser',
        password='adminpassword'
    )


@pytest.fixture(scope='function')
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture(scope='function')
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture(scope='function')
def developer(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        dev, _ = Developer.objects.get_or_create(name='Test Developer')
        yield dev


@pytest.fixture(scope='function')
def genre(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        gen, _ = Genre.objects.get_or_create(name='RPG')
        yield gen


@pytest.fixture(scope='function')
def game(django_db_setup, django_db_blocker, developer, genre):
    with django_db_blocker.unblock():
        g, created = Game.objects.get_or_create(
            slug='the-witcher-3-test-game',
            defaults={
                'title': 'The Witcher 3',
                'price': 19.99,
                'shortDescription': 'A classic RPG.',
                'platforms': 'PC, PS4, Xbox One',
                'developer': developer,
            }
        )
        if created:
            g.genres.set([genre])

        yield g