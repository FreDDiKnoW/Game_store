from django.urls import path
from . import views
urlpatterns = [
    path('developers/', views.DeveloperList.as_view(), name='developer-list'),
    path('developers/<int:pk>/', views.DeveloperDetail.as_view(), name='developer-detail'),

    path('genres/', views.GenreList.as_view(), name='genre-list'),

    path('games/', views.GameList.as_view(), name='game-list'),
    path('games/<int:pk>/', views.GameDetail.as_view(), name='game-detail'),
]
