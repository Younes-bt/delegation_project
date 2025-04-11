from django.contrib import admin
from .models import ScheduleEntry
from accounts.models import Room
from django.contrib.admin import ModelAdmin

@admin.register(ScheduleEntry)
class ScheduleEntryAdmin(admin.ModelAdmin):
    list_display = ('subject', 'group', 'teacher', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'group', 'teacher', 'center')
    search_fields = ('subject', 'teacher__user__full_name', 'group__name')


class RoomAdmin(ModelAdmin):
    list_display = ('name', 'center', 'capacity')

admin.site.register(Room, RoomAdmin)
