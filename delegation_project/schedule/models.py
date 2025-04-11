from django.db import models
from accounts.models import Training, Center, UserProfile
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

    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    group = models.ForeignKey('accounts.TrainingGroup', on_delete=models.CASCADE)
    teacher = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='teaching_schedules')
    subject = models.CharField(max_length=255)
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.ForeignKey('accounts.Room', on_delete=models.SET_NULL, null=True, related_name='schedule_entries')

    class Meta:
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.subject} - {self.group} - {self.day_of_week} {self.start_time} to {self.end_time}"