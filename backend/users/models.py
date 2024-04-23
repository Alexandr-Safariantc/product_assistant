from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from foodgram_backend.settings import (
    EMAIL_FIELD_MAX_LENGTH,
    FIRST_LAST_NAME_FIELDS_MAX_LENGTH,
    PASSWORD_FIELD_MAX_LENGTH,
    ROLE_FIELD_MAX_LENGTH,
    USERNAME_FIELD_MAX_LENGTH,
)


class User(AbstractUser):
    """Describe user model."""

    class Roles(models.TextChoices):
        """Roles for User instances."""
        USER = 'user', 'user'
        ADMIN = 'admin', 'admin'

    email = models.EmailField(
        'Адрес электронной почты',
        db_index=True,
        max_length=EMAIL_FIELD_MAX_LENGTH,
        unique=True
    )
    first_name = models.TextField(
        'Имя', max_length=FIRST_LAST_NAME_FIELDS_MAX_LENGTH
    )
    last_name = models.TextField(
        'Фамилия', db_index=True, max_length=FIRST_LAST_NAME_FIELDS_MAX_LENGTH
    )
    password = models.CharField(
        'Пароль',
        max_length=PASSWORD_FIELD_MAX_LENGTH,
        validators=[validate_password,]
    )
    role = models.CharField(
        'Уровень доступа',
        default=Roles.USER,
        choices=Roles.choices,
        max_length=ROLE_FIELD_MAX_LENGTH
    )
    username = models.CharField(
        'Логин',
        db_index=True,
        max_length=USERNAME_FIELD_MAX_LENGTH,
        unique=True,
        validators=[UnicodeUsernameValidator(),]
    )

    class Meta:
        default_related_name = 'users'
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Return instance text representation."""
        return (f'Пользователь {self.username}'
                f' Имя: {self.first_name} Фамилия: {self.last_name}')

    @property
    def is_admin(self):
        """Return True if user role is admin, false otherwise."""
        return self.role == 'admin' or self.is_superuser


class Follow(models.Model):
    """Describe author subscriptions of users."""

    created_at = models.DateTimeField('Дата подписки', auto_now_add=True)
    following_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authors',
        verbose_name='Автор'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Подписчик'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following_author'],
                name='unique_user_following_author'
            ),
        ]
        ordering = ('-created_at', 'following_author__username',)
        verbose_name = 'подписки'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        """Return instance text representation."""
        return (f'Автор {self.following_author} из списка подписок'
                f' пользователя: {self.user}')
