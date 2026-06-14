from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta
import random

from screenings.models import Hall, Seat, Screening
from movies.models import Movie


class Command(BaseCommand):
    help = "Seed halls, seats and screenings"

    def handle(self, *args, **options):
        self.create_halls()
        self.create_seats()
        self.create_screenings()

    def create_halls(self):
        for i in range(1, 6):
            hall, created = Hall.objects.get_or_create(
                name=f"Sala {i}",
                defaults={
                    "rows": random.randint(6, 10),
                    "seats_per_row": random.randint(8, 14),
                },
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Utworzono salę: {hall.name}"))

    def create_seats(self):
        halls = Hall.objects.all()

        for hall in halls:
            for row in range(1, hall.rows + 1):
                for number in range(1, hall.seats_per_row + 1):
                    Seat.objects.get_or_create(hall=hall, row=row, number=number)
            self.stdout.write(
                self.style.SUCCESS(f"Utworzono miejsca dla sali: {hall.name}")
            )

    def create_screenings(self):
        movies = list(Movie.objects.all())
        halls = list(Hall.objects.all())

        if not movies:
            self.stdout.write(
                self.style.ERROR("Brak filmów. Najpierw zaimportuj filmy.")
            )
            return

        if not halls:
            self.stdout.write(self.style.ERROR("Brak sal."))
            return

        attempts = 0
        created_count = 0

        today = timezone.localdate()
        start_hours = (10, 12, 14, 16, 18, 20, 22)

        while created_count < 30 and attempts < 300:
            attempts += 1

            rand_movie = random.choice(movies)
            rand_hall = random.choice(halls)

            rand_day = today + timedelta(days=random.randint(0, 6))

            rand_hour = random.choice(start_hours)

            start_time = timezone.make_aware(
                timezone.datetime(
                    rand_day.year, rand_day.month, rand_day.day, rand_hour, 0
                )
            )

            rand_screening = Screening(
                hall=rand_hall, movie=rand_movie, start_time=start_time
            )

            try:
                rand_screening.full_clean()
                rand_screening.save()
            except ValidationError:
                continue

            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Utworzono seanse: {created_count}"))
