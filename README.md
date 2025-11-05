# InforceTest — Django REST API (Restaurant Menus & Voting)

This is a **Django + Django REST Framework** project for managing restaurants, daily menus, and voting for the best menu of the day.
The project uses **PostgreSQL** and is fully containerized with **Docker / docker-compose**.
Authentication is handled using **JWT (djangorestframework-simplejwt)**.

---

## Table of Contents

* Overview
* Requirements
* Project Structure
* Setup (Local / Docker)
* Database Migrations & Superuser
* Running the Server
* Running Tests
* API Endpoints
* Example JSON Payloads
* Common Issues
* License

---

## Overview

The API provides endpoints to:

* Register users
* Obtain JWT tokens (login / refresh)
* Create and list restaurants
* Create daily menus (with categories and menu items)
* Vote for a restaurant’s menu
* Get voting results for the current day

---

## Requirements

* Docker & docker-compose
* Python 3.12+ (for local setup)
* PostgreSQL (provided as a container in docker-compose)
* Dependencies listed in `requirements.txt`:

  * Django
  * Django REST Framework
  * SimpleJWT
  * Pytest & pytest-django

---

## Project Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── pytest.ini
├── requirements.txt
├── inforcetest/          # Django project (settings.py, urls.py)
├── restaurant/           # App: Menu, MenuItem, Restaurant, serializers, views
├── users/                # App: User registration, voting logic, serializers, views
└── tests/                # pytest tests
└── auth/                 #App: Registartion
```

---

## Setup (Docker — recommended)



1. Build and run containers:

```bash
docker-compose up --build -d
```

2. Run migrations and create a superuser:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

> ⚠️ If you update `requirements.txt`, rebuild your image:
>
> ```bash
> docker-compose build --no-cache
> ```

---

## Setup (Local Development)

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure your database in `settings.py`

3. Run migrations and start the server:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## Migrations & Admin

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## Running Tests (pytest)

### Locally:

```bash
pytest -v
```

Make sure your `pytest.ini` file includes:

```
[pytest]
DJANGO_SETTINGS_MODULE = inforcetest.settings
```

### Inside Docker:

```bash
docker-compose exec web pytest -v
```

or (recommended for CI):

```bash
docker-compose run --rm web pytest -v
```

> Ensure `pytest` and `pytest-django` are installed inside the container.

---

## Main API Endpoints

**Base URL:** `http://localhost:8000/`

### 🔐 Authentication

| Method | Endpoint              | Description                     |
| ------ | --------------------- | ------------------------------- |
| `POST` | `/register/`          | Register a new user             |
| `POST` | `/api/token/`         | Get access & refresh JWT tokens |
| `POST` | `/api/token/refresh/` | Refresh access token            |


**Example login:**

```json
{
  "username": "alice",
  "password": "pass"
}
```

**Response:**

```json
{
  "access": "jwt_access_token_here",
  "refresh": "jwt_refresh_token_here"
}
```

> Add this header to all protected requests:
>
> ```
> Authorization: Bearer <access_token>
> ```

---

### 🍽️ Restaurants & Menus

| Method | Endpoint            | Description                |
| ------ | ------------------- | -------------------------- |
| `GET`  | `/restaurants/`     | List all restaurants       |
| `POST` | `/restaurants/`     | Create a restaurant        |
| `GET`  | `/menus/`           | List today’s menus         |
| `POST` | `/menus/`           | Create a new menu          |
| `GET`  | `/menus/<id>/`      | Retrieve a specific menu   |
| `POST` | `/votes/`           | Cast a vote for a menu     |
| `GET`  | `/results/`         | Get today’s voting results |

---

## Example JSON for Creating a Menu

`POST /api/menus/`
Header: `Authorization: Bearer <access_token>`

```json
{
  "menu_date": "2025-11-05",
  "restaurant": 1,
  "categories": [
    {
      "name": "Italian",
      "items": [
        {
          "name": "Margherita Pizza",
          "price": 1200,
          "description": "Classic pizza with mozzarella, tomatoes, and basil",
          "category": "Italian"
        },
        {
          "name": "Spaghetti Carbonara",
          "price": 1500,
          "description": "Creamy pasta with pancetta and parmesan",
          "category": "Italian"
        }
      ]
    },
    {
      "name": "Desserts",
      "items": [
        {
          "name": "Tiramisu",
          "price": 800,
          "description": "Coffee-flavored Italian dessert",
          "category": "Desserts"
        }
      ]
    }
  ]
}
```

---

## JWT Authentication Notes

* Tokens are tied to a specific user in your database.
  If you change your DB (e.g., new Postgres container), re-register users and generate new tokens.
* Always include:

  ```
  Authorization: Bearer <access_token>
  ```
* If you see `"User not found"`, the token likely references a user ID missing in your new DB.

---

## Common Issues

**❌ “Apps aren't loaded yet” in pytest**
→ Ensure `pytest-django` is installed and `pytest.ini` has `DJANGO_SETTINGS_MODULE`.

**❌ “User not found” even with a valid token**
→ You likely need to register the user again after switching databases.

**❌ Multiple menus for today**
→ When filtering, ensure you use `menu_date=today` (for `DateField`).

**❌ Serializer returns object instead of list**
→ Always use `many=True` when returning multiple objects.

---

## Minimal `requirements.txt`

```
Django>=5.0,<6.0
djangorestframework>=3.15
djangorestframework-simplejwt>=5.3.1
psycopg2-binary>=2.9
python-dotenv>=1.0
pytest>=8.0
pytest-django>=4.8
pytest-cov>=4.0
django-cors-headers>=4.0
```

---

## Useful Docker Commands

```bash
# Start the containers
docker-compose up --build -d

# View logs
docker-compose logs -f web

# Access the container shell
docker-compose exec web bash

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run tests
docker-compose exec web pytest -v
```

---

## License

You are free to use this code for learning or commercial purposes.
(Feel free to add an open-source license such as MIT or Apache 2.0 if you plan to publish it.)

---

Would you like me to include a ready-to-copy **Dockerfile**, **docker-compose.yml**, and **pytest.ini** section right below this (to make your README 100% self-contained)?
