from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Association, Center, Training, City, UserProfile, Room, Material
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
User = get_user_model()
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role  # Add role to token
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user 

class AssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Association
        fields = '__all__'

class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = '__all__'

class TrainingSerializer(serializers.ModelSerializer):
    center = serializers.StringRelatedField()  # Returns center.name
    class Meta:
        model = Training
        fields = ['id', 'name', 'description', 'is_active', 'center']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'    

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'center', 'capacity']

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True) 

    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), source='city', write_only=True, required=False
    )

    association = AssociationSerializer(read_only=True)
    association_id = serializers.PrimaryKeyRelatedField(
        queryset=Association.objects.all(), source='association', write_only=True, required=False
    )

    center = CenterSerializer(read_only=True)
    center_id = serializers.PrimaryKeyRelatedField(
        queryset=Center.objects.all(), source='center', write_only=True, required=False
    )

    training = TrainingSerializer(read_only=True)
    training_id = serializers.PrimaryKeyRelatedField(
        queryset=Training.objects.all(), source='training', write_only=True, required=False
    )

    class Meta:
        model = UserProfile
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    room_name = serializers.SerializerMethodField()
    center_name = serializers.SerializerMethodField()
    situation_display = serializers.SerializerMethodField()
    center = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Material
        fields = [
            'id', 'title', 'description', 'picture', 'situation', 'situation_display',
            'quantity', 'room', 'room_name', 'center', 'center_name',
            'purchase_date', 'last_maintenance_date', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'center']

    def get_room_name(self, obj):
        return obj.room.name

    def get_center_name(self, obj):
        return obj.center.name

    def get_situation_display(self, obj):
        return obj.get_situation_display()

    def validate_room(self, value):
        # Ensure the room belongs to the user's center
        request = self.context.get('request')
        if request and request.user.role == 'center_staff':
            if value.center != request.user.userprofile.center:
                raise serializers.ValidationError("You can only add materials to rooms in your center")
        return value







