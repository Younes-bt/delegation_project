from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Create your models here.


class CustomUser(AbstractUser):
    username = None 
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('association_staff', 'Association_staff'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('center_staff', 'Center_staff'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    USERNAME_FIELD = 'email'  # <-- this is the key
    REQUIRED_FIELDS = ['first_name', 'last_name']  # any additional fields

    objects = CustomUserManager()

    def __str__(self):
        return self.email

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
)

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('association', 'Association'),
    ('teacher', 'Teacher'),
    ('student', 'Student'),
    ('center_staff', 'Center_staff'),
)

GROUP_CHOICES = (
    ('group_1', 'Group 1'),
    ('group_2', 'Group 2'),
    ('group_3', 'Group 3'),
    ('group_4', 'Group 4'),
    ('group_5', 'Group 5'),
    ('group_6', 'Group 6'),
    ('group_7', 'Group 7'),
    ('group_8', 'Group 8'),
    ('group_9', 'Group 9'),
)

class City(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Association(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    president = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Center(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    association = models.ForeignKey(Association, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " | " + self.association.name
    
class Training(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class TrainingGroup(models.Model):
    name = models.CharField(max_length=50)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    center = models.ForeignKey(Center, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.training.name} @ {self.center.name}"

class Room(models.Model):
    name = models.CharField(max_length=100)
    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name='rooms')
    capacity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Room: {self.name} - {self.center.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    association = models.ForeignKey(Association, on_delete=models.CASCADE, null=True, blank=True)
    center = models.ForeignKey(Center, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    training = models.ForeignKey(Training, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(TrainingGroup, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.role} : {self.first_name} {self.last_name}"

class Material(models.Model):
    SITUATION_CHOICES = [
        ('GOOD', 'Good'),
        ('FAIR', 'Fair'),
        ('POOR', 'Poor'),
        ('BROKEN', 'Broken'),
        ('MAINTENANCE', 'Under Maintenance'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='materials/', blank=True, null=True)
    situation = models.CharField(max_length=20, choices=SITUATION_CHOICES, default='GOOD')
    quantity = models.PositiveIntegerField(default=1)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='materials')
    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name='materials')
    purchase_date = models.DateField(blank=True, null=True)
    last_maintenance_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['room', 'title']
        verbose_name_plural = "Materials"

    def __str__(self):
        return f"{self.title} - {self.room.name} ({self.get_situation_display()})"

    def clean(self):
        # Ensure the room belongs to the selected center
        if self.room.center != self.center:
            raise ValidationError("Room must belong to the selected center")



