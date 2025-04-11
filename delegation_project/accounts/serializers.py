from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Association, Center, Training, City, UserProfile, Room


User = get_user_model()

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
    class Meta:
        model = Training
        fields = '__all__'

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







