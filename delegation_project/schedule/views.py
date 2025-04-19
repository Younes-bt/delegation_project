from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from .models import ScheduleEntry, TeacherAvailability, Holiday
from .serializers import ScheduleEntrySerializer, TeacherAvailabilitySerializer, HolidaySerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny 
from accounts.permissions import IsCenterStaff, IsAdmin
from accounts.models import UserProfile, Training, Center, Room, TrainingGroup
# Create your views here.

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = ScheduleEntry.objects.all()
    serializer_class = ScheduleEntrySerializer


class ScheduleEntryViewSet(viewsets.ModelViewSet):
    queryset = ScheduleEntry.objects.all()
    serializer_class = ScheduleEntrySerializer
    permission_classes = [IsAdmin, IsCenterStaff]

    def get_queryset(self):
        queryset = ScheduleEntry.objects.all()
        
        # Filter by center
        center_id = self.request.query_params.get('center', None)
        if center_id:
            queryset = queryset.filter(center_id=center_id)
        
        # Filter by training
        training_id = self.request.query_params.get('training', None)
        if training_id:
            queryset = queryset.filter(training_id=training_id)
        
        # Filter by teacher
        teacher_id = self.request.query_params.get('teacher', None)
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        
        # Filter by room
        room_id = self.request.query_params.get('room', None)
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        
        # Filter by group
        group_id = self.request.query_params.get('group', None)
        if group_id:
            queryset = queryset.filter(group_id=group_id)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        
        # Filter active schedules
        active_only = self.request.query_params.get('active_only', None)
        if active_only:
            queryset = queryset.filter(is_active=True)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def my_schedule(self, request):
        """Get schedule for the current user based on their role"""
        user_profile = request.user.userprofile
        
        if user_profile.is_teacher:
            # Get teacher's schedule
            schedule = ScheduleEntry.objects.filter(teacher=request.user)
        elif user_profile.is_student:
            # Get student's group schedule
            student_groups = TrainingGroup.objects.filter(students=request.user)
            schedule = ScheduleEntry.objects.filter(group__in=student_groups)
        else:
            return Response({"error": "User must be either a teacher or student"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(schedule, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def generate_recurring(self, request):
        """Generate recurring schedule entries"""
        schedule_data = request.data
        serializer = self.get_serializer(data=schedule_data)
        
        if serializer.is_valid():
            # Create the parent schedule
            parent_schedule = serializer.save(created_by=request.user.userprofile)
            
            # Generate recurring entries
            recurring_entries = parent_schedule.generate_recurring_entries()
            
            # Serialize the generated entries
            result_serializer = self.get_serializer(recurring_entries, many=True)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def create_exception(self, request, pk=None):
        """Create an exception for a recurring schedule"""
        parent_schedule = self.get_object()
        
        if not parent_schedule.is_recurring:
            return Response({"error": "Can only create exceptions for recurring schedules"},
                          status=status.HTTP_400_BAD_REQUEST)
        
        exception_data = request.data
        exception_data['parent_schedule'] = parent_schedule.id
        exception_data['is_exception'] = True
        
        serializer = self.get_serializer(data=exception_data)
        if serializer.is_valid():
            serializer.save(created_by=request.user.userprofile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeacherAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = TeacherAvailability.objects.all()
    serializer_class = TeacherAvailabilitySerializer
    
    def get_queryset(self):
        queryset = TeacherAvailability.objects.all()
        
        # Filter by teacher
        teacher_id = self.request.query_params.get('teacher', None)
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        
        # Filter by day of week
        day_of_week = self.request.query_params.get('day_of_week', None)
        if day_of_week:
            queryset = queryset.filter(day_of_week=day_of_week)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['center']
    search_fields = ['name', 'description']
    ordering_fields = ['start_date', 'end_date', 'name']
    ordering = ['start_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)
            
        return queryset
