import pytest
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth import get_user_model
from api.models import Load, Driver

User = get_user_model()

@pytest.mark.django_db
def test_load_matches(auth_client, user):
    # 1) Создаём груз
    load = Load.objects.create(
        company=user,
        pickup_city="New York",
        delivery_city="Philadelphia",
        weight_kg=1000,
        pickup_date="2025-08-10",
        max_budget=Decimal("1000.00")
    )
    # 2) Создаём пользователя-водителя
    driver_user = User.objects.create_user("drv", "drv@example.com", "pass123")
    driver = Driver.objects.create(
        user=driver_user,
        home_city="New York",
        truck_capacity_kg=2000,
        is_available=True,
        hourly_rate=Decimal("50.00"),
        experience_years=3,
    )
    # 3) Делаем запрос и проверяем ответ
    url = reverse('load-matches', args=[load.id])
    resp = auth_client.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]["driver"] == driver.id