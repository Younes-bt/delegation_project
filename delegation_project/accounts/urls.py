from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssociationViewSet, CenterViewSet, TrainingViewSet, CityViewSet, UserProfileViewSet, UserListView

router = DefaultRouter()

router.register(r'associations', AssociationViewSet)
router.register(r'centers', CenterViewSet)
router.register(r'trainings', TrainingViewSet)
router.register(r'cities', CityViewSet)
router.register(r'profiles', UserProfileViewSet)   

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserListView.as_view(), name='user_list'),
]


