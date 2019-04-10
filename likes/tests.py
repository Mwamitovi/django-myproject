# likes/tests.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import mock
import json
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.test import SimpleTestCase
from locations.models import Location


class JSSetLikeViewTest(SimpleTestCase):
    location = None
    superuser = None

    @classmethod
    def setUpClass(cls):
        super(JSSetLikeViewTest, cls).setUpClass()
        # cls.browser = webdriver.Chrome(os.path.join(BASE_DIRECTORY, 'chromedriver'))
        # cls.browser.delete_all_cookies()
        cls.location = Location.objects.create(
            title="Lubya Hill",
            slug="lubya-hill",
            small_image="locations/2019/03/201903271250_small.jpg",
            medium_image="locations/2019/03/201903271250_medium.jpg",
            large_image="locations/2019/03/201903271250_large.jpg",
        )
        cls.content_type = ContentType.objects.get_for_model(Location)
        cls.username = "test-admin"
        cls.password = "test-admin"
        cls.superuser = User.objects.create_superuser(
            username=cls.username,
            password=cls.password,
            email="",
        )

    @classmethod
    def tearDownClass(cls):
        super(JSSetLikeViewTest, cls).tearDownClass()
        cls.location.delete()
        cls.superuser.delete()

    def test_authenticated_json_set_like(self):
        from .views import json_set_like
        mock_request = mock.Mock()
        mock_request.user = self.superuser
        mock_request.method = "POST"
        response = json_set_like(
            mock_request,
            self.content_type.pk,
            self.location.pk
        )
        expected_result = json.dumps({
            "success": True,
            "action": "added",
            "obj": self.location.title,
            "count": Location.objects.count(),
        })
        self.assertJSONEqual(
            response.content,
            expected_result
        )

    def test_anonymous_json_set_like(self):
        from .views import json_set_like
        mock_request = mock.Mock()
        mock_request.user.is_authenticated.return_value = False
        mock_request.method = "POST"
        response = json_set_like(
            mock_request,
            self.content_type.pk,
            self.location.pk
        )
        expected_result = json.dumps({
            "success": False,
        })
        self.assertJSONEqual(
            response.content,
            expected_result
        )
