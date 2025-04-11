
from django.contrib import admin
from django.urls import path, include
from accounts.views import UserCreateView, UserDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('accounts/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/users/signup/', UserCreateView.as_view(), name='user_create'),
    path('accounts/users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('accounts/auth/', include('rest_framework.urls')),
    path('accounts/', include('accounts.urls')),
    path('training/', include('training.urls')),
]
