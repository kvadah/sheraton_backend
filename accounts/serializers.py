from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'role']

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email Already Exist')
        return email

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
