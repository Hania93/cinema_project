from django.contrib import admin
from .models import Director, Actor, Genre, Movie, MovieActor


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "director", "get_genres", "release_date")
    list_filter = ("genres", "release_date", "director")
    search_fields = ("title", "director__name")
    
    def get_genres(self, obj):
        return ", ".join(genre.name for genre in obj.genres.all())

    get_genres.short_description = "Genres"


@admin.register(MovieActor)
class MovieActorAdmin(admin.ModelAdmin):
    list_display = ("movie", "actor", "role_name", "billing_order")
    list_filter = ("movie",)
