from django.test import TestCase

from agency.models import Topic, Redactor, Newspaper


class TestTopic(TestCase):
    def setUp(self):
        self.topic1 = Topic.objects.create(name="drama")
        self.topic2 = Topic.objects.create(name="politics")

    def test_string_representation(self):
        self.assertEqual(str(self.topic1), "drama")


class TestRedactor(TestCase):
    def setUp(self):
        self.redactor1 = Redactor.objects.create(
            years_of_experience=5,
            first_name="Jack",
            last_name="Smith",
            username="JackS",
        )

    def test_string_representation(self):
        self.assertEqual(str(self.redactor1), "JackS Jack Smith")


class TestNewspaper(TestCase):
    def setUp(self):
        self.topic1 = Topic.objects.create(name="test_topic")
        self.newspaper = Newspaper.objects.create(
            title="testtitle",
            topic=self.topic1,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.newspaper), "testtitle (Topic: test_topic)")
