from django.views.generic import DetailView, ListView

from .models import Genre, Movie


class MovieListView(ListView):
    model = Movie
    template_name = "movies/movie_list.html"
    context_object_name = "movies"
    paginate_by = 10

    def get_queryset(self):
        qs = Movie.objects.select_related("director").prefetch_related(
            "genres", "actors"
        )

        genre_id = self.request.GET.get("genre")

        if genre_id:
            qs = qs.filter(genres__id=genre_id)

        q = self.request.GET.get("q")

        if q:
            qs = qs.filter(title__icontains=q)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["genres"] = Genre.objects.all()

        context["current_q"] = self.request.GET.get("q", "")
        
        context["query_params"] = self.request.GET.copy()
        context["query_params"].pop("page", None)

        return context


class MovieDetailView(DetailView):
    model = Movie
    template_name = "movies/movie_detail.html"
    context_object_name = "movie"

    def get_queryset(self):

        return Movie.objects.select_related("director").prefetch_related(
            "genres", "movieactor_set__actor"
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cast"] = (
            self.object.movieactor_set
            .select_related("actor")
            .order_by("billing_order")
        )
        return context   
