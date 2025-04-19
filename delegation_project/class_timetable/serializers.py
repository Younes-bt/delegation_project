from rest_framework import serializers
from .models import TimeSlot

class TimeSlotSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()
    room_name = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()
    training_name = serializers.SerializerMethodField()
    day_name = serializers.SerializerMethodField()

    class Meta:
        model = TimeSlot
        fields = [
            'id', 'training', 'training_name', 'group', 'group_name',
            'teacher', 'teacher_name', 'room', 'room_name', 'subject',
            'day_of_week', 'day_name', 'start_time', 'end_time'
        ]

    def get_teacher_name(self, obj):
        return obj.teacher.get_full_name()

    def get_room_name(self, obj):
        return obj.room.name

    def get_group_name(self, obj):
        return obj.group.name

    def get_training_name(self, obj):
        return obj.training.name

    def get_day_name(self, obj):
        return obj.get_day_of_week_display() 