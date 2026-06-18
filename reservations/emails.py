from django.conf import settings
from django.core.mail import send_mail

from reservations.models import Reservation


def send_reservation_confirm_email(
    reservation: Reservation,
) -> None:
    """
    Send reservation confirmation email to the user.
    """

    user = reservation.user
    screening = reservation.screening

    if not user.email:
        return

    seats = reservation.reserved_seats.select_related("seat").all()

    seats_text = ", ".join(
        f"Rząd {reservation_seat.seat.row}, miejsce {reservation_seat.seat.number}"
        for reservation_seat in seats
    )

    subject = "Potwierdzenie rezerwacji"

    message = (
        f"Cześć {user.username}, \n\n"
        f"Twoja rezerwacja została utowrzona. \n\n"
        f"Film: {screening.movie.title}\n"
        f"Data: {screening.start_time:%d.%m.%Y}\n"
        f"Godzina: {screening.start_time:%H:%M}\n"
        f"Sala: {screening.hall.name}\n"
        f"Miejsca: {seats_text}\n"
        f"Koszt: {reservation.total_cost} zł\n\n"
        f"Dziękujemy za rezerwację!"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
