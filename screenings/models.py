from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models


class Hall(models.Model):
    name = models.CharField(max_length=50, unique=True)
    rows = models.PositiveSmallIntegerField()
    seats_per_row = models.PositiveSmallIntegerField()

    @property
    def total_seats(self):
        return self.rows * self.seats_per_row

    def __str__(self):
        return self.name

    class Meta:
        db_table = "halls"


class Seat(models.Model):
    hall = models.ForeignKey(
        Hall,
        on_delete=models.CASCADE,
        related_name="seats",
    )
    row = models.PositiveSmallIntegerField()
    number = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["hall", "row", "number"],
                name="unique_seat_per_hall",
            )
        ]

        db_table = "seats"

    def clean(self):
        if self.row < 1:
            raise ValidationError("Numer rzędu musi być większy od 0.")

        if self.number < 1:
            raise ValidationError("Numer miejsca musi być większy od 0.")

        if self.row > self.hall.rows:
            raise ValidationError("Numer rzędu jest większy niż liczba rzędów w sali.")

        if self.number > self.hall.seats_per_row:
            raise ValidationError(
                "Numer miejsca jest większy niż liczba miejsc w rzędzie."
            )

    def __str__(self):
        return f"{self.hall} - rząd {self.row}, miejsce {self.number}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Screening(models.Model):
    movie = models.ForeignKey(
        "movies.Movie",
        on_delete=models.CASCADE,
        related_name="screenings",
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(
        blank=True,
        editable=False,
    )

    hall = models.ForeignKey(
        Hall,
        on_delete=models.PROTECT,
        related_name="screenings",
    )
    
    price = models.DecimalField(
        max_digits=6, decimal_places=2, default=20.00
    ) 

    def set_end_time(self):
        if self.movie and self.start_time and self.movie.duration:
            self.end_time = self.start_time + timedelta(
            minutes=self.movie.duration,
            )

    def clean(self):
        self.set_end_time()
        
        if self.start_time is None or self.end_time is None:
            raise ValidationError(
                "Nie można ustalić czasu zakończenia seansu — sprawdź, czy film ma ustawiony czas trwania (duration).",
            )

        if self.end_time <= self.start_time:
            raise ValidationError(
                "Koniec seansu musi być późniejszy niż początek.",
            )

        overlapping_screenings = Screening.objects.filter(
            hall=self.hall,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        )

        if self.pk:
            overlapping_screenings = overlapping_screenings.exclude(pk=self.pk)

        if overlapping_screenings.exists():
            raise ValidationError(
                "W tej sali istnieje już seans w tym przedziale czasowym.",
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.movie.title} - {self.start_time}"

    class Meta:
        ordering = ["start_time"]
        db_table = "screenings"
