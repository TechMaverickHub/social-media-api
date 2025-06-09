from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.role.models import Role


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
            'username',
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
        email = value.strip()
        if get_user_model().objects.filter(email=email,is_active=True).exists():
            raise serializers.ValidationError("Email already in use")
        return email

    def validate_username(self, value):
        username = value.strip()
        if get_user_model().objects.filter(username=username,is_active=True).exists():
            raise serializers.ValidationError("Username already in use")
        return username


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = get_user_model().objects.create_user(password=password, **validated_data)
        return user

class RoleDisplaySerializer(serializers.ModelSerializer):
    """ Serializer: Display user details """

    class Meta:
        model = Role
        fields = ('pk','name')


class UserDisplaySerializer(serializers.ModelSerializer):
    """ Serializer: Display user details """
    role = RoleDisplaySerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'pk',
            'email',
            'first_name',
            'last_name',
            'username',
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


class UserListFilterDisplaySerializer(serializers.ModelSerializer):
    """ Serializer: Display user details """

    class Meta:
        model = get_user_model()
        fields = (
            'pk',
            'email',
            'first_name',
            'last_name',
            'username',
            'bio',
            'birth_date',
            'location',
            'website',
            'profile_picture',
            'last_active',
        )

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'pk',
            'email',
            'first_name',
            'last_name',
            'username',
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
        email = value.strip()
        if get_user_model().objects.filter(email=email,is_active=True).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("Email already in use")
        return email

    def validate_username(self, value):
        username = value.strip()
        if get_user_model().objects.filter(username=username,is_active=True).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("Username already in use")
        return username

