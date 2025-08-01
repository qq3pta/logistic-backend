from django.urls import path
from .views import LoadCreateView, LoadMatchesView, DriverAvailabilityView, SuitableLoadsView

urlpatterns = [
    path('loads/', LoadCreateView.as_view()),
    path('loads/<int:id>/matches/', LoadMatchesView.as_view()),
    path('drivers/availability/', DriverAvailabilityView.as_view()),
    path('drivers/suitable-loads/', SuitableLoadsView.as_view()),
]