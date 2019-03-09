# myproject/settings.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import os
import sys
from django.utils.translation import ugettext_lazy as _
from .conf.dev import *
from utils.misc import get_git_changeset


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

EXTERNAL_LIBS_PATH = os.path.join(BASE_DIR, "externals", "libs")

EXTERNAL_APPS_PATH = os.path.join(BASE_DIR, "externals", "apps")

sys.path = ["", EXTERNAL_LIBS_PATH, EXTERNAL_APPS_PATH] + sys.path


CMS_APPHOOKS = (
    "movies.cms_app.MoviesApphook",
)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "myproject",
        'USER': "root",
        'PASSWORD': "root",
    }
}


MEDIA_ROOT = os.path.join(BASE_DIR, "myproject", "media")


# This should be an initially empty destination directory
# for collecting your static files from their permanent locations into one directory for ease of deployment;
# it is not a place to store your static files permanently.

STATIC_ROOT = os.path.join(BASE_DIR, "myproject", "static")


MEDIA_URL = "/media/"


# URL to use when referring to static files located in STATIC_ROOT.
# Below, we had set the STATIC_URL dynamically with a varying path component - get_git_changeset
# So whenever the code is updated, the visitor's browser will force loading of all-new uncached static files.

# STATIC_URL = "/static/%s/" % get_git_changeset(BASE_DIR)
# Changed to serve files from myproject/site_static
STATIC_URL = "/site_static/"


# This setting defines the additional locations the staticfiles app will traverse
# if the FileSystemFinder finder is enabled, e.g. if you use the collectstatic
# or findstatic management command or use the static file serving view.

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "myproject", "site_static"),
)


LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

FILE_UPLOAD_TEMP_DIR = os.path.join(
    BASE_DIR, "myproject", "tmp"
)

LANGUAGES = (
    ("en", "English"),
    ("de", "Deutsch"),
    ("fr", "Français"),
    ("sw", "Swahili"),
)

LANGUAGE_CODE = "en"

# overwrite the STATUS_CHOICE from magazine/app_settings.py
MYAPP1_STATUS_CHOICES = (
    ("imported",   _("Imported")),
    ("draft",      _("Draft")),
    ("published",  _("Published")),
    ("not_listed", _("Not Listed")),
    ("expired",    _("Expired")),
)

# local_settings.py - which might not be added to version control
# This entirely depends on how simple you keep things
try:
    # execfile( os.path.join(os.path.dirname(__file__), "local_settings.py" ) )
    # execfile was removed in python 3+, replaced with exec(open(fn).read())
    exec( open(os.path.join(
        os.path.dirname(__file__), "local_settings.py")
    ).read() )
except IOError:
    pass
