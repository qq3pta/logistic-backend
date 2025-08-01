import pytest
from django.urls import reverse
from decimal import Decimal

@pytest.mark.django_db
def test_create_load(auth_client):
    url = reverse('load-create')
    data = {
        "pickup_city": "New York",
        "delivery_city": "Boston",
        "weight_kg": 1000,
        "pickup_date": "2025-08-10",
        "max_budget": "500.00"
    }
    resp = auth_client.post(url, data, format='json')
    assert resp.status_code == 201
    body = resp.json()
    assert body["pickup_city"] == data["pickup_city"]
    assert Decimal(body["max_budget"]) == Decimal("500.00")