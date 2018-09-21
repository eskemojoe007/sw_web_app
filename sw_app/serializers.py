from rest_framework import serializers
from .models import User


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['email'],
            password=validated_data['password'])

        return user


class UserSerializer(serializers.ModelSerializer):
    """Return Serializer after user Creation"""
    class Meta:
        model = User
        fields = ('id', 'email')
