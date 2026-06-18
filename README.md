# 🎬 Cinema Project

A web application for browsing movies, viewing screenings and reserving cinema tickets.

## Features

### Authentication

* User registration
* User login/logout
* User reservation history

### Movies

* Browse all movies
* Movie details page
* Director information
* Cast information
* Genre filtering
* Movie search

### Screenings

* Daily repertoire
* Upcoming screenings
* Screening details
* Hall information

### Reservations

* Interactive seat selection
* Seat availability validation
* Reservation creation
* Reservation cancellation
* Reservation history
* Reservation status management

### Email Notifications

* Reservation confirmation emails

### Data Management

* Import movies from TMDb API
* Generate fake reservations using Faker
* Automatically generate future screenings

---

## Technologies

### Backend

* Python 3
* Django
* PostgreSQL

### Frontend

* HTML
* CSS
* Bootstrap 5

### External Services

* TMDb API
* Gmail SMTP

### Development Tools

* Faker
* Ruff
* Git
* Docker

---

## Project Structure

```text
cinema_project/
├── accounts/
├── movies/
├── screenings/
├── reservations/
├── templates/
├── static/
├── media/
├── manage.py
└── requirements.txt
```

---

## Installation

### Clone repository

```bash
git clone <repository-url>
cd cinema_project
```

### Create virtual environment

Linux / macOS:

```bash
python -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root directory.

Example configuration:

```env
SECRET_KEY=your_secret_key

DEBUG=True

DB_NAME=cinema
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

TMDB_API_TOKEN=your_tmdb_token

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

### Apply migrations

```bash
python manage.py migrate
```

### Create superuser

```bash
python manage.py createsuperuser
```

### Run development server

```bash
python manage.py runserver
```

Application will be available at:

```text
http://127.0.0.1:8000/
```

---

## Management Commands

### Import movies from TMDb

```bash
python manage.py import_movies
```

Imports:

* movies
* genres
* directors
* actors
* posters

### Generate future screenings

```bash
python manage.py generate_screenings
```

Keeps the repertoire available for the next 7 days.

### Generate fake reservations

```bash
python manage.py seed_reservations
```

Generates:

* users
* reservations
* reserved seats

---

## Running Tests

Run all tests:

```bash
python manage.py test
```

Run tests for a specific application:

```bash
python manage.py test reservations
```

```bash
python manage.py test screenings
```

```bash
python manage.py test movies
```

```bash
python manage.py test accounts
```

---

## Implemented Tests

* Reservation total cost calculation
* Reservation seat validation
* Reservation cancellation
* User reservations view
* Screening overlap validation
* User registration
* Movie genres relationship

---

## Future Improvements

* Stripe payments
* Celery + Redis
* PDF tickets
* REST API
* Swagger/OpenAPI documentation
* Recommendation system

---

## Author

Created as a portfolio project for learning Django, PostgreSQL and web application development.
