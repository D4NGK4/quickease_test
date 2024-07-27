from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserSerializer
from rest_framework import serializers


User = get_user_model()


User = get_user_model()

class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'firstname', 'lastname', 'password']

class ViewUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ['id', 'email', 'firstname', 'lastname']
