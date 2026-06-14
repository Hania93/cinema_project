from django.urls import path
from .views import ScreeningListView, ScreeningDetailView

urlpatterns = [
    path("", ScreeningListView.as_view(), name="screening-list"),
    path("<int:pk>/", ScreeningDetailView.as_view(), name="screening-detail"),
]
