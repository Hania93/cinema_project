from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views.generic import ListView, DeleteView

from .models import Reservation

class UserReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "reservations/user_reservation_list.html"
    context_object_name = "reservations"
    
    def get_queryset(self):
        return (
            Reservation.objects
            .filter(user=self.request.user)
            .select_related(
                "screening", 
                "screening__movie",
                "screening__hall"
            )
            .prefetch_related(
                "reserved_seats__seat",
            )
            .order_by("-created_at")        
        )

class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name ="reservations/reservation_confirm_delete.html"
    success_url = reverse_lazy("user-reservations")
    
    def get_queryset(self):
        return Reservation.objects.filter(
            user=self.request.user,
        )