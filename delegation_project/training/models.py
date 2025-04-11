from django.db import models
from django.conf import settings

# Create your models here.
class Course(models.Model):
    training = models.ForeignKey('accounts.Training', on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exercises')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Submission(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='submissions')
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)
    feedback = models.TextField(blank=True)

class Progress(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('training.Course', on_delete=models.CASCADE)
    training = models.ForeignKey('accounts.Training', on_delete=models.CASCADE)
    session_date = models.DateField()
    session_time = models.TimeField()
    topics_covered = models.TextField()
    feedback = models.TextField(blank=True, null=True)
    date = models.DateField()


    def __str__(self):
        return f"{self.teacher.first_name} - {self.course.name} - {self.session_date}"


class Mark(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    mark = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.first_name} - {self.exercise.title} - {self.mark}"       

class Attendance(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_attendances') 
    training = models.ForeignKey('accounts.Training', on_delete=models.CASCADE)
    center = models.ForeignKey('accounts.Center', on_delete=models.CASCADE)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_attendances')
    date = models.DateField()
    session_time = models.TimeField()
    is_present = models.BooleanField(default=False)
    is_late = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.first_name} - {self.training.name} - {self.date}"
