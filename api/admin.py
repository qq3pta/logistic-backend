from django.contrib import admin
from .models import Driver, Load, LoadMatch

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'home_city', 'truck_capacity_kg', 'is_available', 'experience_years')
    list_filter = ('is_available', 'home_city')
    search_fields = ('user__username',)

@admin.register(Load)
class LoadAdmin(admin.ModelAdmin):
    list_display = ('id','company','pickup_city','delivery_city','weight_kg','status','created_at')
    list_filter = ('status','pickup_city','delivery_city')
    search_fields = ('company__username',)

@admin.register(LoadMatch)
class LoadMatchAdmin(admin.ModelAdmin):
    list_display = ('load','driver','distance_category','match_score','created_at')
    list_filter = ('distance_category',)