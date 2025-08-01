# API Reference

## Authentication

### Получение токена
**POST** `/api/token/`

**Request Body:**
```json
{
  "username": "admin",
  "password": "secret"
}
```
**Response 200:**
```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}
```
**Errors:**

401 Unauthorized — неверный credentials

## Endpoints
### 1. Создать Load
#### POST ```/api/loads/```
**Headers:**
```pgsql
Authorization: Bearer <access_token>
Content-Type: application/json
```
**Request Body:**
```json
{
  "pickup_city": "New York",
  "delivery_city": "Philadelphia",
  "weight_kg": 5000,
  "pickup_date": "2025-08-01",
  "max_budget": 600
}
```
**Response 201:**
```json
{
  "id": 1,
  "company": 1,
  "pickup_city": "New York",
  "delivery_city": "Philadelphia",
  "weight_kg": 5000,
  "pickup_date": "2025-08-01",
  "max_budget": "600.00",
  "status": "POSTED",
  "created_at": "2025-07-31T12:00:00Z"
}
```
**Errors:**

400 Bad Request — некорректные поля

401 Unauthorized — отсутствует или неверен токен
## 2. Получить Matches для Load
#### GET ```/api/loads/{id}/matches/```
**Headers:**
```pgsql
Authorization: Bearer <access_token>
```
**Path Parameters:**

**`id` (integer, required) — ID заявки**

**Response 200:**

```json
[
  { "driver": 3, "distance_category": "SAME_CITY", "match_score": 87.5 },
  { "driver": 5, "distance_category": "NEARBY",     "match_score": 76.0 }
]
```
**Errors:**

404 Not Found — заявка с таким `id` не найдена

401 Unauthorized

## 3. Обновить доступность водителя
#### POST ```/api/drivers/availability/```
**Headers:**
```pgsql
Authorization: Bearer <access_token>
Content-Type: application/json
```
**Request Body:**
```json
{
  "driver_id": 3,
  "is_available": true
}
```
**Response 200**

**Errors:**

400 Bad Request — некорректный JSON

403 Forbidden — попытка менять статус чужого водителя

404 Not Found — водитель с таким `driver_id` не найден

401 Unauthorized
## 4. Получить Suitable Loads для водителя
#### GET ```/api/drivers/suitable-loads/```
**Headers:**
```pgsql
Authorization: Bearer <access_token>
```
**Response 200**
```json
[
  {
    "load_id": 2,
    "pickup_city": "Los Angeles",
    "delivery_city": "San Diego",
    "distance_category": "NEARBY",
    "match_score": 72.3
  }
]
```
**Errors:**

401 Unauthorized