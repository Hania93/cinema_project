from django.contrib import admin

from .models import Screening, Hall, Seat


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = (
        "hall",
        "row",
        "number",
    )

    list_filter = ("hall", "row")

    search_fields = ("hall__name",)


@admin.register(Screening)
class ScreeningAdmin(admin.ModelAdmin):
    list_display = (
        "movie",
        "start_time",
        "end_time",
        "hall",
    )

    list_filter = ("movie", "start_time", "hall")

    search_fields = ("movie__title",)

    readonly_fields = ("end_time",)
