from django.contrib import admin
from .models import Progress, Attendance, Mark, Submission, Exercise, AnnualDistribution, Control

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'training', 'annual_distribution', 'date', 'session_time')
    list_filter = ('training', 'teacher', 'date', 'annual_distribution')
    search_fields = ('teacher__first_name', 'teacher__last_name', 'training__name', 'annual_distribution__title')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'training', 'center', 'teacher', 'date', 'session_time', 'is_present', 'is_late')
    list_filter = ('training', 'center', 'teacher', 'is_present', 'is_late', 'date')
    search_fields = ('student__first_name', 'student__last_name', 'training__name', 'teacher__first_name', 'teacher__last_name')

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'exercise', 'mark', 'feedback')
    list_filter = ('exercise', 'student')
    search_fields = ('student__first_name', 'student__last_name', 'exercise__title')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'submitted_by', 'submission_date', 'status')
    list_filter = ('exercise', 'submitted_by', 'status')
    search_fields = ('exercise__title', 'submitted_by__first_name', 'submitted_by__last_name')  

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'annual_distribution', 'exercise_type', 'difficulty', 'due_date', 'is_active')
    list_filter = ('annual_distribution', 'exercise_type', 'difficulty', 'is_active', 'due_date')
    search_fields = ('title', 'annual_distribution__title', 'description')
    ordering = ('-created_at',)

@admin.register(AnnualDistribution)
class AnnualDistributionAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'training', 'month', 'week')
    list_filter = ('training', 'teacher', 'month')
    search_fields = ('title', 'teacher__first_name', 'teacher__last_name', 'training__name')
    ordering = ('month', 'week')

@admin.register(Control)
class ControlAdmin(admin.ModelAdmin):
    list_display = ('title', 'annual_distribution', 'training', 'teacher', 'control_type', 'is_active')
    list_filter = ('annual_distribution', 'training', 'teacher', 'control_type', 'is_active')
    search_fields = ('title', 'annual_distribution__title', 'training__name', 'teacher__first_name', 'teacher__last_name')
    ordering = ('-created_at',)      


