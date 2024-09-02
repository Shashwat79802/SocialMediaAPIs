from django.contrib.auth.models import update_last_login
from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class SignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'password']
        extra_kwargs = {'password': {'write_only': True}, 'full_name': {'required': False}}

    def create(self, validated_data):
        validated_data['email'] = validated_data['email'].lower()
        user = User.objects.create_user(**validated_data)
        return user


class LoginInSerializer(Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email').lower()
        password = data.get('password')

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid credentials')

        update_last_login(None, user)  # Optionally update the last login time

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }