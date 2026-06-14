from django.db import models
from django.contrib.auth import get_user_model
from screenings.models import Screening, Seat

User = get_user_model()

class Reservation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    screening = models.ForeignKey(
        Screening,
        on_delete=models.CASCADE,
        related_name="reserved_seats",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
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
    
    class Meta:        
        def __str__(self):
            return f"{self.reservation} - {self.seat}"