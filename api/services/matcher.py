from .distance import categorize_distance
from django.core.cache import cache

def get_estimated_hours(origin: str, dest: str) -> float:
    return 1.0

def score_driver(load, driver):
    cache_key = f"match_{load.id}_{driver.id}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    # 1) Distance Score
    dist_cat = categorize_distance(driver.home_city, load.pickup_city)
    dist_scores = {'SAME_CITY': 100, 'NEARBY': 75, 'REGIONAL': 50, 'LONG_DISTANCE': 25}
    distance_score = dist_scores.get(dist_cat, 0)

    # 2) Capacity Match Score
    util = (load.weight_kg / driver.truck_capacity_kg) * 100
    if util > 100:
        capacity_score = 0
    elif util >= 80:
        capacity_score = 100
    elif util >= 60:
        capacity_score = 75
    elif util >= 40:
        capacity_score = 50
    elif util >= 20:
        capacity_score = 25
    else:
        capacity_score = 0

    # 3) Budget vs Rate
    hours = get_estimated_hours(load.pickup_city, load.delivery_city)
    total_cost = float(driver.hourly_rate) * hours
    if total_cost <= float(load.max_budget):
        budget_score = min((float(load.max_budget) / total_cost) * 100, 100)
    else:
        budget_score = 0

    # 4) Experience Bonus
    exp = driver.experience_years
    if exp >= 5:
        exp_bonus = 20
    elif exp >= 3:
        exp_bonus = 10
    elif exp >= 1:
        exp_bonus = 5
    else:
        exp_bonus = 0

    total_score = (
        distance_score * 0.35 +
        capacity_score * 0.30 +
        budget_score * 0.25 +
        exp_bonus * 0.10
    )
    result = {'distance_category': dist_cat, 'match_score': round(total_score, 2)}
    cache.set(cache_key, result, timeout=600)
    return result