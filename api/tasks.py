from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Driver, Load

@receiver(post_save, sender=Driver)
def invalidate_driver_cache(sender, instance, **kwargs):
    cache.delete(f"availability_{instance.id}")
    # инвалидировать все match-кеши для водителя
    redis = get_redis_connection()
    for key in redis.scan_iter(f"match_*_{instance.id}"):
        redis.delete(key)

@receiver(post_save, sender=Load)
def invalidate_load_cache(sender, instance, **kwargs):
    # инвалидировать все match-кеши для груза
    redis = get_redis_connection()
    for key in redis.scan_iter(f"match_{instance.id}_*"):
        redis.delete(key)