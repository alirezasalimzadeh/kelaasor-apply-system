from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from accounts.models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'national_id', 'phone_number', 'degree', 'gpa']

    def create(self, validated_data):
        user = self.context['request'].user
        if Profile.objects.filter(user=user).exists():
            raise serializers.ValidationError("This user is already registered")
        return Profile.objects.create(user=user, **validated_data)
