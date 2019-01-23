
# myproject/settings.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from .conf.dev import *
from utils.misc import get_git_changeset
import os
import sys
from django.utils.translation import ugettext_lazy as _


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


EXTERNAL_LIBS_PATH = os.path.join(BASE_DIR, "externals", "libs")

EXTERNAL_APPS_PATH = os.path.join(BASE_DIR, "externals", "apps")

sys.path = ["", EXTERNAL_LIBS_PATH, EXTERNAL_APPS_PATH] + sys.path


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "myproject",
        'USER': "root",
        'PASSWORD': "root",
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, "myproject", "media")

STATIC_ROOT = os.path.join(BASE_DIR, "myproject", "static")

STATIC_URL = "/static/%s/" % get_git_changeset(BASE_DIR)

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, "myproject", "site_static"),
)

LOCALE_PATHS = (
	os.path.join(BASE_DIR, "locale"),
)

FILE_UPLOAD_TEMP_DIR = os.path.join(
	BASE_DIR, "myproject", "tmp"
)

# overwrite the STATUS_CHOICE from magazine/app_settings.py
MYAPP1_STATUS_CHOICES = (
	("imported",   _("Imported")),
	("draft",      _("Draft")),
	("published",  _("Published")),
	("not_listed", _("Not Listed")),
	("expired",    _("Expired")),
)

# local_settings.py
try:
	# execfile( os.path.join(os.path.dirname(__file__), "local_settings.py" ) )
	# execfile was removed in python 3+, replaced with exec(open(fn).read())
	exec( open(os.path.join(
		os.path.dirname(__file__), "local_settings.py" )
	).read() )
except IOError:
    pass
	