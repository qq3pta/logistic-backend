import pytest
from django.urls import reverse
from api.models import Load, Driver
from decimal import Decimal

@pytest.mark.django_db
def test_suitable_loads(auth_client, user):
    driver = Driver.objects.create(
        user=user, home_city="NY", truck_capacity_kg=1000,
        is_available=True, hourly_rate=Decimal("30.00"), experience_years=5)
    load = Load.objects.create(
        company=user, pickup_city="NY", delivery_city="NY",
        weight_kg=800, pickup_date="2025-08-10", max_budget=Decimal("1000.00"))
    url = reverse('suitable-loads')
    resp = auth_client.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert any(item["load_id"] == load.id for item in data)