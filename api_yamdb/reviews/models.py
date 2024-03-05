from django.contrib.auth import get_user_model
from django.db import models

from .validators import validate_actual_year

User = get_user_model()


class CategoryGenreBase(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='ID',
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ('name',)


class Category(CategoryGenreBase):
    """Категории 'произведений'."""

    class Meta(CategoryGenreBase.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreBase):
    """Жанры 'произведений'."""

    class Meta(CategoryGenreBase.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Произведение культуры. Конкретный объект.

    Поля 'name', 'year', 'category', 'description'.
    name - Авторское или исторически сложившееся название. Обязательное.
    year - Год издания/публикации произведения. Обязательное.
    category - ссылка на категорию. Обязательное. При удалении категории,
    принимает дефоптное значение.
    Значение по умолчанию - 'Null'.
    description - Краткое представление произведения.
    """
    name = models.CharField(
        verbose_name='Название',
        max_length=256

    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=[validate_actual_year]
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'

    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)
