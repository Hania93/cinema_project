from django.core.management import call_command
from django.core.management.base import BaseCommand

from movies.models import Movie
from screenings.models import Screening
from reservations.models import Reservation


class Command(BaseCommand):
    help = "Set up demo data for deployed application"

    def handle(self, *args, **options):
        if Movie.objects.exists() and Screening.objects.exists():
            self.stdout.write(
                self.style.WARNING("Demo data already exists. Skipping setup.")
            )
            return

        self.stdout.write("Importing movies...")
        call_command("import_movies")

        self.stdout.write("Generating screenings...")
        call_command("seed_screenings")

        if not Reservation.objects.exists():
            self.stdout.write("Generating fake reservations...")
            call_command("seed_reservations")

        self.stdout.write(self.style.SUCCESS("Demo data setup completed."))
