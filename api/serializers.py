from rest_framework import serializers
from .models import Load, LoadMatch

class LoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Load
        fields = [
            'id', 'company', 'pickup_city', 'delivery_city',
            'weight_kg', 'pickup_date', 'max_budget',
            'status', 'created_at'
        ]
        read_only_fields = ['id', 'company', 'status', 'created_at']

class DriverAvailabilitySerializer(serializers.Serializer):
    driver_id = serializers.IntegerField()
    is_available = serializers.BooleanField()

class LoadMatchSerializer(serializers.Serializer):
    driver = serializers.IntegerField()
    distance_category = serializers.CharField(max_length=20)
    match_score = serializers.FloatField()