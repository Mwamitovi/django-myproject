# likes/templatetags/likes_tags.py
# -*- coding: UTF-8 -*-
from django import template
from django.contrib.contenttypes.models import ContentType
from django.template import loader
from likes.models import LikeThis
from django.utils.encoding import python_2_unicode_compatible
register = template.Library()


# TAGS #
@python_2_unicode_compatible
@register.tag
def like_widget(parser, token):
    try:
        tag_name, for_str, obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a following syntax: {%% %r for <object> %%}" %
            (token.contents[0], token.contents[0])
        )
    return ObjectLikeWidget(obj)


@python_2_unicode_compatible
class ObjectLikeWidget(template.Node):
    def __init__(self, obj):
        self.obj = obj

    def render(self, context):
        # obj = template.resolve_variable(self.obj, context)
        obj = template.Variable(self.obj).resolve(context)
        ct = ContentType.objects.get_for_model(obj)
        is_liked_by_user = bool(LikeThis.objects.filter(
            user=context["request"].user,
            content_type=ct,
            object_id=obj.pk,
        ))

        context.push()
        context["object"] = obj
        context["content_type_id"] = ct.pk
        context["is_liked_by_user"] = is_liked_by_user
        context["count"] = get_likes_count(obj)
        # output = loader.render_to_string("likes/includes/like.html", context)
        output = loader.render_to_string(
            "likes/includes/like.html",
            context={}
        )
        context.pop()
        return output


# FILTERS #
@python_2_unicode_compatible
@register.filter
def get_likes_count(obj):
    ct = ContentType.objects.get_for_model(obj)
    return LikeThis.objects.filter(
        content_type=ct,
        object_id=obj.pk,
    ).count()
