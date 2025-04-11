from django.shortcuts import render
from rest_framework import viewsets
from .models import ScheduleEntry
from .serializers import ScheduleEntrySerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny 
from accounts.permissions import IsCenterStaff, IsAdmin
# Create your views here.

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = ScheduleEntry.objects.all()
    serializer_class = ScheduleEntrySerializer


class ScheduleEntryViewSet(viewsets.ModelViewSet):
    queryset = ScheduleEntry.objects.all()
    serializer_class = ScheduleEntrySerializer
    permission_classes = [IsAdmin, IsCenterStaff]

    def perform_create(self, serializer):
        serializer.save()
