from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

import random

from screenings.models import Screening, Hall
from movies.models import Movie



class Command(BaseCommand):
    help = "Generate screenings for the last missing day in 7-day repertoire"

    def handle(self, *args, **kwargs):
        now = timezone.now().date()
        target_date = now + timedelta(days=3)
        
        if Screening.objects.filter(
            start_time__date=target_date
        ).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"Seanse na {target_date} już istnieją. Nic nie generuję."
                )
            )
            return
        
        movies = list(Movie.objects.all())
        halls = list(Hall.objects.all())
        
        screenings_hours = (10, 13, 16, 19, 22)
        created_count = 0
        
        for _ in range(3):            
            random_movie = random.choice(movies)
            hall = random.choice(halls)
            hour = random.choice(screenings_hours)
                
            screening = Screening(
                movie=random_movie,
                hall=hall,
                start_time=timezone.make_aware(
                    timezone.datetime(
                        target_date.year,
                        target_date.month,
                        target_date.day,
                        hour,
                        0
                    )                        
                )
            )
                
            try:
                screening.full_clean()
                screening.save()
                created_count += 1
            except ValidationError:
                continue
                    
        self.stdout.write(
            self.style.SUCCESS(
                f"Utworzono {created_count} seansów na dzień {target_date}."
            )
        )