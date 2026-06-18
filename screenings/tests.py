from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from movies.models import Director, Movie
from screenings.models import Hall, Screening


class ScreeningModelTests(TestCase):
    def setUp(self):
        self.director = Director.objects.create(
            name="Test Director",
        )

        self.movie = Movie.objects.create(
            title="Test Movie",
            director=self.director,
            duration=120,
        )

        self.hall = Hall.objects.create(
            name="Sala 1",
            rows=5,
            seats_per_row=10,
        )

    def test_screening_cannot_overlap_in_same_hall(self):
        start_time = timezone.now() + timezone.timedelta(days=1)

        Screening.objects.create(
            movie=self.movie,
            hall=self.hall,
            start_time=start_time,
        )

        overlapping_screening = Screening(
            movie=self.movie,
            hall=self.hall,
            start_time=start_time + timezone.timedelta(minutes=30),
        )

        with self.assertRaises(ValidationError):
            overlapping_screening.full_clean()
