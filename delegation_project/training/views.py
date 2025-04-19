from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import  Exercise, Progress, Submission, Attendance, Mark, AnnualDistribution
from .serializers import  ExerciseSerializer, ProgressSerializer, SubmissionSerializer, AttendanceSerializer, MarkSerializer, AnnualDistributionSerializer
from rest_framework.views import APIView
# --- Course ViewSet ---


# --- Exercise ViewSet ---
class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


# --- Progress ViewSet ---
class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer


# --- Submission ViewSet ---
class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

# --- Attendance ViewSet ---
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

# --- Mark ViewSet ---
class MarkViewSet(viewsets.ModelViewSet):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer

# --- Annual Distribution ViewSet ---
class AnnualDistributionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        distributions = AnnualDistribution.objects.filter(teacher=request.user)
        serializer = AnnualDistributionSerializer(distributions, many=True)
        return Response(serializer.data)
