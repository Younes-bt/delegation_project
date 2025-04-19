from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, permissions
from .serializers import UserSerializer, AssociationSerializer, CenterSerializer, TrainingSerializer, CitySerializer, UserProfileSerializer, MaterialSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import Association, Center, Training, City, UserProfile, Material, Room
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsAdmin, IsAssociation, IsTeacher, IsStudent, IsCenterStaffForMaterial
from rest_framework.views import APIView

User = get_user_model()

class TeacherTrainingsView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        trainings = Training.objects.filter(userprofile__user=request.user)
        serializer = TrainingSerializer(trainings, many=True)
        return Response(serializer.data)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise permissions.PermissionDenied("Only admin users can create new users.")
        serializer.save()

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

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated, IsCenterStaffForMaterial]
    filterset_fields = ['center', 'room', 'situation']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'situation', 'quantity', 'created_at']
    ordering = ['room', 'title']

    def get_queryset(self):
        queryset = Material.objects.all()
        if self.request.user.role == 'center_staff':
            queryset = queryset.filter(center=self.request.user.userprofile.center)
        return queryset

    def perform_create(self, serializer):
        serializer.save(center=self.request.user.userprofile.center)

    @action(detail=False, methods=['get'])
    def room_inventory(self, request):
        room_id = request.query_params.get('room', None)
        if not room_id:
            return Response(
                {"error": "Room ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            room = Room.objects.get(id=room_id, center=request.user.userprofile.center)
        except Room.DoesNotExist:
            return Response(
                {"error": "Room not found or not authorized"},
                status=status.HTTP_404_NOT_FOUND
            )
        materials = Material.objects.filter(room=room)
        serializer = self.get_serializer(materials, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def center_inventory(self, request):
        materials = Material.objects.filter(center=request.user.userprofile.center)
        serializer = self.get_serializer(materials, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def situation_report(self, request):
        queryset = Material.objects.filter(center=request.user.userprofile.center)
        report = {}
        for situation, _ in Material.SITUATION_CHOICES:
            count = queryset.filter(situation=situation).count()
            report[situation] = count
        return Response(report)
