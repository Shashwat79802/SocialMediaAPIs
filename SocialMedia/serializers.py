from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import UserFriends

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']


class UserFriendsSerializer(serializers.ModelSerializer):
    friend = UserSerializer()

    class Meta:
        model = UserFriends
        fields = ['friend', 'status']
