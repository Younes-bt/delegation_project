from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import TimeSlot
from .serializers import TimeSlotSerializer
from accounts.permissions import IsCenterStaff, IsAdmin

# Create your views here.

class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = TimeSlot.objects.all()
        
        # Filter by training
        training_id = self.request.query_params.get('training', None)
        if training_id:
            queryset = queryset.filter(training_id=training_id)
        
        # Filter by teacher
        teacher_id = self.request.query_params.get('teacher', None)
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        
        # Filter by group
        group_id = self.request.query_params.get('group', None)
        if group_id:
            queryset = queryset.filter(group_id=group_id)
        
        # Filter by room
        room_id = self.request.query_params.get('room', None)
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        
        # Filter by day
        day = self.request.query_params.get('day', None)
        if day:
            queryset = queryset.filter(day_of_week=day.upper()[:3])
        
        return queryset

    @action(detail=False, methods=['get'])
    def my_timetable(self, request):
        """Get timetable for the current user based on their role"""
        user = request.user.userprofile
        
        if user.is_teacher:
            # Get teacher's timetable
            timetable = TimeSlot.objects.filter(teacher=user)
        elif user.is_student:
            # Get student's group timetable
            timetable = TimeSlot.objects.filter(group__students=user)
        else:
            return Response(
                {"error": "User must be either a teacher or student"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(timetable, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def check_availability(self, request):
        """Check availability for a specific time slot"""
        day = request.query_params.get('day', '').upper()[:3]
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        teacher_id = request.query_params.get('teacher', None)
        room_id = request.query_params.get('room', None)
        group_id = request.query_params.get('group', None)

        if not all([day, start_time, end_time]):
            return Response(
                {"error": "day, start_time, and end_time are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        conflicts = []
        
        # Check teacher availability
        if teacher_id:
            teacher_conflicts = TimeSlot.objects.filter(
                teacher_id=teacher_id,
                day_of_week=day,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            if teacher_conflicts.exists():
                conflicts.append("Teacher is not available")
        
        # Check room availability
        if room_id:
            room_conflicts = TimeSlot.objects.filter(
                room_id=room_id,
                day_of_week=day,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            if room_conflicts.exists():
                conflicts.append("Room is not available")
        
        # Check group availability
        if group_id:
            group_conflicts = TimeSlot.objects.filter(
                group_id=group_id,
                day_of_week=day,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            if group_conflicts.exists():
                conflicts.append("Group is not available")

        return Response({
            "is_available": len(conflicts) == 0,
            "conflicts": conflicts
        })
