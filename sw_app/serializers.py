from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from django.utils.translation import gettext as _


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


class LoginUserSerializer(serializers.Serializer):
    """Used to login users with password and validate"""

    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user

        raise serializers.ValidationError(_('Unable to log in with provided credentials'))
