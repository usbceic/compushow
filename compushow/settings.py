"""
Django settings for compushow project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from os import path
from datetime import date

#ESTADO DEL SISTEMA:
DEBUG = True

TEMPLATE_DEBUG = DEBUG

class Etapas:
    # El Compushow se encuentra cerrado, no han iniciado ningun tipo de votaciones.
    CERRADO   = 0
    # Etapa en la que se hacen nominaciones a las categorias.
    NOMINANDO = 1
    # Etapa de filtrado.
    FILTRANDO = 2
    # Etapa en la que se vota por los nominados para elegir un ganador.
    VOTANDO   = 3

# Indica en que etapa se encuentra el Compushow para el comportamiento de la pagina
ETAPA = Etapas.CERRADO

# Dia en el que se realizara el compushow
FECHA_DE_EVENTO = date(date.today().year, 3, 1)

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'votaciones',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'compushow.urls'

WSGI_APPLICATION = 'compushow.wsgi.application'

ADMINS = (
    ('Rosangelis Garcia', 'rosangelis.92@gmail.com'),
    ('Ivan Travecedo', 'ivantrave@gmail.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'compushow',                      
        'USER': 'postgres',                      
        'PASSWORD': '123456',                  
        'HOST': '',                     
        'PORT': '',                      
    }
}

TIME_ZONE = 'America/Caracas'

LANGUAGE_CODE = 'es-ve'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

PROJECT_ROOT = path.dirname(path.abspath(__file__))

MEDIA_ROOT = PROJECT_ROOT + '/media/'
MEDIA_URL = '/media/'

STATIC_ROOT = PROJECT_ROOT+'/templates/'
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    ('site', PROJECT_ROOT+'/templates'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'z--3m5shawjl79c@4!u+t_33@#*t_da)y9a)rlqd&p2g&)l@!$'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    PROJECT_ROOT+'/templates',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
