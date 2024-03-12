from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
    ('superuser', 'Суперюзер Django')
)


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.CharField(
        max_length=20,
        choices=CHOICES,
        default='user',
        verbose_name='Роль'
    )
    confirmation_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Код подтверждения'
    )

    def clean(self):
        # super().clean()
        if self.username == 'me':
            raise ValidationError(
                {'username': 'Использование имени "me" в качестве username '
                 'запрещено.'}
            )
        if CustomUser.objects.exclude(
            id=self.id
        ).filter(username=self.username).exists():
            raise ValidationError(
                {'username': 'Этот username уже используется.'}
            )
        if self.email:
            if CustomUser.objects.exclude(
                id=self.id
            ).filter(email=self.email).exists():
                raise ValidationError(
                    {'email': 'Этот email уже используется.'}
                )
