from rest_framework import serializers
from .models import Exercise, Progress, Submission, Mark, Attendance, AnnualDistribution, Control

# --- Exercise Serializer ---
class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'


# --- Progress Serializer ---
class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = '__all__'


# --- Submission Serializer ---
class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'


# --- Mark Serializer ---
class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = '__all__'  


# --- Attendance Serializer ---
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


# --- Annual Distribution Serializer ---

class AnnualDistributionSerializer(serializers.ModelSerializer):
    training = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()  # Optional: display teacher name
    month_display = serializers.CharField(source='get_month_display', read_only=True)

    class Meta:
        model = AnnualDistribution
        fields = ['id', 'month', 'month_display', 'week', 'teacher', 'training', 'title', 'details']

# --- Control Serializer ---
class ControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Control
        fields = '__all__'





