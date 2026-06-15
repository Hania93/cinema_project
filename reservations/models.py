from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from screenings.models import Screening, Seat

User = get_user_model()

class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Oczekująca"),
        ("confirmed", "Potwierdzona"),
        ("cancelled", "Anulowana")
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    screening = models.ForeignKey(
        Screening,
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="confirmed"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_cost(self):
        return (
            self.reserved_seats.count() * self.screening.price
        )
    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.screening.movie.title}"
        )
        
class ReservationSeat(models.Model):
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="reserved_seats",
    )
    seat = models.ForeignKey(
        Seat,
        on_delete=models.PROTECT,
        related_name="reservations",
    )
    
    def clean(self):
        if self.seat.hall != self.reservation.screening.hall:
            raise ValidationError(
                "To miejsce nie należy do sali tego seansu."
            )
            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
    class Meta:
        ordering = ["reservation"]
        constraints = [
            models.UniqueConstraint(
                fields=["reservation", "seat"],
                name="unique_seat_per_reservation",
            )
        ]
        
    def __str__(self):
        return f"{self.reservation} - {self.seat}"