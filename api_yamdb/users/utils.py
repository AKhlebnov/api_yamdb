from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string


def generate_confirmation_code(length=10):
    """Функция генерации кода подтверждения."""
    return get_random_string(length)


def send_confirmation_email(email, confirmation_code):
    """Функция отправки письма с кодом подтверждения."""
    subject = 'Confirmation Code api_yamdb'
    message = f'Your confirmation code is: {confirmation_code}'
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
