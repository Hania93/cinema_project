from django.db import models


# Create your models here.
class Director(models.Model):
    tmdb_id = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=120)
    photo = models.ImageField(upload_to="directors/", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "directors"
        ordering = ["name"]


class Actor(models.Model):
    tmdb_id = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=120)
    photo = models.ImageField(upload_to="actors/", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "actors"
        ordering = ["name"]


class Genre(models.Model):
    tmdb_id = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=55, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "genres"


class Movie(models.Model):
    tmdb_id = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    poster = models.ImageField(upload_to="posters/", null=True, blank=True)
    trailer_url = models.URLField(blank=True, null=True)
    vote_average = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True
    )
    vote_count = models.PositiveIntegerField(null=True, blank=True)

    director = models.ForeignKey(
        Director, on_delete=models.CASCADE, related_name="movies"
    )

    genres = models.ManyToManyField(Genre, related_name="movies")

    actors = models.ManyToManyField(Actor, through="MovieActor", related_name="movies")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "movies"
        ordering = ["title"]


class MovieActor(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

    role_name = models.CharField(
        max_length=100,
        blank=True,
    )
    billing_order = models.PositiveIntegerField()

    class Meta:
        db_table = "movies_actors"

        constraints = [
            models.UniqueConstraint(
                fields=["movie", "actor"], name="unique_movie_actor"
            )
        ]

        indexes = [
            models.Index(fields=["movie"]),
            models.Index(fields=["actor"]),
        ]

        ordering = ["billing_order"]

    def __str__(self):
        return f"{self.actor} as {self.role_name}"
