from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserCreateSerializer(serializers.ModelSerializer):
    """ Serializer: Create a new user """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'pk',
            'email',
            'first_name',
            'last_name',
            'password',
            'bio',
            'birth_date',
            'location',
            'website',
            'profile_picture',
            'is_private',
            'role'
        )

    def validate_email(self, value):
        # Custom email validation logic
        if get_user_model().objects.filter(email=value.strip(),is_active=True).exists():
            raise serializers.ValidationError("Email already in use")
        return value.lower()

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = get_user_model().objects.create_user(password=password, **validated_data)
        return user


class UserDisplaySerializer(serializers.ModelSerializer):
    """ Serializer: Display user details """

    class Meta:
        model = get_user_model()
        fields = (
            'pk',
            'email',
            'first_name',
            'last_name',
            'role',
            'bio',
            'birth_date',
            'location',
            'website',
            'profile_picture',
            'is_private',
            'is_verified',
            'is_active',
            'last_active',
        )
