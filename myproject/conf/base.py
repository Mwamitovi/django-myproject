# myproject/conf/base.py - shared settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mfa!g+0p!9*asdei+9%l!*$bif+%wlt+lsbolgpr4-9ft00-i6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'debug_toolbar.apps.DebugToolbarConfig',
    'ajaxuploader',
    'crispy_forms',
    'mptt',
    'django_mptt_admin',
    'rest_framework',
    # 'tastypie',
    'mptt_tree_editor',
    'custom_admin',
    'haystack',
    'magazine',
    'myapp1',
    'music',
    'quotes',
    'search',
    'likes',
    'locations',
    "movies",
    "products",
    'utils',
    # "bulletin_board",
    # "cv",
    # 'email_messages',
    # added from cmstart/settings.py
    'djangocms_admin_style',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'filer',
    'easy_thumbnails',
    'djangocms_column',
    'djangocms_file',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_style',
    'djangocms_snippet',
    'djangocms_googlemap',
    'djangocms_video',
)

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # activates translation
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [   # We are telling...
                    # django.template.loaders.filesystem.Loader:
                    # to look into this folder...
                    # C:\virtualenvs\myproject_env\project\django-myproject\myproject\templates\ (myapp1\idea_list.html)
                    # The last part in brackets is generated from myapp1/views.py - template_name
                    os.path.join(BASE_DIR, "templates")
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Kampala'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'


# Crispy forms template
CRISPY_TEMPLATE_PACK = "bootstrap4"

# HayStack connections
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'search.multilingual_whoosh_backend.MultilingualWhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'myproject', 'tmp','whoosh_index_en'),
    },
    'default_en': {
        'ENGINE': 'search.multilingual_whoosh_backend.MultilingualWhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'myproject', 'tmp', 'whoosh_index_en'),
    },
    'default_de': {
        'ENGINE': 'search.multilingual_whoosh_backend.MultilingualWhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'myproject', 'tmp', 'whoosh_index_de'),
    },
    "default_fr": {
        'ENGINE': 'search.multilingual_whoosh_backend.MultilingualWhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'myproject', 'tmp', 'whoosh_index_fr'),
    },
    'default_sw': {
        'ENGINE': 'search.multilingual_whoosh_backend.MultilingualWhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'myproject', 'tmp', 'whoosh_index_sw'),
    },
}

# django-restframework config
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions."
        "DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
}






