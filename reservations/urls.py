from django.urls import path

from .views import ReservationCancelView, UserReservationListView

urlpatterns = [
    path(
        "my/",
        UserReservationListView.as_view(),
        name="user-reservations",
    ),
    path(
        "<int:pk>/cancel/",
        ReservationCancelView.as_view(),
        name="reservation-cancel",
    ),
]
