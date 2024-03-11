from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .utils import generate_confirmation_code, send_confirmation_email

User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации."""
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Использование имени 'me' запрещено."
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Этот username уже используется."
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже используется.")
        return value

    def create(self, validated_data):
        confirmation_code = generate_confirmation_code()
        user = User.objects.create(
            **validated_data,
            confirmation_code=confirmation_code
        )
        send_confirmation_email(validated_data['email'], confirmation_code)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор для получения JWT-токена."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']
        self.fields['username'] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, attrs):
        username = attrs['username']
        confirmation_code = attrs['confirmation_code']
        user = User.objects.filter(
            username=username,
            confirmation_code=confirmation_code
        ).first()
        if not user:
            raise NotFound('User not found')
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с пользователями."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserMePatchSerializer(serializers.ModelSerializer):
    """Сериализатор для метода PATCH."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)
