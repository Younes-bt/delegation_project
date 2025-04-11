from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, ExerciseViewSet, ProgressViewSet, SubmissionViewSet, AttendanceViewSet, MarkViewSet  

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'exercises', ExerciseViewSet)
router.register(r'progress', ProgressViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'attendances', AttendanceViewSet)
router.register(r'marks', MarkViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
