from datetime import timedelta

from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.generic import DetailView, ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from collections import defaultdict

from .models import Screening
from reservations.models import Reservation, ReservationSeat


class ScreeningListView(ListView):
    model = Screening
    template_name = "screenings/screening_list.html"
    context_object_name = "screenings"

    def get_selected_date(self):
        selected_date = parse_date(self.request.GET.get("date", ""))

        if selected_date:
            return selected_date

        return timezone.localdate()

    # def get_queryset(self):
    #     selected_date = self.get_selected_date()

    #     return (
    #         Screening.objects
    #         .select_related("movie", "hall")
    #         .filter(start_time__date=selected_date)
    #         .order_by("start_time")
    #     )

    def get_queryset(self):
        qs = Screening.objects.select_related(
            "movie",
            "hall",
        ).order_by("start_time")

        selected_date = self.get_selected_date()

        if selected_date:
            qs = qs.filter(start_time__date=selected_date)
        else:
            today = timezone.localdate()
            qs = qs.filter(start_time__date=today)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.localdate()

        context["dates"] = [today + timedelta(days=i) for i in range(7)]
        context["current_date"] = self.get_selected_date().isoformat()

        return context


class ScreeningDetailView(LoginRequiredMixin, DetailView):
    model = Screening
    template_name = "screenings/screening_detail.html"
    context_object_name = "screening"

    def get_queryset(self):
        return Screening.objects.select_related(
            "movie",
            "hall",
        ).order_by("start_time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        seats = self.object.hall.seats.all().order_by(
            "row",
            "number",
        )

        seats_by_row = defaultdict(list)

        for seat in seats:
            seats_by_row[seat.row].append(seat)

        reserved_seat_ids = ReservationSeat.objects.filter(
            reservation__screening=self.object,
            reservation__status__in=["confirmed", "pending"],
        ).values_list(
            "seat_id",
            flat=True,
        )

        context["seats_by_row"] = dict(seats_by_row)
        context["reserved_seat_ids"] = set(reserved_seat_ids)
        available_seats = seats.count() - len(reserved_seat_ids)
        context["available_seats"] = available_seats

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        selected_seat_ids = request.POST.getlist("seats")

        if not selected_seat_ids:
            messages.error(request, "Wybierz przynajmniej jedno miejsce.")
            return redirect("screening-detail", pk=self.object.pk)

        already_reserved = ReservationSeat.objects.filter(
            reservation__screening=self.object,
            reservation__status__in=["pending", "confirmed"],
            seat_id__in=selected_seat_ids,
        ).exists()

        if already_reserved:
            messages.error(request, "Jedno z wybranych miejsc jest już zajęte.")
            return redirect("screening-detail", pk=self.object.pk)

        reservation = Reservation.objects.create(
            user=request.user,
            screening=self.object,
        )

        for seat_id in selected_seat_ids:
            ReservationSeat.objects.create(
                reservation=reservation,
                seat_id=seat_id,
            )

        messages.success(request, "Rezerwacja została utworzona.")
        return redirect("screening-detail", pk=self.object.pk)
