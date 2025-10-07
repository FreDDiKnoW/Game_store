from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Developer(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):
    PLATFORM_CHOICES = [
        ('PC', 'PC'),
        ('PS5', 'PlayStation 5'),
        ('PS4', 'PlayStation 4'),
        ('XBOX', 'Xbox Series X/S'),
        ('SWITCH', 'Nintendo Switch'),
        ('MOBILE', 'Mobile'),
    ]

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    short_description = models.TextField(blank=True)
    full_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="USD")
    release_date = models.DateField(null=True, blank=True)
    rating = models.FloatField(default=0)
    developer = models.ForeignKey(Developer, on_delete=models.PROTECT, related_name="games")
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name="games")
    platforms = models.CharField(max_length=50, choices=PLATFORM_CHOICES, default='PC')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class UserGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_games")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="created_by_users")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'game']

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"