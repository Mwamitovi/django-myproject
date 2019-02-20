# myproject/urls.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.conf.urls import include, url
# from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import string_concat
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.i18n import i18n_patterns

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from haystack.views import SearchView
import utils.views


admin.site.site_header = "MyProject administration"
admin.site.site_title = "MyAdmin Portal"
admin.site.index_title = "Welcome to MyProject"

login_helper = FormHelper()
login_helper.form_action = reverse_lazy("my_login_page")
login_helper.form_method = "POST"
login_helper.form_class = "form-signin"
login_helper.html5_required = True
login_helper.layout = layout.Layout(layout.HTML(
    string_concat("""<h2 class="form-signinheading">""", "(Please Sign In)", """</h2>""")),
    layout.Field("username", placeholder=_("username")),
    layout.Field("password", placeholder=_("password")),
    layout.HTML("""<input type="hidden" name="next" value="{{ next }}" />"""),
    layout.Submit("submit", _("Login"), css_class="btn-lg"),
)


class CrispySearchView(SearchView):
    def extra_context(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.disable_csrf = True
        return {"search_helper": helper}


urlpatterns = i18n_patterns(
    # Examples:
    # url(r'^$', myproject.views.home, name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'login/$', views.LoginView.as_view(),
        {"extra_context": {"login_helper": login_helper}}, name="my_login_page"),
    url(r'^myapp1/', include('myapp1.urls', namespace='myapp1')),
    url(r'^quotes/', include('quotes.urls', namespace='quotes')),
    url(r'^locations/', include('locations.urls', namespace='locations')),
    url(r'^search/', CrispySearchView(), name='haystack_search'),
    url(r'^js-settings/$', utils.views.render_js,
        {"template_name": "settings.js"},
        name='js_settings'
        ),
)
