from django.urls import path
from .views import (
    LoadCreateView,
    LoadMatchesView,
    DriverAvailabilityView,
    SuitableLoadsView,
)

urlpatterns = [
    path('loads/', LoadCreateView.as_view(), name='load-create'),
    path('loads/<int:id>/matches/', LoadMatchesView.as_view(), name='load-matches'),
    path('drivers/availability/', DriverAvailabilityView.as_view(), name='driver-availability'),
    path('drivers/suitable-loads/', SuitableLoadsView.as_view(), name='suitable-loads'),
]