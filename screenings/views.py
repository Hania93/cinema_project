from datetime import timedelta

from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.generic import DetailView, ListView

from .models import Screening


class ScreeningListView(ListView):
    model = Screening
    template_name = "screenings/screening_list.html"
    context_object_name = "screenings"
    
    def get_selected_date(self):
        selected_date = parse_date(self.request.GET.get("date", ""))
        
        if selected_date:
            return selected_date

        return timezone.localdate()

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


class ScreeningDetailView(DetailView):
    model = Screening
    template_name = "screenings/screening_detail.html"
    context_object_name = "screening"

    def get_queryset(self):
        return Screening.objects.select_related(
            "movie",
            "hall",
        ).order_by("start_time")
