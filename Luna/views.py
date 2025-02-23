from django.db.models import Prefetch
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from rest_framework import viewsets, permissions

from .models import HydroponicSystem, Reading
from .seliarizers import (
    HydroponicSystemSerializer,
    ReadingSerializer,
    HydroponicSystemDetailSerializer,
)


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class HydroponicSystemViewSet(viewsets.ModelViewSet):
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return HydroponicSystemDetailSerializer
        return HydroponicSystemSerializer

    def get_queryset(self):
        queryset = HydroponicSystem.objects.filter(owner=self.request.user)

        # Eager loading dla wydajności
        if self.action == "retrieve":
            queryset = queryset.prefetch_related(
                Prefetch(
                    "readings",
                    queryset=Reading.objects.order_by("-timestamp")[:10],
                    to_attr="latest_readings",
                )
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ReadingFilter(filters.FilterSet):
    timestamp_after = filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    timestamp_before = filters.DateTimeFilter(field_name="timestamp", lookup_expr="lte")

    class Meta:
        model = Reading
        fields = {
            "hydroponic_system": ["exact"],
            "temperature": ["exact", "gte", "lte"],
            "ph": ["exact", "gte", "lte"],
            "tds": ["exact", "gte", "lte"],
        }


class ReadingViewSet(viewsets.ModelViewSet):
    serializer_class = ReadingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend, drf_filters.OrderingFilter]
    filterset_class = ReadingFilter
    ordering_fields = ["timestamp", "temperature", "ph", "tds"]

    def get_queryset(self):
        return Reading.objects.filter(
            hydroponic_system__owner=self.request.user
        ).order_by("-timestamp")
