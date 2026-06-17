# reservations/tests/test_models.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse

from movies.models import Movie, Director
from screenings.models import Hall, Seat, Screening
from reservations.models import Reservation, ReservationSeat


User = get_user_model()


class ReservationModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )

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
            rows=2,
            seats_per_row=5,
        )

        self.seat1 = Seat.objects.create(
            hall=self.hall,
            row=1,
            number=1,
        )

        self.seat2 = Seat.objects.create(
            hall=self.hall,
            row=1,
            number=2,
        )

        self.screening = Screening.objects.create(
            movie=self.movie,
            hall=self.hall,
            start_time=timezone.now() + timezone.timedelta(days=1),
            price=25,
        )

    def test_reservation_total_cost(self):
        reservation = Reservation.objects.create(
            user=self.user,
            screening=self.screening,
        )

        ReservationSeat.objects.create(
            reservation=reservation,
            seat=self.seat1,
        )

        ReservationSeat.objects.create(
            reservation=reservation,
            seat=self.seat2,
        )

        self.assertEqual(
            reservation.total_cost,
            50,
        )
    
    def test_cannot_reserve_seat_from_different_hall(self):
        other_hall = Hall.objects.create(
            name="Sala 2",
            rows=2,
            seats_per_row=5,
        )

        seat_from_other_hall = Seat.objects.create(
            hall=other_hall,
            row=1,
            number=1,
        )

        reservation = Reservation.objects.create(
            user=self.user,
            screening=self.screening,
        )

        reservation_seat = ReservationSeat(
            reservation=reservation,
            seat=seat_from_other_hall,
        )

        with self.assertRaises(ValidationError):
            reservation_seat.full_clean()
            
    def test_user_reservations_view_shows_only_logged_user_reservations(self):
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpass123",
        )

        my_reservation = Reservation.objects.create(
            user=self.user,
            screening=self.screening,
        )

        other_reservation = Reservation.objects.create(
            user=other_user,
            screening=self.screening,
        )

        self.client.login(
            username="testuser",
            password="testpass123",
        )

        response = self.client.get(
            reverse("user-reservations")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            my_reservation.screening.movie.title,
        )
        self.assertNotContains(
            response,
            other_user.username,
        )
        
    def test_cancel_reservation(self):
        reservation = Reservation.objects.create(
            user=self.user,
            screening=self.screening,
            status="confirmed",
        )

        self.client.login(
            username="testuser",
            password="testpass123",
        )

        self.client.post(
            reverse(
                "reservation-cancel",
                kwargs={"pk": reservation.pk},
            )
        )

        reservation.refresh_from_db()

        self.assertEqual(
            reservation.status,
            "cancelled",
        )