# flake8: noqa
import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_DJANGO_KEY', 'secret_key')

DEBUG = os.getenv('DEBUG_VALUE') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'colorfield',
    'django_filters',
    'djoser',
    'rest_framework.authtoken',
    'api.apps.ApiConfig',
    'recipes.apps.RecipesConfig',
    'users.apps.UsersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foodgram_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'foodgram_backend.wsgi.application'


# Database settings

if os.getenv('POSTGRES_DB'):
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'django'),
            'USER': os.getenv('POSTGRES_USER', 'django'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', ''),
            'PORT': os.getenv('DB_PORT', 5432)
        }
    }

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization

LANGUAGE_CODE = 'ru-Ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'collected_static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rest Framework settings

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# Djoser settings

DJOSER = {
    'LOGIN_FIELD': 'email',
    'SERIALIZERS': {
        'token_create': 'api.serializers.AuthTokenCreateSerializer',
    },
}

# .csv data import settings

CSV_DATA_DIRECTORY_PATH = 'csv_data'

# Admin site settings

ADMIN_SITE_EMPTY_VALUE = 'Значение не задано'

# File render settings

SHOPPING_CART_FILE_HEADERS = ['FOODGRAM SHOPPING LIST',]

# Pagination settings

QUERY_PARAMETER_NAME = 'limit'
MAX_PAGE_SIZE = 30
RECIPES_PAGE_SIZE = 6
USERS_PAGE_SIZE = 6

# Recipes settings

COOKING_TIME_MAX_MINUTES = 7200
COOKING_TIME_MIN_MINUTES = 1
INGREDIENT_AMOUNT_MAX = 100_000
INGREDIENT_AMOUNT_MIN = 1
INGREDIENT_NAME_MAX_LENGTH = 50
MEASUREMENT_NAME_MAX_LENGTH = 25
RECIPE_NAME_MAX_LENGTH = 200
TAG_NAME_SLUG_MAX_LENGTH = 25

# Users settings

AUTH_USER_MODEL = 'users.User'
EMAIL_FIELD_MAX_LENGTH = 254
FIRST_LAST_NAME_FIELDS_MAX_LENGTH = 150
PASSWORD_FIELD_MAX_LENGTH = 150
USERNAME_FIELD_MAX_LENGTH = 150

# Success/error messages

COOKING_TIME_INGREDIENT_AMOUNT_TOO_LOW = '{field_name} не может быть меньше {min_value}'
COOKING_TIME_INGREDIENT_AMOUNT_TOO_HIGH = 'Значение {field_name} слишком большое'
CSV_IMPORT_PROCCESSING = 'Importing objects from {filename}.csv is proccessing...'
CSV_IMPORT_SUCCESS = ('{count} objects from {filename}.csv'
                      ' has been successfully imported into {filename} model')
FOLLOW_RECIPE_DOES_NOT_EXIST = '{request_object} не существует'
INVALID_CURRENT_PASSWORD_VALUE = 'Неверное значение поля "Старый пароль"'
RECIPE_CREATION_WITH_DUPLICATE_DATA = 'Каждый {field_name} может быть добавлен только один раз'
RECIPE_CREATION_WITHOUT_REQ_FIELDS = 'Поле {field_name} не может быть пустым'
SHOP_CART_FAVORITES_TWICE_ADDING_DELETING = 'Рецепт уже {action}'
SUBSCRIBE_TWICE_TO_SAME_AUTHOR = 'Вы уже подписаны на данного автора'
SUBSCRIBE_TO_SELF = 'Пользователь не может подписаться на себя'
SUCCESSFULLY_PASSWORD_SETTING = 'Пароль был изменен успешно'
USER_CREATION_WITH_USERNAME_ME = 'Укажите корректный логин'
