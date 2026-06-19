# 🎬 Cinema Project

A web application for browsing movies, viewing screenings and reserving cinema tickets.

## Features

### Authentication

* User registration
* User login and logout
* User reservation history

### Movies

* Browse movies
* Search movies
* Filter movies by genre
* Movie details page
* Director and cast information

### Screenings

* Daily repertoire
* Screening details
* Hall information

### Reservations

* Seat selection
* Reservation creation
* Reservation cancellation
* Reservation history
* Seat availability validation

### Email Notifications

* Reservation confirmation emails

### Data Management

* Import movies from TMDb API
* Generate fake reservations using Faker

## Technologies

* Python 3.12
* Django
* PostgreSQL
* Bootstrap 5
* Docker
* TMDb API
* Faker

## Installation

Clone repository:

```bash
git clone <repository-url>
cd cinema_project
```

Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file and configure environment variables.

Run migrations:

```bash
python manage.py migrate
```

Run server:

```bash
python manage.py runserver
```

## Docker

Build and start containers:

```bash
docker compose up --build
```

Run migrations:

```bash
docker compose exec web python manage.py migrate
```

Create superuser:

```bash
docker compose exec web python manage.py createsuperuser
```

Run tests:

```bash
docker compose exec web python manage.py test
```

Stop containers:

```bash
docker compose down
```

## Management Commands

Import movies from TMDb:

```bash
python manage.py import_movies
```

Generate fake reservations:

```bash
python manage.py seed_reservations
```

## Tests

Run all tests:

```bash
python manage.py test
```

## Future Improvements

* Stripe payments
* Celery + Redis
* REST API
* Swagger/OpenAPI documentation
* PDF tickets

## Author

Portfolio project created to learn Django, PostgreSQL, Docker and web application development.
