from django.contrib import admin
from .models import AttendanceReport

@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'period', 'start_date', 'end_date', 'generated_at', 'attendance_rate')
    list_filter = ('report_type', 'period', 'start_date', 'end_date')
    search_fields = ('notes', 'student__email', 'teacher__email', 'group__name', 'center__name')
    readonly_fields = ('generated_at', 'total_sessions', 'attended_sessions', 'attendance_rate', 
                      'late_sessions', 'excused_absences', 'unexcused_absences', 'data')
    fieldsets = (
        ('Basic Information', {
            'fields': ('report_type', 'period', 'start_date', 'end_date', 'generated_at')
        }),
        ('Report Target', {
            'fields': ('student', 'teacher', 'group', 'center', 'training')
        }),
        ('Statistics', {
            'fields': ('total_sessions', 'attended_sessions', 'attendance_rate', 
                      'late_sessions', 'excused_absences', 'unexcused_absences')
        }),
        ('Additional Data', {
            'fields': ('data', 'notes')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """
        Override save_model to calculate statistics when saving
        """
        if not change:  # Only calculate statistics for new reports
            obj.calculate_statistics()
        super().save_model(request, obj, form, change)
