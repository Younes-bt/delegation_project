from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduleEntryViewSet, TeacherAvailabilityViewSet, HolidayViewSet

router = DefaultRouter()
router.register(r'schedules', ScheduleEntryViewSet, basename='schedule')
router.register(r'availability', TeacherAvailabilityViewSet, basename='availability')
router.register(r'holidays', HolidayViewSet, basename='holiday')

urlpatterns = [
    path('', include(router.urls)),
] 