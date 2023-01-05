import os

from .enviroment import DEBUG

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE_DEBUG') if DEBUG is True else os.environ.get('DATABASE_ENGINE'),  # noqa
        'NAME': os.environ.get('DATABASE_NAME_DEBUG') if DEBUG is True else os.environ.get('DATABASE_NAME'),  # noqa
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
    }
}
