from django.test import TestCase

from movies.models import Director, Genre, Movie


class MovieModelTests(TestCase):
    def test_movie_can_have_genres(self):
        director = Director.objects.create(
            name="Test Director",
        )

        movie = Movie.objects.create(
            title="Test Movie",
            director=director,
            duration=120,
        )

        genre = Genre.objects.create(
            name="Akcja",
        )

        movie.genres.add(genre)

        self.assertIn(
            genre,
            movie.genres.all(),
        )
