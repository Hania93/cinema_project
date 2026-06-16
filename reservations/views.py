from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.views.generic import ListView

from .models import Reservation


class UserReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "reservations/user_reservation_list.html"
    context_object_name = "reservations"

    def get_queryset(self):
        return (
            Reservation.objects.filter(user=self.request.user)
            .select_related("screening", "screening__movie", "screening__hall")
            .prefetch_related(
                "reserved_seats__seat",
            )
            .order_by("-created_at")
        )


class ReservationCancelView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        reservation = get_object_or_404(
            Reservation,
            user=request.user,
            pk=kwargs["pk"],
        )
        if reservation.status == "cancelled":
            messages.warning(request, "Ta rezerwacja jest już anulowana.")
            return redirect("user-reservations")

        reservation.status = "cancelled"
        reservation.save()

        messages.success(request, "Rezerwacja została anulowana.")
        return redirect("user-reservations")
