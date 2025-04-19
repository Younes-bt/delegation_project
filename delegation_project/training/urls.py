from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExerciseViewSet, ProgressViewSet, SubmissionViewSet, AttendanceViewSet, MarkViewSet, AnnualDistributionsView
from . import views

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet)
router.register(r'progress', ProgressViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'attendances', AttendanceViewSet)
router.register(r'marks', MarkViewSet)

urlpatterns = [
    path('annual-distributions/', views.AnnualDistributionsView.as_view(), name='annual-distributions'),
    path('', include(router.urls)),
]
