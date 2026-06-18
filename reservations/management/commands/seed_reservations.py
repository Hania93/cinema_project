from faker import Faker
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import random

from reservations.models import Reservation, ReservationSeat
from screenings.models import Screening


User = get_user_model()


class Command(BaseCommand):
    help = "Seed fake users and reservations"

    def handle(self, *args, **kwargs):
        fake = Faker("pl_PL")

        self.stdout.write("Generowanie rezerwacji rozpoczęte...")

        users = self.create_users(fake)

        self.stdout.write(self.style.SUCCESS(f"Utworzono {len(users)} użytkowników"))

        users = list(User.objects.all())

        screenings = list(Screening.objects.all().select_related("movie", "hall"))

        if not screenings:
            self.stdout.write(self.style.ERROR("Brak seansów, najpierw utwórz seans"))
            return

        reservations = self.create_reservations(users, screenings)

        self.stdout.write(
            self.style.SUCCESS(f"Utworzono {len(reservations)} rezerwacji")
        )
        
    def create_users(
            self,
            fake: Faker,
            count: int = 10,
        ) -> list:
        """
        Create fake users.
        """
        
        users = []

        for _ in range(count):
            username = fake.unique.user_name()
            email = fake.unique.email()

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                },
            )

            if created:
                user.set_password("haslo1234")
                user.save()

            users.append(user)

        return users
    
    def create_reservations(
        self,
        users: list,
        screenings: list[Screening],
        count: int = 20,
    ) -> list[Reservation]:
        """
        Create fake reservations for screenings.
        """
        
        reservations = []
        statuses = ["confirmed", "confirmed", "confirmed", "pending", "cancelled"]

        for _ in range(count):

            screening = random.choice(screenings)
            user = random.choice(users)

            seats = list(screening.hall.seats.all())

            reserved_seats_ids = set(
                ReservationSeat.objects.filter(
                    reservation__screening=screening,
                    reservation__status__in=["confirmed", "pending"],
                ).values_list("seat_id", flat=True)
            )

            available_seats = [
                seat for seat in seats if seat.id not in reserved_seats_ids
            ]

            if not available_seats:
                continue

            seats_count = min(
                random.randint(1, 4),
                len(available_seats),
            )

            selected_seats = random.sample(available_seats, seats_count)

            status = random.choice(statuses)

            reservation = Reservation.objects.create(
                screening=screening,
                user=user,
                status=status,
            )

            if status != "cancelled":
                for seat in selected_seats:
                    ReservationSeat.objects.create(
                        reservation=reservation,
                        seat=seat,
                    )

            reservations.append(reservation)

        return reservations
