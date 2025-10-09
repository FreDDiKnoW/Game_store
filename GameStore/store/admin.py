from django.contrib import admin
from .models import User, Developer, Genre, Game

admin.site.register(Developer)
admin.site.register(Genre)
admin.site.register(Game)
