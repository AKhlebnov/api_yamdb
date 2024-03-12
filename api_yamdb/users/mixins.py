from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UsernameAndEmailValidatorMixin:
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
