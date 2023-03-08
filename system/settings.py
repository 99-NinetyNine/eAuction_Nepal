import os


from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-=k7$^3y6v)vp^axv1q_4c4wcr%(pyfmn%t6y5rigy6(li#_v+-'
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    #3rd party
    'crispy_forms',
    #'location_field.apps.DefaultConfig',

    #ours
    #mechanism
    'mechanism',
    
    #policy
    'simple_auth',
    'auctions',
    'bidding',
    'pages',
    'notification',
    'ai',

]
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "simple_auth.authenticate.EmailAuthbackend",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'system.wsgi.application'
# Daphne
ASGI_APPLICATION = "system.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

#Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# # DATABASES = {
# #     'default': {
# #         'ENGINE': 'django.db.backends.mysql',
        
# #         'NAME': 'eauction',
# #         'USER': 'root',
# #         'PASSWORD': '123456',
# #         'HOST':'localhost',
# #         'PORT':'3306',
        
# #     }
# # }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

LOCATION_FIELD = {
    'provider.google.api': '//maps.google.com/maps/api/js?sensor=false',
    'provider.google.api_key': 'apikey xaina cause no debit account ',
    'provider.google.api_libraries': '',
    'provider.google.map.type': 'ROADMAP',
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'
STATTICFILES_DIRS=[os.path.join(BASE_DIR, 'static')]
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


LOGIN_REDIRECT_URL='home'
LOGOUT_REDIRECT_URL='login'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'eBid'
# EMAIL_HOST_PASSWORD = '92nbj39RrGnCw6h@'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


AUTH_USER_MODEL = 'mechanism.User'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CELERY_BROKER_URL = "redis://127.0.0.1:6379"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379"
CELERY_TIMEZONE = 'UTC'



from celery.schedules import crontab

from celery import shared_task


from celery.schedules import crontab

@shared_task()
def hello():
    print("asas")

CELERY_BEAT_SCHEDULE = {
    'check_expiry_task': {
        'task': 'mechanism.auction.beat_beat',
        
        #'schedule': crontab(minute='*/1'),
        'schedule':5,
    },
}
