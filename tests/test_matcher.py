import pytest
from api.models import Load, Driver
from api.services.matcher import score_driver
from decimal import Decimal

@pytest.mark.django_db
def test_score_driver_basic(user):
    load = Load(company=user, pickup_city="NY", delivery_city="Boston",
                weight_kg=500, pickup_date="2025-08-10", max_budget=Decimal("1000"))
    driver = Driver(user=user, home_city="NY", truck_capacity_kg=600,
                    is_available=True, hourly_rate=Decimal("50"), experience_years=4)
    result = score_driver(load, driver)
    assert result["distance_category"] == "SAME_CITY"
    assert result["match_score"] > 0