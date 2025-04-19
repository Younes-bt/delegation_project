from django.db import models
from django.db.models import Avg, Count, Q
from django.utils import timezone
from accounts.models import UserProfile, Center, Training, TrainingGroup
from training.models import Attendance

class AttendanceReport(models.Model):
    REPORT_TYPES = [
        ('STUDENT', 'Student Report'),
        ('TEACHER', 'Teacher Report'),
        ('GROUP', 'Group Report'),
        ('CENTER', 'Center Report'),
    ]

    PERIOD_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('CUSTOM', 'Custom Range'),
    ]

    # Basic information
    report_type = models.CharField(max_length=10, choices=REPORT_TYPES)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    generated_at = models.DateTimeField(auto_now_add=True)

    # Report targets (optional based on report type)
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='student_attendance_reports')
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='teacher_attendance_reports')
    group = models.ForeignKey(TrainingGroup, on_delete=models.CASCADE, null=True, blank=True, related_name='group_attendance_reports')
    center = models.ForeignKey(Center, on_delete=models.CASCADE, null=True, blank=True, related_name='center_attendance_reports')
    training = models.ForeignKey(Training, on_delete=models.CASCADE, null=True, blank=True, related_name='training_attendance_reports')

    # Report statistics
    total_sessions = models.IntegerField(default=0)
    attended_sessions = models.IntegerField(default=0)
    attendance_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Percentage
    late_sessions = models.IntegerField(default=0)
    excused_absences = models.IntegerField(default=0)
    unexcused_absences = models.IntegerField(default=0)

    # Additional data
    data = models.JSONField(default=dict)  # For storing detailed statistics
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['report_type', 'start_date', 'end_date']),
            models.Index(fields=['student', 'start_date']),
            models.Index(fields=['teacher', 'start_date']),
            models.Index(fields=['group', 'start_date']),
            models.Index(fields=['center', 'start_date']),
        ]

    def __str__(self):
        target = self.student or self.teacher or self.group or self.center
        return f"{self.get_report_type_display()} - {target} ({self.start_date} to {self.end_date})"

    def calculate_statistics(self):
        """Calculate attendance statistics based on report type"""
        queryset = Attendance.objects.filter(
            date__range=(self.start_date, self.end_date)
        )

        if self.student:
            queryset = queryset.filter(student=self.student)
        elif self.teacher:
            queryset = queryset.filter(schedule__teacher=self.teacher)
        elif self.group:
            queryset = queryset.filter(student__groups=self.group)
        elif self.center:
            queryset = queryset.filter(student__center=self.center)

        if self.training:
            queryset = queryset.filter(schedule__training=self.training)

        # Calculate basic statistics
        total = queryset.count()
        attended = queryset.filter(status='PRESENT').count()
        late = queryset.filter(status='LATE').count()
        excused = queryset.filter(status='EXCUSED').count()
        unexcused = queryset.filter(status='ABSENT').count()

        # Update model fields
        self.total_sessions = total
        self.attended_sessions = attended
        self.late_sessions = late
        self.excused_absences = excused
        self.unexcused_absences = unexcused
        self.attendance_rate = (attended / total * 100) if total > 0 else 0

        # Calculate additional statistics based on report type
        if self.report_type == 'STUDENT':
            self.data = self._calculate_student_statistics(queryset)
        elif self.report_type == 'TEACHER':
            self.data = self._calculate_teacher_statistics(queryset)
        elif self.report_type == 'GROUP':
            self.data = self._calculate_group_statistics(queryset)
        elif self.report_type == 'CENTER':
            self.data = self._calculate_center_statistics(queryset)

        self.save()

    def _calculate_student_statistics(self, queryset):
        """Calculate detailed statistics for student reports"""
        return {
            'attendance_by_subject': dict(
                queryset.values('schedule__subject')
                .annotate(
                    total=Count('id'),
                    present=Count('id', filter=Q(status='PRESENT')),
                    rate=models.ExpressionWrapper(
                        models.F('present') * 100.0 / models.F('total'),
                        output_field=models.FloatField()
                    )
                )
                .values_list('schedule__subject', 'rate')
            ),
            'attendance_by_day': dict(
                queryset.values('date__week_day')
                .annotate(
                    total=Count('id'),
                    present=Count('id', filter=Q(status='PRESENT')),
                    rate=models.ExpressionWrapper(
                        models.F('present') * 100.0 / models.F('total'),
                        output_field=models.FloatField()
                    )
                )
                .values_list('date__week_day', 'rate')
            ),
            'monthly_trend': dict(
                queryset.values('date__month')
                .annotate(
                    rate=models.ExpressionWrapper(
                        Count('id', filter=Q(status='PRESENT')) * 100.0 / Count('id'),
                        output_field=models.FloatField()
                    )
                )
                .values_list('date__month', 'rate')
            )
        }

    def _calculate_teacher_statistics(self, queryset):
        """Calculate detailed statistics for teacher reports"""
        return {
            'class_attendance_rates': dict(
                queryset.values('schedule__id', 'schedule__subject')
                .annotate(
                    total=Count('id'),
                    present=Count('id', filter=Q(status='PRESENT')),
                    rate=models.ExpressionWrapper(
                        models.F('present') * 100.0 / models.F('total'),
                        output_field=models.FloatField()
                    )
                )
                .values_list('schedule__subject', 'rate')
            ),
            'student_attendance': dict(
                queryset.values('student__id', 'student__first_name', 'student__last_name')
                .annotate(
                    total=Count('id'),
                    present=Count('id', filter=Q(status='PRESENT')),
                    rate=models.ExpressionWrapper(
                        models.F('present') * 100.0 / models.F('total'),
                        output_field=models.FloatField()
                    )
                )
                .values_list('student__email', 'rate')
            )
        }

    def _calculate_group_statistics(self, queryset):
        """Calculate detailed statistics for group reports"""
        return {
            'overall_attendance': dict(
                queryset.values('date')
                .annotate(
                    total=Count('id'),
                    present=Count('id', filter=Q(status='PRESENT')),
                    rate=models.ExpressionWrapper(
                        models.F('present') * 100.0 / models.F('total'),
                        output_field=models.FloatField()
                    )
                )
                .values_list('date', 'rate')
            ),
            'student_comparison': dict(
                queryset.values('student__email')
                .annotate(
                    rate=models.ExpressionWrapper(
                        Count('id', filter=Q(status='PRESENT')) * 100.0 / Count('id'),
                        output_field=models.FloatField()
                    )
                )
                .values_list('student__email', 'rate')
            )
        }

    def _calculate_center_statistics(self, queryset):
        """Calculate detailed statistics for center reports"""
        return {
            'group_rates': dict(
                queryset.values('student__groups__name')
                .annotate(
                    rate=models.ExpressionWrapper(
                        Count('id', filter=Q(status='PRESENT')) * 100.0 / Count('id'),
                        output_field=models.FloatField()
                    )
                )
                .values_list('student__groups__name', 'rate')
            ),
            'training_rates': dict(
                queryset.values('schedule__training__name')
                .annotate(
                    rate=models.ExpressionWrapper(
                        Count('id', filter=Q(status='PRESENT')) * 100.0 / Count('id'),
                        output_field=models.FloatField()
                    )
                )
                .values_list('schedule__training__name', 'rate')
            ),
            'daily_rates': dict(
                queryset.values('date')
                .annotate(
                    rate=models.ExpressionWrapper(
                        Count('id', filter=Q(status='PRESENT')) * 100.0 / Count('id'),
                        output_field=models.FloatField()
                    )
                )
                .values_list('date', 'rate')
            )
        }
