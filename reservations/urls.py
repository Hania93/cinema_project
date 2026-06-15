from django.urls import path

from .views import UserReservationListView, ReservationDeleteView

urlpatterns = [
    path(
        "my/",
        UserReservationListView.as_view(),
        name="user-reservations",
    ),
    path("<int:pk>/delete/",
         ReservationDeleteView.as_view(),
         name="reservation-delete",
         ),
]