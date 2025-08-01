from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import (
    extend_schema, extend_schema_view,
    OpenApiResponse, OpenApiParameter
)
from drf_spectacular.types import OpenApiTypes

from .models import Load, Driver
from .serializers import (
    LoadSerializer,
    DriverAvailabilitySerializer,
    LoadMatchSerializer
)
from .services.matcher import score_driver


@extend_schema_view(
    post=extend_schema(
        request=LoadSerializer,
        responses={201: LoadSerializer},
        description='Создать новую заявку на перевозку'
    )
)
class LoadCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LoadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        load = serializer.save(company=request.user)
        return Response(LoadSerializer(load).data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name='id',
                description='ID заявки',
                required=True,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH
            )
        ],
        responses=LoadMatchSerializer(many=True),
        description='Получить топ-10 водителей для указанной заявки'
    )
)
class LoadMatchesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        load = get_object_or_404(Load, pk=id)
        drivers = Driver.objects.filter(
            is_available=True,
            truck_capacity_kg__gte=load.weight_kg * 1.1
        ).select_related('user')

        matches = []
        for driver in drivers:
            result = score_driver(load, driver)
            if result['match_score'] > 0:
                matches.append({
                    'driver': driver.id,
                    'distance_category': result['distance_category'],
                    'match_score': result['match_score'],
                })

        top10 = sorted(matches, key=lambda x: x['match_score'], reverse=True)[:10]
        serializer = LoadMatchSerializer(data=top10, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


@extend_schema_view(
    post=extend_schema(
        request=DriverAvailabilitySerializer,
        responses={200: OpenApiResponse(description='OK')},
        description='Переключить доступность текущего водителя'
    )
)
class DriverAvailabilityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DriverAvailabilitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        driver = get_object_or_404(Driver, pk=serializer.validated_data['driver_id'])
        if driver.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        driver.is_available = serializer.validated_data['is_available']
        driver.save()
        return Response(status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        responses=LoadMatchSerializer(many=True),
        description='Получить подходящие грузы для текущего водителя'
    )
)
class SuitableLoadsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        driver = get_object_or_404(Driver, user=request.user)
        loads = Load.objects.filter(status=Load.STATUS_POSTED)

        suitable = []
        for load in loads:
            if driver.truck_capacity_kg < load.weight_kg * 1.1:
                continue
            result = score_driver(load, driver)
            if result['match_score'] > 0:
                suitable.append({
                    'load_id': load.id,
                    'pickup_city': load.pickup_city,
                    'delivery_city': load.delivery_city,
                    'distance_category': result['distance_category'],
                    'match_score': result['match_score'],
                })

        top10 = sorted(suitable, key=lambda x: x['match_score'], reverse=True)[:10]
        return Response(top10)