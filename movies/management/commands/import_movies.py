import requests

from django.conf import settings

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from movies.models import Actor, Director, Genre, Movie, MovieActor


class Command(BaseCommand):
    help = "Import popular movies from TMDb"

    def build_tmdb_image_url(self, img_path):
        if not img_path:
            return ""

        return f"https://image.tmdb.org/t/p/w500{img_path}"
        
    def download_image(
        self,
        img_path,
        db_object,
        field_name,
    ):
        img_field = getattr(db_object, field_name)

        if img_path and not img_field:
            img_url = self.build_tmdb_image_url(img_path)

            try:
                img_response = requests.get(img_url, timeout=10)
                img_response.raise_for_status()

                img_field.save(
                    f"{field_name}_{db_object.tmdb_id or 'unknown'}.jpg",
                    ContentFile(img_response.content),
                    save=True,
                )

            except requests.RequestException as e:
                self.stdout.write(
                    self.style.WARNING(
                        f"Nie udało się pobrać obrazu dla TMDB ID={db_object.tmdb_id}: {e}"
                    )
                )

    def fetch_movies(self, page, headers):
        try:
            response_movies = requests.get(
                "https://api.themoviedb.org/3/movie/popular",
                headers=headers,
                params={
                    "language": "en-US",
                    "page": page,
                },
                timeout=10,
            )
            response_movies.raise_for_status()

        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Błąd TMDb: {e}"))
            return []

        data = response_movies.json()
        return data.get("results", [])

    def fetch_movie_details(self, movie_id, headers):
        try:
            response = requests.get(
                f"https://api.themoviedb.org/3/movie/{movie_id}",
                headers=headers,
                params={
                    "language": "en-US",
                    "append_to_response": "credits,videos",
                },
                timeout=10,
            )
            response.raise_for_status()

        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Błąd TMDb: {e}"))
            return None

        return response.json()

    def get_or_create_director(self, details):
        credits = details.get("credits", {})

        director_data = next(
            (
                person
                for person in credits.get("crew", [])
                if person.get("job") == "Director"
            ),
            None,
        )

        if not director_data:
            return None

        profile_path = director_data.get("profile_path")

        director, _ = Director.objects.update_or_create(
            tmdb_id=director_data["id"],
            defaults={
                "name": director_data["name"],
                "photo_url": self.build_tmdb_image_url(profile_path),
            },
        )

        self.download_image(profile_path, director, "photo")

        return director

    def get_or_create_genres(self, details):
        genres = []
        genres_data = details.get("genres", [])

        if not genres_data:
            return None

        for genre_item in genres_data:
            genre, _ = Genre.objects.get_or_create(
                tmdb_id=genre_item["id"],
                defaults={
                    "name": genre_item["name"],
                },
            )
            genres.append(genre)

        return genres

    def get_trailer_url(self, details):
        videos = details.get("videos", {})
        videos_data = videos.get("results", [])

        for video in videos_data:
            if video.get("site") == "YouTube" and video.get("type") == "Trailer":
                return f"https://www.youtube.com/watch?v={video['key']}"

        return ""

    def get_or_create_movie(self, details, director, genres, trailer_url):
        poster_path = details.get("poster_path")

        movie, _ = Movie.objects.update_or_create(
            tmdb_id=details["id"],
            defaults={
                "title": details.get("title", ""),
                "description": details.get("overview", ""),
                "duration": details.get("runtime") or 0,
                "release_date": details.get("release_date") or None,
                "vote_average": round(details.get("vote_average", 0), 1),
                "vote_count": details.get("vote_count", 0),
                "trailer_url": trailer_url,
                "director": director,
                "poster_url": self.build_tmdb_image_url(poster_path),
            },
        )

        movie.genres.set(genres)

        self.download_image(poster_path, movie, "poster")

        return movie

    def get_or_create_actors(self, details, movie):
        credits = details.get("credits", {})

        for actor_data in credits.get("cast", [])[:10]:
            profile_path = actor_data.get("profile_path")

            actor, _ = Actor.objects.update_or_create(
                tmdb_id=actor_data["id"],
                defaults={
                    "name": actor_data["name"],
                    "photo_url": self.build_tmdb_image_url(profile_path),
                },
            )

            self.download_image(profile_path, actor, "photo")

            MovieActor.objects.update_or_create(
                movie=movie,
                actor=actor,
                defaults={
                    "role_name": actor_data.get("character") or "",
                    "billing_order": actor_data.get("order") or 0,
                },
            )

    def handle(self, *args, **kwargs):
        api_token = settings.TMDB_API_TOKEN

        if not api_token:
            self.stdout.write(self.style.ERROR("Brak TMDB_API_TOKEN w settings."))
            return

        headers = {
            "Authorization": f"Bearer {api_token}",
            "accept": "application/json",
        }

        for page in range(1, 3):
            movies_data = self.fetch_movies(page, headers)

            for item in movies_data:
                tmdb_movie_id = item.get("id")

                if not tmdb_movie_id:
                    continue

                movie_details = self.fetch_movie_details(tmdb_movie_id, headers)

                if not movie_details:
                    continue

                director = self.get_or_create_director(movie_details)

                if not director:
                    continue

                genres = self.get_or_create_genres(movie_details)

                if not genres:
                    continue

                trailer_url = self.get_trailer_url(movie_details)

                movie = self.get_or_create_movie(
                    movie_details,
                    director,
                    genres,
                    trailer_url,
                )

                self.get_or_create_actors(movie_details, movie)

                self.stdout.write(self.style.SUCCESS(f"Imported: {movie.title}"))
