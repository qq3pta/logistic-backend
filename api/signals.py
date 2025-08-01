from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Driver, Load

@receiver(post_save, sender=Driver)
def clear_driver_match_cache(sender, instance, **kwargs):
    # удаляем все ключи match_<любое>_<driver.id>
    cache.delete_pattern(f"match_*_{instance.id}")

@receiver(post_save, sender=Load)
def clear_load_match_cache(sender, instance, **kwargs):
    # удаляем все ключи match_<load.id>_*
    cache.delete_pattern(f"match_{instance.id}_*")