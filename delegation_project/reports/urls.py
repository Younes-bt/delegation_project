from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceReportViewSet

router = DefaultRouter()
router.register(r'reports', AttendanceReportViewSet, basename='attendance-report')

urlpatterns = [
    path('', include(router.urls)),
] 