from django.contrib import admin
from django.db.models import Count

from .models import Reservation, ReservationSeat


class ReservationSeatInline(admin.TabularInline):
    model = ReservationSeat
    extra = 0


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "screening",
        "status",
        "seats_count",
        "total_cost_display",
        "created_at",
    ]

    list_filter = ["status", "created_at"]

    search_fields = ["user__username", "user__email", "screening__movie__title"]
    autocomplete_fields = ["user", "screening"]
    list_editable = ["status"]
    inlines = [ReservationSeatInline]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("user", "screening", "screening__movie")
            .prefetch_related("reserved_seats")
            .annotate(seats_count_db=Count("reserved_seats"))
        )

    def seats_count(self, obj):
        return obj.seats_count_db

    seats_count.short_description = "Liczba miejsc"

    def total_cost_display(self, obj):
        count = obj.seats_count_db
        return f"{count * obj.screening.price:.2f} zł"

    total_cost_display.short_description = "Koszt"


@admin.register(ReservationSeat)
class ReservationSeatAdmin(admin.ModelAdmin):
    list_display = ["reservation", "seat", "hall_name"]
    list_filter = ["seat__hall"]
    search_fields = [
        "reservation__user__username",
        "reservation__screening__movie__title",
    ]
    autocomplete_fields = ["reservation", "seat"]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("seat__hall", "reservation__screening__movie")
        )

    def hall_name(self, obj):
        return obj.seat.hall.name

    hall_name.short_description = "Sala"
