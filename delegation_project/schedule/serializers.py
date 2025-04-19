from rest_framework import serializers
from .models import ScheduleEntry, TeacherAvailability, Holiday
from accounts.models import Training, Center, UserProfile, Room, TrainingGroup

class TeacherAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAvailability
        fields = '__all__'
    
    def validate(self, data):
        # Check if the teacher exists and is a teacher
        teacher = data.get('teacher')
        if not teacher or not teacher.is_teacher:
            raise serializers.ValidationError("Selected user must be a teacher")
        
        # Check for overlapping availability entries
        overlapping = TeacherAvailability.objects.filter(
            teacher=teacher,
            day_of_week=data['day_of_week'],
            start_time__lt=data['end_time'],
            end_time__gt=data['start_time']
        )
        if self.instance:
            overlapping = overlapping.exclude(id=self.instance.id)
        
        if overlapping.exists():
            raise serializers.ValidationError("This time slot overlaps with another availability entry")
        
        return data

class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ['id', 'name', 'start_date', 'end_date', 'is_recurring', 'description', 'center']
        read_only_fields = ['id']

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data

class ScheduleEntrySerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()
    room_name = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()
    conflicts = serializers.SerializerMethodField()
    
    class Meta:
        model = ScheduleEntry
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by')
    
    def get_teacher_name(self, obj):
        return obj.teacher.get_full_name() if obj.teacher else None
    
    def get_room_name(self, obj):
        return obj.room.name if obj.room else None
    
    def get_group_name(self, obj):
        return obj.group.name if obj.group else None
    
    def get_conflicts(self, obj):
        conflicts = []
        
        # Check teacher availability
        if not obj.check_teacher_availability():
            conflicts.append("Teacher has a scheduling conflict")
        
        # Check room availability
        if not obj.check_room_availability():
            conflicts.append("Room has a scheduling conflict")
        
        # Check group availability
        if not obj.check_group_availability():
            conflicts.append("Group has a scheduling conflict")
        
        # Check if date falls on a holiday
        if obj.exception_date:
            holiday = Holiday.objects.filter(date=obj.exception_date).first()
            if holiday:
                conflicts.append(f"Date falls on holiday: {holiday.name}")
        
        return conflicts
    
    def validate(self, data):
        # Validate time slots
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time")
        
        # Validate teacher
        teacher = data.get('teacher')
        if teacher and not teacher.is_teacher:
            raise serializers.ValidationError("Selected user must be a teacher")
        
        # Validate room belongs to the center
        room = data.get('room')
        center = data.get('center')
        if room and room.center != center:
            raise serializers.ValidationError("Room must belong to the selected center")
        
        # Validate group belongs to the training
        group = data.get('group')
        training = data.get('training')
        if group and group.training != training:
            raise serializers.ValidationError("Group must belong to the selected training")
        
        # Check for conflicts
        if not data.get('check_teacher_availability', True):
            raise serializers.ValidationError("Teacher has a scheduling conflict")
        
        if not data.get('check_room_availability', True):
            raise serializers.ValidationError("Room has a scheduling conflict")
        
        if not data.get('check_group_availability', True):
            raise serializers.ValidationError("Group has a scheduling conflict")
        
        # Validate recurrence
        if data.get('is_recurring'):
            if data.get('recurrence_type') == 'none':
                raise serializers.ValidationError("Recurrence type must be specified for recurring schedules")
            if not data.get('recurrence_end_date'):
                raise serializers.ValidationError("Recurrence end date must be specified for recurring schedules")
        
        # Validate exceptions
        if data.get('is_exception'):
            if not data.get('parent_schedule'):
                raise serializers.ValidationError("Exception must have a parent schedule")
            if not data.get('exception_date'):
                raise serializers.ValidationError("Exception must have an exception date")
        
        return data
    
    def create(self, validated_data):
        # Set the created_by field to the current user
        validated_data['created_by'] = self.context['request'].user.userprofile
        return super().create(validated_data)
 