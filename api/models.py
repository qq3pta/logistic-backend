from django.db import models
from django.conf import settings

class Driver(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='driver_profile'
    )
    home_city = models.CharField(max_length=100)
    truck_capacity_kg = models.PositiveIntegerField()
    is_available = models.BooleanField(default=False)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    experience_years = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} ({self.home_city})"

    class Meta:
        indexes = [
            models.Index(fields=['is_available']),
            models.Index(fields=['home_city']),
        ]
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'


class Load(models.Model):
    STATUS_POSTED = 'POSTED'
    STATUS_MATCHED = 'MATCHED'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_CHOICES = [
        (STATUS_POSTED, 'posted'),
        (STATUS_MATCHED, 'matched'),
        (STATUS_COMPLETED, 'completed'),
    ]

    company = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='loads'
    )
    pickup_city = models.CharField(max_length=100)
    delivery_city = models.CharField(max_length=100)
    weight_kg = models.PositiveIntegerField()
    pickup_date = models.DateField()
    max_budget = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_POSTED
    )

    def __str__(self):
        return f"Load #{self.id}: {self.pickup_city} → {self.delivery_city}"

    class Meta:
        indexes = [
            models.Index(fields=['pickup_city', 'delivery_city']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'Load'
        verbose_name_plural = 'Loads'


class LoadMatch(models.Model):
    DIST_SAME = 'SAME_CITY'
    DIST_NEAR = 'NEARBY'
    DIST_REG = 'REGIONAL'
    DIST_LONG = 'LONG_DISTANCE'
    CATEGORIES = [
        (DIST_SAME, 'same_city'),
        (DIST_NEAR, 'nearby'),
        (DIST_REG, 'regional'),
        (DIST_LONG, 'long_distance'),
    ]

    load = models.ForeignKey(
        Load,
        on_delete=models.CASCADE,
        related_name='matches'
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name='matches'
    )
    distance_category = models.CharField(max_length=20, choices=CATEGORIES)
    match_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match L{self.load_id} ↔ D{self.driver_id}: {self.match_score}"

    class Meta:
        unique_together = [('load', 'driver')]
        indexes = [
            models.Index(fields=['distance_category']),
            models.Index(fields=['match_score']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'Load Match'
        verbose_name_plural = 'Load Matches'