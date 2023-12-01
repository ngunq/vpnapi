from base64 import b64decode
import os
import pathlib
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(filename='settings.env'))
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

os.makedirs(os.path.join(BASE_DIR, Path('ansible_log')), exist_ok=True)
os.chmod(os.path.join(BASE_DIR, Path('ansible_log')), mode=0o777)

os.makedirs(os.path.join(BASE_DIR, Path(
    'ansible_log/ansible_runner_data')), exist_ok=True)
os.chmod(os.path.join(BASE_DIR, Path(
    'ansible_log/ansible_runner_data')), mode=0o777)

open(os.path.join(BASE_DIR, Path('ansible_log/ansible.log')), 'a+').close()
os.chmod(os.path.join(BASE_DIR, Path('ansible_log/ansible.log')), mode=0o777)

pathlib.Path(os.path.join(BASE_DIR, 'log', 'open_vpn')
             ).mkdir(parents=True, exist_ok=True)
pathlib.Path(os.path.join(BASE_DIR, 'log', 'ping_service')
             ).mkdir(parents=True, exist_ok=True)
pathlib.Path(os.path.join(BASE_DIR, 'log', 'server')
             ).mkdir(parents=True, exist_ok=True)
open(os.path.join(BASE_DIR, 'log', 'open_vpn', 'open_vpn.log'), 'a+').close()
open(os.path.join(BASE_DIR, 'log', 'ping_service', 'ping_service.log'), 'a+').close()
open(os.path.join(BASE_DIR, 'log', 'server', 'api.log'), 'a+').close()
os.chmod(os.path.join(BASE_DIR, 'log', 'open_vpn', 'open_vpn.log'), mode=0o777)
os.chmod(os.path.join(BASE_DIR, 'log', 'ping_service',
         'ping_service.log'), mode=0o777)
os.chmod(os.path.join(BASE_DIR, 'log', 'server', 'api.log'), mode=0o777)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

SECRET_KEY = os.getenv('SECRET_KEY')
FERNET_KEY = os.getenv('FERNET_KEY').encode()
# print(FERNET_KEY)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = ['*']

DOMAIN = os.getenv('DOMAIN')
ZONEID = os.getenv('ZONEID')
CLOUDFLARE_GENERAL_TOKEN = os.getenv('CLOUDFLARE_GENERAL_TOKEN')
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
CLOUDFLARE_EMAIL = os.getenv('CLOUDFLARE_EMAIL')
OPENVPN_SESSIONS_LIMIT = os.getenv('OPENVPN_SESSIONS_LIMIT')
WIREGUARD_SESSIONS_LIMIT = os.getenv('WIREGUARD_SESSIONS_LIMIT')
OPENVPN_SECRET = os.getenv('OPENVPN_SECRET')

# account settings
AUTH_USER_MODEL = 'api.AppUser'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "ansible_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "verbose",
            "filename": os.path.join(BASE_DIR, Path('ansible_log/ansible.log')),
            "when": "h",
            "interval": 24,
            "backupCount": 365,
            "delay": True
        },
        "ovpn": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "verbose",
            "filename": os.path.join(BASE_DIR, Path('log/open_vpn/open_vpn.log')),
            "when": "h",
            "interval": 24,
            "backupCount": 365,
            "delay": True
        },
        "ping_service": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "verbose",
            "filename": os.path.join(BASE_DIR, Path('log/ping_service/ping_service.log')),
            "when": "h",
            "interval": 24,
            "backupCount": 365,
            "delay": True
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "verbose",
            "filename": os.path.join(BASE_DIR, Path('log/server/api.log')),
            "when": "h",
            "interval": 24,
            "backupCount": 365,
            "delay": True,
            "level": "ERROR"
        }
    },
    "formatters": {
        "verbose": {
            "format": "{asctime} {levelname} {message}",
            "style": "{",
        },
    },
    "loggers": {
        "ansible": {
            "handlers": ["ansible_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "openvpn": {
            "handlers": ["ovpn"],
            "level": "DEBUG",
            "propagate": False,
        },
        "ping_service": {
            "handlers": ["ping_service"],
            "level": "DEBUG",
            "propagate": False,
        },
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'dj_rest_auth',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_seed',
    'django_extensions',
    'django_celery_beat',
    'celery',
    'django_celery_results',
    # 'django_cleanup.apps.CleanupConfig',
]

# rest settings
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'api.helpers.ApiRenderer',
        # 'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
    ]
}

REST_AUTH = {
    'REGISTER_SERIALIZER': 'api.serializers.UserRegisterSerializer',
    'USER_DETAILS_SERIALIZER': 'api.serializers.UserDetailsSerializer',
    'SESSION_LOGIN': False,
    'LOGIN_SERIALIZER': 'api.serializers.LoginSerializer',
    'USE_JWT': True,
    'JWT_SERIALIZER': 'api.serializers.JWTSerializer'
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(weeks=500)
}

SPECTACULAR_SETTINGS = {
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    'TITLE': 'vpn api',
    'DESCRIPTION': 'vpn app api',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': '/api/',
    'POSTPROCESSING_HOOKS': [
        'drf_spectacular.hooks.postprocess_schema_enums',
        'drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields',
    ],
    'ENUM_NAME_OVERRIDES': {
        'VpnTypeEnum': 'api.models.enums.VPNType'
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djangorestframework_camel_case.middleware.CamelCaseMiddleWare',
]

ROOT_URLCONF = 'vpn_app.urls'

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

WSGI_APPLICATION = 'vpn_app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.mysql",
        #  'NAME': 'vpn',
        #  'USER': 'root',
        #  'PASSWORD': 'P@ssw0rd',
        #  'HOST': '172.16.100.90',
        #  'PORT': '3306',
        "OPTIONS": {
            "read_default_file": str(BASE_DIR) + "/vpn_app/mysql.cnf",
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SITE_ID = 1
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'MEDIA/'
MEDIA_ROOT = 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# email configuration
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = os.getenv('email')
# EMAIL_HOST_PASSWORD = os.getenv('email_password')

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# CELERY_RESULT_BACKEND =
CELERY_BEAT_SCHEDULE = {
    'check_public_servers': {
        'task': 'api.tasks.update_public_server_status.update_public_server_status',
        'schedule': 30
    },
    'check_private_servers': {
        'task': 'api.tasks.update_private_server_status.update_private_server_status',
        'schedule': 30
    },
    'check_private_vm_servers': {
        'task': 'api.tasks.update_private_server_vm_status.update_private_server_vm_status',
        'schedule': 30
    },
}

CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True
CELERY_TASK_TRACK_STARTED = True
DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH = 191

ASGI_APPLICATION = 'vpn_app.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        # from channels_redis.core import RedisChannelLayer
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                ("127.0.0.1", 6379)
            ],
        }
    }
}
