CITY_DISTANCES = {
    'New York':    {'nearby': ['Philadelphia','Newark'], 'regional': ['Boston','Washington DC']},
    'Los Angeles': {'nearby': ['San Diego','Long Beach'], 'regional': ['San Francisco','Las Vegas']},
}

def categorize_distance(origin: str, dest: str) -> str:
    if origin == dest:
        return 'SAME_CITY'
    cfg = CITY_DISTANCES.get(origin, {})
    if dest in cfg.get('nearby', []):
        return 'NEARBY'
    if dest in cfg.get('regional', []):
        return 'REGIONAL'
    return 'LONG_DISTANCE'