from django.core.validators import RegexValidator, MaxLengthValidator
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .utils import generate_confirmation_code, send_confirmation_email
from .mixins import UsernameAndEmailValidatorMixin

User = get_user_model()


class UserSignupSerializer(
    UsernameAndEmailValidatorMixin,
    serializers.ModelSerializer
):
    """Сериализатор регистрации."""
    username = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Поле "username" должно содержать только буквы, '
                'цифры и символы: @/./+/-/_',
                code='invalid_username'
            ),
            MaxLengthValidator(150)
        ]
    )

    class Meta:
        model = User
        fields = ('email', 'username')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
        }

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        confirmation_code = generate_confirmation_code()
        ex_user = User.objects.filter(username=username, email=email).first()
        if ex_user:
            ex_user.confirmation_code = confirmation_code
            ex_user.save()
            send_confirmation_email(validated_data['email'], confirmation_code)
            return ex_user
        user = User.objects.create(
            **validated_data,
            confirmation_code=confirmation_code
        )
        send_confirmation_email(email, confirmation_code)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор для получения JWT-токена."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']
        self.fields['username'] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

        if not username:
            raise serializers.ValidationError(
                {'username': 'Username is required.'})
        user = User.objects.filter(username=username).first()
        if not user:
            raise NotFound({'detail': 'User not found.'})
        if not confirmation_code:
            raise serializers.ValidationError(
                {'confirmation_code': 'Confirmation code is required.'})
        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError(
                {'confirmation_code': 'Invalid confirmation code.'})
        return attrs


class UserSerializer(
    UsernameAndEmailValidatorMixin,
    serializers.ModelSerializer
):
    """Сериализатор для работы с пользователями."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserMePatchSerializer(
    UsernameAndEmailValidatorMixin,
    serializers.ModelSerializer
):
    """Сериализатор для метода PATCH."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)
