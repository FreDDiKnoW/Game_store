from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
import logging

logger = logging.getLogger(__name__)


class UserRegistrationSerializer(serializers.ModelSerializer):
    # Додаємо поле для повторного вводу пароля, воно не зберігається в базі
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Паролі не збігаються."})

        try:
            validate_password(attrs['password'])
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        user = User.objects.create_user(**validated_data)

        logger.info(f"Створено нового користувача: {user.username}")

        return user
