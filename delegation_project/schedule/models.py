from django.db import models
from accounts.models import Training, Center, UserProfile
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

# Create your models here.
class ScheduleEntry(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

    RECURRENCE_CHOICES = [
        ('none', 'No Recurrence'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    group = models.ForeignKey('accounts.TrainingGroup', on_delete=models.CASCADE)
    teacher = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='teaching_schedules')
    subject = models.CharField(max_length=255)
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.ForeignKey('accounts.Room', on_delete=models.SET_NULL, null=True, related_name='schedule_entries')
    
    # Recurrence fields
    is_recurring = models.BooleanField(default=False)
    recurrence_type = models.CharField(max_length=10, choices=RECURRENCE_CHOICES, default='none')
    recurrence_end_date = models.DateField(null=True, blank=True)
    
    # Status fields
    is_active = models.BooleanField(default=True)
    is_exception = models.BooleanField(default=False)
    parent_schedule = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='exceptions')
    exception_date = models.DateField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='created_schedules')

    class Meta:
        ordering = ['day_of_week', 'start_time']
        verbose_name_plural = "Schedule Entries"

    def __str__(self):
        return f"{self.subject} - {self.group} - {self.day_of_week} {self.start_time} to {self.end_time}"
    
    def clean(self):
        # Validate that end_time is after start_time
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")
        
        # Validate recurrence fields
        if self.is_recurring and self.recurrence_type == 'none':
            raise ValidationError("Recurrence type must be specified for recurring schedules")
        
        if self.is_recurring and not self.recurrence_end_date:
            raise ValidationError("Recurrence end date must be specified for recurring schedules")
        
        # Validate exception fields
        if self.is_exception and not self.parent_schedule:
            raise ValidationError("Exception must have a parent schedule")
        
        if self.is_exception and not self.exception_date:
            raise ValidationError("Exception must have an exception date")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def check_teacher_availability(self):
        """Check if the teacher is available during this time slot"""
        if not self.teacher:
            return True
        
        # Get all schedule entries for this teacher on this day
        conflicting_entries = ScheduleEntry.objects.filter(
            teacher=self.teacher,
            day_of_week=self.day_of_week,
            is_active=True
        ).exclude(id=self.id)
        
        # Check for time conflicts
        for entry in conflicting_entries:
            if (self.start_time < entry.end_time and self.end_time > entry.start_time):
                return False
        
        return True
    
    def check_room_availability(self):
        """Check if the room is available during this time slot"""
        if not self.room:
            return True
        
        # Get all schedule entries for this room on this day
        conflicting_entries = ScheduleEntry.objects.filter(
            room=self.room,
            day_of_week=self.day_of_week,
            is_active=True
        ).exclude(id=self.id)
        
        # Check for time conflicts
        for entry in conflicting_entries:
            if (self.start_time < entry.end_time and self.end_time > entry.start_time):
                return False
        
        return True
    
    def check_group_availability(self):
        """Check if the group is available during this time slot"""
        # Get all schedule entries for this group on this day
        conflicting_entries = ScheduleEntry.objects.filter(
            group=self.group,
            day_of_week=self.day_of_week,
            is_active=True
        ).exclude(id=self.id)
        
        # Check for time conflicts
        for entry in conflicting_entries:
            if (self.start_time < entry.end_time and self.end_time > entry.start_time):
                return False
        
        return True
    
    def generate_recurring_entries(self):
        """Generate recurring schedule entries based on this entry"""
        if not self.is_recurring or self.recurrence_type == 'none':
            return []
        
        # This would be implemented in a task or management command
        # For now, we'll just return an empty list
        return []


class TeacherAvailability(models.Model):
    """Model to track teacher availability outside of regular schedules"""
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='availability')
    day_of_week = models.CharField(max_length=3, choices=ScheduleEntry.DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    note = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Teacher Availabilities"
        unique_together = ['teacher', 'day_of_week', 'start_time', 'end_time']
    
    def __str__(self):
        status = "Available" if self.is_available else "Unavailable"
        return f"{self.teacher} - {self.day_of_week} {self.start_time} to {self.end_time} - {status}"
    
    def clean(self):
        # Validate that end_time is after start_time
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Holiday(models.Model):
    """Model to track holidays and special dates"""
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_recurring = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    center = models.ForeignKey('accounts.Center', on_delete=models.CASCADE, related_name='holidays')

    class Meta:
        verbose_name_plural = "Holidays"
        ordering = ['start_date']

    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("End date must be after start date")