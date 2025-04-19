from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'associations', views.AssociationViewSet)
router.register(r'centers', views.CenterViewSet)
router.register(r'trainings', views.TrainingViewSet)
router.register(r'cities', views.CityViewSet)
router.register(r'profiles', views.UserProfileViewSet)
router.register(r'materials', views.MaterialViewSet)

urlpatterns = [
    path('users/signup/', views.UserCreateView.as_view(), name='user-signup'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('trainings/me/', views.TeacherTrainingsView.as_view(), name='teacher-trainings'),
    path('', include(router.urls)),
]