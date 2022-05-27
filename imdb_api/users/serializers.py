from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'name']

    email = serializers.CharField(required=True, max_length=50)
    name = serializers.CharField(required=True, max_length=30)
    password = serializers.CharField(required=True, min_length=8, max_length=30)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'name']

