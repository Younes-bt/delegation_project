from rest_framework import serializers
from .models import ScheduleEntry

class ScheduleEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleEntry
        fields = '__all__'

    def validate(self, data):
        start = data['start_time']
        end = data['end_time']
        teacher = data['teacher']
        training = data['training']
        room = data['room']

        # Check teacher conflict
        if ScheduleEntry.objects.filter(teacher=teacher, start_time__lt=end, end_time__gt=start).exists():
            raise serializers.ValidationError("Teacher has another class during this time.")

        # Check student group conflict (same training)
        if ScheduleEntry.objects.filter(training=training, start_time__lt=end, end_time__gt=start).exists():
            raise serializers.ValidationError("Training already scheduled during this time.")

        # Check room conflict
        if ScheduleEntry.objects.filter(room=room, start_time__lt=end, end_time__gt=start).exists():
            raise serializers.ValidationError("Room is already occupied during this time.")
        


        return data
 