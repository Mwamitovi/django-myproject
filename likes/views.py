# likes/views.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import json
import sys
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from likes.models import LikeThis
from likes.templatetags.likes_tags import get_likes_count


if sys.version_info.major == 3:
    """In python 3, unicode was replaced by strings because of it's abundance
    Therefore if using python 2 & 3, we need to define unicode
    """
    unicode = str


@never_cache
@csrf_exempt
def json_set_like(request, content_type_id, object_id):
    """
    Sets the object as a favorite for the current user
    """
    result = {"success": False, }

    if request.user.is_authenticated() and request.method == "POST":
        content_type = ContentType.objects.get(id=content_type_id)
        obj = content_type.get_object_for_this_type(pk=object_id)
        like, is_created = LikeThis.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
            user=request.user,
        )

        if not is_created:
            like.delete()

        result = {
            "success": True,
            "obj": unicode(obj),
            "action": is_created and "added" or "removed",
            "count": get_likes_count(obj),
        }

    # json_str = json.dumps(result, ensure_ascii=False, encoding="utf8")
    json_str = json.dumps(result, ensure_ascii=False)
    # return HttpResponse(json_str, mimetype="application/json; charset=utf-8")
    return HttpResponse(json_str, content_type="application/json; charset=utf-8")
