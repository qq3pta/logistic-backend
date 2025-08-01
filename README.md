# Logistics-backend

Smart Load Matching System автоматически подбирает топ-10 водителей для перевозки грузов на основе параметров: расстояние, вместимость, бюджет и опыт.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Examples](#examples)
- [Error Codes](#error-codes)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features
- Создание и управление заявками (Load)
- Тоггл доступности водителей
- Подбор топ-10 водителей по скорингу
- Получение подходящих грузов для водителя
- Redis-кеширование (10 мин) с инвалидацией
- Документация Swagger и DRF Browseable
- Dockerized: Django, PostgreSQL, Redis
- JWT-аутентификация

## Tech Stack
- Python 3.12+, Django 5.2, DRF
- PostgreSQL 15, Redis 7
- Gunicorn, Docker, docker-compose
- pytest, pytest-django

## Quick Start
```bash
git clone https://github.com/your-org/logistics-load-matching-api.git
cd logistics-load-matching-api
cp .env.example .env
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```

## Configuration
Создайте в корне ```.env:```

```env
POSTGRES_DB=logistics
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secret
DJANGO_SECRET_KEY=<your_secret_key>
```