from django.contrib.auth.models import AbstractUser
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
