from django.contrib import admin
from .models import Screening


@admin.register(Screening)
class ScreeningAdmin(admin.ModelAdmin):
    list_display = (
        "movie",
        "start_time",
        "hall",
    )

    list_filter = ("start_time", "hall")
