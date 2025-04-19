from django.contrib import admin
from .models import TimeSlot

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('subject', 'training', 'group', 'teacher', 'room', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('training', 'teacher', 'room', 'day_of_week')
    search_fields = ('subject', 'teacher__first_name', 'teacher__last_name', 'group__name')
    ordering = ('day_of_week', 'start_time')
