from django.db import models


class Developer(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="USD")
    released_at = models.DateField(null=True, blank=True)
    rating = models.FloatField(default=0)
    developer = models.ForeignKey(Developer, on_delete=models.PROTECT, related_name="games")
    genres = models.ManyToManyField(Genre, blank=True, related_name="games")
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
