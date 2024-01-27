from .models import UserPasswordManager
from rest_framework import serializers


class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPasswordManager
        fields = ['username', 'password', 'application_type', 'name', 'url']
