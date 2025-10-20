from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from agency.models import Newspaper, Topic

class PublicViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.topic = Topic.objects.create(name="Test Topic")
        cls.newspaper = Newspaper.objects.create(
            title="Test Newspaper",
            content="Content",
            topic=cls.topic,
        )
        cls.redactor = get_user_model().objects.create_user(
            username="testuser", password="pass123"
        )
        cls.newspaper.publishers.add(cls.redactor)

    def setUp(self):
        self.client = Client()

    def test_login_required_for_all_views(self):
        urls = [
            reverse("agency:index"),
            reverse("agency:newspaper-list"),
            reverse("agency:newspaper-detail", args=[self.newspaper.id]),
            reverse("agency:newspaper-create"),
            reverse("agency:newspaper-update", args=[self.newspaper.id]),
            reverse("agency:newspaper-delete", args=[self.newspaper.id]),
            reverse("agency:topic-list"),
            reverse("agency:redactor-list"),
            reverse("agency:redactor-detail", args=[self.redactor.id]),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)


class PrivateViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.topic = Topic.objects.create(name="Test Topic")
        cls.newspaper = Newspaper.objects.create(
            title="Test Newspaper",
            content="Content",
            topic=cls.topic,
        )
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="pass123"
        )
        cls.newspaper.publishers.add(cls.user)

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)

    def test_index_view(self):
        url = reverse("agency:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, Newspaper.objects.count())
        self.assertContains(response, Topic.objects.count())
        self.assertContains(response, get_user_model().objects.count())

    # Newspaper
    def test_newspaper_list_view(self):
        url = reverse("agency:newspaper-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "agency/newspaper_list.html")
        self.assertIn(self.newspaper, response.context["newspaper_list"])

    def test_newspaper_detail_view(self):
        url = reverse("agency:newspaper-detail", args=[self.newspaper.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "agency/newspaper_detail.html")
        self.assertEqual(response.context["object"], self.newspaper)

    def test_newspaper_create_view(self):
        url = reverse("agency:newspaper-create")
        data = {"title": "New Paper", "content": "Some content", "topic": self.topic.id, "publishers": [self.user.id],}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Newspaper.objects.filter(title="New Paper").exists())

    def test_newspaper_update_view(self):
        url = reverse("agency:newspaper-update", args=[self.newspaper.id])
        data = {"title": "Updated Title", "content": "Updated content", "topic": self.topic.id, "publishers": [self.user.id],}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.newspaper.refresh_from_db()
        self.assertEqual(self.newspaper.title, "Updated Title")

    def test_newspaper_delete_view(self):
        url = reverse("agency:newspaper-delete", args=[self.newspaper.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Newspaper.objects.filter(id=self.newspaper.id).exists())

    # Topic
    def test_topic_list_view(self):
        url = reverse("agency:topic-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "agency/topic_list.html")
        self.assertIn(self.topic, response.context["topic_list"])

    # Redactor
    def test_redactor_list_view(self):
        url = reverse("agency:redactor-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "agency/redactor_list.html")
        self.assertIn(self.user, response.context["redactor_list"])

    def test_redactor_detail_view(self):
        url = reverse("agency:redactor-detail", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "agency/redactor_detail.html")
        self.assertEqual(response.context["object"], self.user)
