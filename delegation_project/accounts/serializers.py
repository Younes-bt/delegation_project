from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Association, Center, Training, City, UserProfile

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

class UserProfileSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    association = AssociationSerializer(read_only=True)
    center = CenterSerializer(read_only=True)
    training = TrainingSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'






