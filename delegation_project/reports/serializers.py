from rest_framework import serializers
from .models import AttendanceReport
from accounts.models import UserProfile, Center, Training, TrainingGroup
from accounts.serializers import UserProfileSerializer, CenterSerializer, TrainingSerializer

class TrainingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingGroup
        fields = '__all__'

class AttendanceReportSerializer(serializers.ModelSerializer):
    """Serializer for the AttendanceReport model"""
    student = UserProfileSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.filter(role='STUDENT'),
        source='student',
        write_only=True,
        required=False
    )
    teacher = UserProfileSerializer(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.filter(role='TEACHER'),
        source='teacher',
        write_only=True,
        required=False
    )
    group = TrainingGroupSerializer(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=TrainingGroup.objects.all(),
        source='group',
        write_only=True,
        required=False
    )
    center = CenterSerializer(read_only=True)
    center_id = serializers.PrimaryKeyRelatedField(
        queryset=Center.objects.all(),
        source='center',
        write_only=True,
        required=False
    )
    training = TrainingSerializer(read_only=True)
    training_id = serializers.PrimaryKeyRelatedField(
        queryset=Training.objects.all(),
        source='training',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = AttendanceReport
        fields = [
            'id', 'report_type', 'period', 'start_date', 'end_date', 'generated_at',
            'student', 'student_id', 'teacher', 'teacher_id', 'group', 'group_id',
            'center', 'center_id', 'training', 'training_id',
            'total_sessions', 'attended_sessions', 'attendance_rate',
            'late_sessions', 'excused_absences', 'unexcused_absences',
            'data', 'notes'
        ]
        read_only_fields = [
            'id', 'generated_at', 'total_sessions', 'attended_sessions',
            'attendance_rate', 'late_sessions', 'excused_absences',
            'unexcused_absences', 'data'
        ]
    
    def validate(self, data):
        """
        Validate the report data to ensure proper target selection based on report type
        """
        report_type = data.get('report_type')
        
        # Check if the appropriate target is provided based on report type
        if report_type == 'STUDENT' and not data.get('student'):
            raise serializers.ValidationError("Student report requires a student target")
        elif report_type == 'TEACHER' and not data.get('teacher'):
            raise serializers.ValidationError("Teacher report requires a teacher target")
        elif report_type == 'GROUP' and not data.get('group'):
            raise serializers.ValidationError("Group report requires a group target")
        elif report_type == 'CENTER' and not data.get('center'):
            raise serializers.ValidationError("Center report requires a center target")
        
        # Check if date range is valid
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("End date must be after start date")
        
        return data
    
    def create(self, validated_data):
        """
        Create a new report and calculate statistics
        """
        report = super().create(validated_data)
        report.calculate_statistics()
        return report
    
    def update(self, instance, validated_data):
        """
        Update an existing report and recalculate statistics if necessary
        """
        # Check if any fields that would affect statistics have changed
        stats_fields = ['start_date', 'end_date', 'student', 'teacher', 'group', 'center', 'training']
        if any(field in validated_data for field in stats_fields):
            report = super().update(instance, validated_data)
            report.calculate_statistics()
            return report
        
        return super().update(instance, validated_data) 