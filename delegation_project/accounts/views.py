from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, permissions
from .serializers import UserSerializer, AssociationSerializer, CenterSerializer, TrainingSerializer, CitySerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Association, Center, Training, City, UserProfile
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsAdmin, IsAssociation, IsTeacher, IsStudent

User = get_user_model()

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class AssociationViewSet(viewsets.ModelViewSet):
    queryset = Association.objects.all()
    serializer_class = AssociationSerializer
    permission_classes = [IsAdmin]

class CenterViewSet(viewsets.ModelViewSet):
    queryset = Center.objects.all()
    serializer_class = CenterSerializer
    permission_classes = [IsAdmin | IsAssociation]  

class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = [IsAdmin]  

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdmin]  

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related('user', 'city', 'association', 'center', 'training')
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]        

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return UserProfile.objects.all()
        elif user.role == 'association_staff':
            return UserProfile.objects.filter(association=user.association)
        elif user.role == 'teacher':
            return UserProfile.objects.filter(training=user.training)
        elif user.role == 'student':
            return UserProfile.objects.filter(user=user)
        return UserProfile.objects.none()
    
    def perform_create(self, serializer):
        user = self.request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        if not created:
            serializer.update(profile, serializer.validated_data)
        else:
            serializer.save(user=user)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=404)










