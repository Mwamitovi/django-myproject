# bulletin_board/tests.py
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, Bulletin


class BulletinTests(APITestCase):
    category = None
    bulletin = None
    superuser = None

    @classmethod
    def setUpClass(cls):
        super(BulletinTests, cls).setUpClass()
        cls.superuser, created = User.objects.get_or_create(username="test-admin", )
        cls.superuser.is_active = True
        cls.superuser.is_superuser = True
        cls.superuser.save()
        cls.category = Category.objects.create(title="Movies")

        cls.bulletin = Bulletin.objects.create(
            bulletin_type="searching",
            category=cls.category,
            title="The Escapades",
            description="There is no way back for a techie.",
            contact_person="Martin Matovu",
        )
        cls.bulletin_to_delete = Bulletin.objects.create(
            bulletin_type="searching",
            category=cls.category,
            title="Hunting for land",
            description="Real Estate: "
                        "There's a difference, "
                        "between a hunting and searching.",
            contact_person="Martin Matovu",
        )

    @classmethod
    def tearDownClass(cls):
        super(BulletinTests, cls).tearDownClass()
        cls.category.delete()
        cls.bulletin.delete()
        cls.superuser.delete()

    def test_list_bulletins(self):
        url = reverse("rest_bulletin_list")
        data = {}
        response = self.client.get(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], Bulletin.objects.count())

    def test_get_bulletin(self):
        url = reverse("rest_bulletin_detail", kwargs={"pk": self.bulletin.pk})
        data = {}
        response = self.client.get(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.bulletin.pk)
        self.assertEqual(response.data["bulletin_type"], self.bulletin.bulletin_type)
        self.assertEqual(response.data["category"]["id"], self.category.pk)
        self.assertEqual(response.data["title"], self.bulletin.title)
        self.assertEqual(response.data["description"], self.bulletin.description)
        self.assertEqual(response.data["contact_person"], self.bulletin.contact_person)

    def test_create_bulletin_allowed(self):
        # login
        self.client.force_authenticate(user=self.superuser)
        url = reverse("rest_bulletin_list")
        data = {
            "bulletin_type": "offering",
            "category": {"title": self.category.title},
            "title": "Back to the Future",
            "description": "Roads? Where we're going, we don't need roads.",
            "contact_person": "Martin Matovu",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Bulletin.objects.filter(pk=response.data["id"]).count() == 1)
        # logout
        self.client.force_authenticate(user=None)

    def test_create_bulletin_restricted(self):
        # make sure the user is logged out
        self.client.force_authenticate(user=None)
        url = reverse("rest_bulletin_list")
        data = {
            "bulletin_type": "offering",
            "category": {"title": self.category.title},
            "title": "Back to the Future",
            "description": "Roads? Where we're going, we don't need roads.",
            "contact_person": "Martin Matovu",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_change_bulletin_allowed(self):
        # login
        self.client.force_authenticate(user=self.superuser)
        url = reverse("rest_bulletin_detail", kwargs={"pk": self.bulletin.pk})
        # change only title
        data = {
            "bulletin_type": self.bulletin.bulletin_type,
            "category": {"title": self.bulletin.category.title},
            "title": "Going the extra mile",
            "description": self.bulletin.description,
            "contact_person": self.bulletin.contact_person,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.bulletin.pk)
        self.assertEqual(response.data["bulletin_type"], "searching")
        # logout
        self.client.force_authenticate(user=None)

    def test_change_bulletin_restricted(self):
        # make sure the user is logged out
        self.client.force_authenticate(user=None)
        url = reverse("rest_bulletin_detail", kwargs={"pk": self.bulletin.pk})
        # change only title
        data = {
            "bulletin_type": self.bulletin.bulletin_type,
            "category": {"title": self.bulletin.category.title},
            "title": "Going the extra mile",
            "description": self.bulletin.description,
            "contact_person": self.bulletin.contact_person,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_delete_bulletin_allowed(self):
        # login
        self.client.force_authenticate(user=self.superuser)
        url = reverse("rest_bulletin_detail", kwargs={"pk": self.bulletin_to_delete.pk})
        data = {}
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # logout
        self.client.force_authenticate(user=None)

    def test_delete_bulletin_restricted(self):
        # make sure the user is logged out
        self.client.force_authenticate(user=None)
        url = reverse("rest_bulletin_detail", kwargs={"pk": self.bulletin_to_delete.pk})
        data = {}
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
