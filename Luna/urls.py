from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HydroponicSystemViewSet, ReadingViewSet

router = DefaultRouter()
router.register(r"systems", HydroponicSystemViewSet, basename="hydroponic system")
router.register(r"readings", ReadingViewSet, basename="reading")

urlpatterns = [
    path("", include(router.urls)),
]
