from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta
from .models import AttendanceReport
from .serializers import AttendanceReportSerializer
from accounts.models import UserProfile, Center, Training, TrainingGroup
from django.db import models

class AttendanceReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing attendance reports.
    """
    queryset = AttendanceReport.objects.all()
    serializer_class = AttendanceReportSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['report_type', 'period', 'student', 'teacher', 'group', 'center', 'training']
    search_fields = ['notes']
    ordering_fields = ['generated_at', 'start_date', 'end_date', 'attendance_rate']
    ordering = ['-generated_at']
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions and role
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        # Superusers can see all reports
        if user.is_superuser:
            return queryset
        
        # Center managers can see reports for their center
        if user.role == 'CENTER_MANAGER':
            return queryset.filter(center=user.center)
        
        # Teachers can see their own reports and reports for their students
        if user.role == 'TEACHER':
            return queryset.filter(
                models.Q(teacher=user) | 
                models.Q(student__in=user.students.all())
            )
        
        # Students can only see their own reports
        if user.role == 'STUDENT':
            return queryset.filter(student=user)
        
        return queryset.none()
    
    @action(detail=False, methods=['get'])
    def my_reports(self, request):
        """
        Get reports specific to the requesting user
        """
        user = request.user
        queryset = self.get_queryset()
        
        if user.role == 'TEACHER':
            queryset = queryset.filter(teacher=user)
        elif user.role == 'STUDENT':
            queryset = queryset.filter(student=user)
        else:
            return Response(
                {"detail": "This endpoint is only available for teachers and students"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def generate_report(self, request):
        """
        Generate a new report based on the provided parameters
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            report = serializer.save()
            return Response(
                self.get_serializer(report).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def quick_stats(self, request):
        """
        Get quick statistics for the current period
        """
        user = request.user
        today = timezone.now().date()
        
        # Default to last 30 days if no date range provided
        start_date = request.query_params.get('start_date', today - timedelta(days=30))
        end_date = request.query_params.get('end_date', today)
        
        queryset = self.get_queryset().filter(
            start_date__gte=start_date,
            end_date__lte=end_date
        )
        
        # Calculate aggregate statistics
        stats = {
            'total_reports': queryset.count(),
            'average_attendance_rate': queryset.aggregate(
                avg_rate=models.Avg('attendance_rate')
            )['avg_rate'] or 0,
            'total_sessions': queryset.aggregate(
                total=models.Sum('total_sessions')
            )['total'] or 0,
            'attended_sessions': queryset.aggregate(
                attended=models.Sum('attended_sessions')
            )['attended'] or 0,
        }
        
        return Response(stats)
    
    @action(detail=True, methods=['post'])
    def recalculate(self, request, pk=None):
        """
        Recalculate statistics for a specific report
        """
        report = self.get_object()
        report.calculate_statistics()
        return Response(self.get_serializer(report).data)
    
    @action(detail=False, methods=['get'])
    def export(self, request):
        """
        Export reports in various formats (CSV, Excel, etc.)
        """
        # Implementation for report export
        # This would typically involve generating a file and returning it as a response
        pass
