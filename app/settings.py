import os
import dj_database_url

# Database configuration
db_url = os.environ.get('DATABASE_URL')
if db_url:
    DATABASES = {"default": dj_database_url.parse(db_url)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'mydb',
            'USER': 'myuser',
            'PASSWORD': 'mypassword',
            'HOST': 'db',
            'PORT': 3306,
        }
    }

# Cache configuration
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Additional installed apps
INSTALLED_APPS += [
    'channels',
    'dj_database_url',
    'django_redis',
    'orders',
]

# ASGI application
ASGI_APPLICATION = 'app.routing.application'

# Channel layers configuration
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
        },
    },
}

# Allowed hosts configuration
if "APP_RUNNER_DEFAULT_HOST" in os.environ:
    ALLOWED_HOSTS = [os.environ["APP_RUNNER_DEFAULT_HOST"]]
else:
    ALLOWED_HOSTS = ["*"]
