from django.db import models
from django.conf import settings
from accounts.models import Training, Center, TrainingGroup

# Create your models here.
class AnnualDistribution(models.Model):
    MONTH_CHOICES = [
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    ]
    month = models.IntegerField(choices=MONTH_CHOICES)
    week = models.PositiveIntegerField()
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='annual_distributions')
    training = models.ForeignKey('accounts.Training', on_delete=models.CASCADE, related_name='annual_distributions')
    title = models.CharField(max_length=255)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.teacher.first_name} - {self.title} ({self.get_month_display()} Week {self.week})"


class Exercise(models.Model):
    EXERCISE_TYPE_CHOICES = [
        ('QCM', 'Multiple Choice Question'),
        ('Simple', 'Simple Exercise'),
        ('Project', 'Project Exercise'),
        ('Quiz', 'Quiz'),
    ]

    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    annual_distribution = models.ForeignKey(AnnualDistribution, on_delete=models.CASCADE, related_name='exercises', null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    control = models.ForeignKey('training.Control', on_delete=models.CASCADE, related_name='exercises', null=True, blank=True)
    points = models.PositiveIntegerField(help_text="Points allocated for this exercise in the control", null=True, blank=True)
    exercise_type = models.CharField(max_length=10, choices=EXERCISE_TYPE_CHOICES, default='Simple')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Medium')
    question = models.TextField(blank=True, null=True)
    answer_options = models.JSONField(blank=True, null=True, help_text="Options for QCM exercises")
    correct_answer = models.TextField(blank=True, null=True, help_text="Correct answer for the exercise")
    image = models.ImageField(upload_to='exercise_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    estimated_time = models.PositiveIntegerField(help_text="Estimated time in minutes", null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.annual_distribution.title if self.annual_distribution else 'No Distribution'}"


class Submission(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='submissions')
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)
    feedback = models.TextField(blank=True)

class Progress(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    annual_distribution = models.ForeignKey(AnnualDistribution, on_delete=models.CASCADE, null=True, blank=True)
    training = models.ForeignKey('accounts.Training', on_delete=models.CASCADE)
    session_date = models.DateField()
    session_time = models.TimeField()
    topics_covered = models.TextField()
    feedback = models.TextField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.teacher.first_name} - {self.annual_distribution.title if self.annual_distribution else 'No Distribution'} - {self.session_date}"


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


class Control(models.Model):
    CONTROL_TYPE_CHOICES = [
        ('Midterm', 'Midterm Exam'),
        ('Final', 'Final Exam'),
        ('Quiz', 'Quiz'),
        ('Project', 'Project'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    annual_distribution = models.ForeignKey(AnnualDistribution, on_delete=models.CASCADE, related_name='controls')
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='controls')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='controls')
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name='controls')
    group = models.ForeignKey(TrainingGroup, on_delete=models.CASCADE, related_name='controls')
    control_type = models.CharField(max_length=20, choices=CONTROL_TYPE_CHOICES, default='Quiz')
    total_points = models.PositiveIntegerField(default=20)
    passing_score = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.annual_distribution.title} - {self.teacher.first_name}"
