# utils/templatetags/utility_tags.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import sys
# import urllib - replaced with import below...
from django.utils.http import urlencode
from django.utils.encoding import force_str
import datetime
from django import template
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as tz_now
import re
from django.utils.safestring import mark_safe
from django.utils.encoding import python_2_unicode_compatible
register = template.Library()


if sys.version_info.major == 3:
    """In python 3, unicode was replaced by strings because of it's abundance
    Therefore if using python 2 & 3, we need to define unicode
    """
    unicode = str


# TAGS #
@python_2_unicode_compatible
@register.tag
def try_to_include(parser, token):
    """Usage: {% try_to_include "sometemplate.html" %}
    This will fail silently if the template doesn't exist.
    If it does exist, it will be rendered with the current
    context."""
    try:
        tag_name, template_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0]
        )
    return IncludeNode(template_name)


@python_2_unicode_compatible
class IncludeNode(template.Node):
    def __init__(self, template_name):
        self.template_name = template_name

    def render(self, context):
        try:
            # Loading the template and rendering it
            # django.template.resolve_variable is "Deprecated" for sometime
            # template_name = template.resolve_variable(self.template_name, context)
            template_name = template.Variable(self.template_name).resolve(context)
            included_template = get_template(template_name).render(context)
        except template.TemplateDoesNotExist:
            included_template = ""
        return included_template


@python_2_unicode_compatible
@register.tag
def get_objects(parser, token):
    """
    Gets a queryset of objects of the model specified by app and model names
    Usage:
        {% get_objects [<manager>.]<method> from <app_name>.<model_name>
            [limit <amount>] as <var_name> %}
    Example:
        {% get_objects latest_published from people.Person limit 3 as people %}
        {% get_objects site_objects.all from news.Article limit 3 as articles %}
        {% get_objects site_objects.all from news.Article as articles %}
    """
    amount = None
    try:
        tag_name, manager_method, str_from, appmodel, \
        str_limit, amount, str_as, var_name = token.split_contents()
    except ValueError:
        try:
            tag_name, manager_method, str_from, appmodel, \
            str_as, var_name = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError(
                "get_objects tag requires a following syntax: "
                "{% get_objects [<manager>.]<method> from <app_ name>.<model_name> "
                "[limit <amount>] as <var_name> %}"
            )
    try:
        app_name, model_name = appmodel.split(".")
    except ValueError:
        raise template.TemplateSyntaxError(
            "get_objects tag requires application name and model name separated by a dot"
        )
    # model = models.get_model(app_name, model_name)
    model = appmodel.get_model(app_name, model_name)
    return ObjectsNode(
        model, manager_method, amount, var_name
    )


@python_2_unicode_compatible
class ObjectsNode(template.Node):
    def __init__(self, model, manager_method, amount, var_name):
        self.model = model
        self.manager_method = manager_method
        self.amount = amount
        self.var_name = var_name

    # noinspection PyProtectedMember
    def render(self, context):
        if "." in self.manager_method:
            manager, method = self.manager_method.split(".")
        else:
            manager = "_default_manager"
            method = self.manager_method

        qs = getattr(
            getattr(self.model, manager),
            method,
            self.model._default_manager.none,
        )()

        if self.amount:
            # django.template.resolve_variable is "Deprecated" for sometime
            # amount = template.resolve_variable(self.amount, context)
            amount = template.Variable(self.amount).resolve(context)
            context[self.var_name] = qs[:amount]
        else:
            context[self.var_name] = qs
        return ""


# noinspection PyProtectedMember
@python_2_unicode_compatible
@register.simple_tag(takes_context=True)
def modify_query(context, *params_to_remove, **params_to_change):
    """ Renders a link with modified current query parameters """
    query_params = []
    for key, value_list in context["request"].GET._iterlists():
        if key not in params_to_remove:
            # don't add key-value pairs for params_to_change
            if key in params_to_change:
                query_params.append(
                    (key, params_to_change[key])
                )
                params_to_change.pop(key)
            else:
                # leave existing parameters as they were
                # if not mentioned in the params_to_change
                for value in value_list:
                    query_params.append((key, value))

    # attach new params
    for key, value in params_to_change.items():
        query_params.append((key, value))
    query_string = context["request"].path
    if len(query_params):
        # django.utils.http.urlencode is a version of python's urllib.urlencode
        # query_string += "?%s" % urllib.urlencode([
        query_string += "?%s" % urlencode([
            (key, force_str(value))
            for (key, value) in query_params if value
        ]).replace("&", "&amp;")
    return query_string


# noinspection PyProtectedMember
@python_2_unicode_compatible
@register.simple_tag(takes_context=True)
def add_to_query(context, *params_to_remove, **params_to_add):
    """ Renders a link with modified current query parameters """
    query_params = []
    # go through current query params..
    for key, value_list in context["request"].GET._iterlists():
        if key not in params_to_remove:
            # don't add key-value pairs which already
            # exist in the query
            if key in params_to_add and unicode(params_to_add[key]) in value_list:
                params_to_add.pop(key)
            for value in value_list:
                query_params.append((key, value))

    # add the rest key-value pairs
    for key, value in params_to_add.items():
        query_params.append((key, value))
        # empty values will be removed
        query_string = context["request"].path

        if len(query_params):
            query_string += "?%s" % urlencode([
                (key, force_str(value))
                for (key, value) in query_params if value
            ]).replace("&", "&amp;")

        return query_string


# noinspection PyProtectedMember
@python_2_unicode_compatible
@register.simple_tag(takes_context=True)
def remove_from_query(context, *args, **kwargs):
    """ Renders a link with modified current query parameters """
    query_params = []
    # go through current query params..
    for key, value_list in context["request"].GET._iterlists():
        # skip keys mentioned in the args
        if key not in args:
            for value in value_list:
                # skip key-value pairs mentioned in kwargs
                if not (key in kwargs and unicode(value) == unicode(kwargs[key])):
                    query_params.append((key, value))

    # empty values will be removed
    query_string = context["request"].path
    if len(query_params):
        query_string = "?%s" % urlencode([
            (key, force_str(value))
            for (key, value) in query_params if value
        ]).replace("&", "&amp;")
    return query_string


# FILTERS #
@register.filter
def days_since(value):
    """ Returns number of days between today and value."""

    today = tz_now().date()
    if isinstance(value, datetime.datetime):
        value = value.date()
    diff = today - value

    if diff.days > 1:
        return _("%s days ago") % diff.days
    elif diff.days == 1:
        return _("yesterday")
    elif diff.days == 0:
        return _("today")
    else:
        # Date is in the future; return formatted date.
        return value.strftime("%B %d, %Y")


media_tags_regex = re.compile(
    r"<figure[\S\s]+?</figure>|"
    r"<object[\S\s]+?</object>|"
    r"<video[\S\s]+?</video>|"
    r"<audio[\S\s]+?</audio>|"
    r"<iframe[\S\s]+?</iframe>|"
    r"<(img|embed)[^>]+>",
    re.MULTILINE
)


@register.filter
def first_media(content):
    """ Returns the first image or flash file from the html
    content """
    m = media_tags_regex.search(content)
    media_tag = ""

    if m:
        media_tag = m.group()
    return mark_safe(media_tag)


@register.filter
def humanize_url(url, letter_count):
    """ Returns a shortened human-readable URL """
    letter_count = int(letter_count)
    re_start = re.compile(r"^https?://")
    re_end = re.compile(r"/$")
    url = re_end.sub("", re_start.sub("", url))

    if len(url) > letter_count:
        url = "%s…" % url[:letter_count - 1]
    return url
