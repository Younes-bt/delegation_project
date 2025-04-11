from django.contrib import admin
from .models import Progress, Attendance, Mark, Submission, Exercise, Course

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'training', 'date', 'session_time')
    list_filter = ('training', 'teacher', 'date')
    search_fields = ('teacher__first_name', 'teacher__last_name', 'training__name')

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
    list_display = ('title', 'course', 'due_date')
    list_filter = ('course', 'due_date')
    search_fields = ('title', 'course__name')   

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'training')
    list_filter = ('training',)
    search_fields = ('name', 'training__name')      


