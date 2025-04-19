from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import Training, Center, UserProfile, Room, TrainingGroup
from django.utils import timezone

class TimeSlot(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

    # Basic information
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    group = models.ForeignKey(TrainingGroup, on_delete=models.CASCADE)
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='teaching_slots')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)

    # Time information
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK, default='MON')
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)

    class Meta:
        ordering = ['day_of_week', 'start_time']
        # Ensure we don't double-book teachers or rooms
        constraints = [
            models.UniqueConstraint(
                fields=['teacher', 'day_of_week', 'start_time'],
                name='unique_teacher_timeslot'
            ),
            models.UniqueConstraint(
                fields=['room', 'day_of_week', 'start_time'],
                name='unique_room_timeslot'
            ),
            models.UniqueConstraint(
                fields=['group', 'day_of_week', 'start_time'],
                name='unique_group_timeslot'
            )
        ]

    def __str__(self):
        return f"{self.subject} - {self.group} - {self.get_day_of_week_display()} {self.start_time.strftime('%H:%M')}"

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")
        
        # Check for overlapping slots for teacher
        teacher_conflicts = TimeSlot.objects.filter(
            teacher=self.teacher,
            day_of_week=self.day_of_week,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)
        
        if teacher_conflicts.exists():
            raise ValidationError("Teacher is already booked during this time slot")

        # Check for overlapping slots for room
        room_conflicts = TimeSlot.objects.filter(
            room=self.room,
            day_of_week=self.day_of_week,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)
        
        if room_conflicts.exists():
            raise ValidationError("Room is already booked during this time slot")

        # Check for overlapping slots for group
        group_conflicts = TimeSlot.objects.filter(
            group=self.group,
            day_of_week=self.day_of_week,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)
        
        if group_conflicts.exists():
            raise ValidationError("Group is already booked during this time slot")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
