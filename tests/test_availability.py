import pytest
from django.urls import reverse
from api.models import Driver

@pytest.mark.django_db
def test_toggle_availability(auth_client, user):
    driver = Driver.objects.create(
        user=user, home_city="A", truck_capacity_kg=1000,
        is_available=False, hourly_rate=10, experience_years=1)
    url = reverse('driver-availability')
    resp = auth_client.post(url, {"driver_id": driver.id, "is_available": True}, format='json')
    assert resp.status_code == 200
    driver.refresh_from_db()
    assert driver.is_available is True