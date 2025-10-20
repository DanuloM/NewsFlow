from traceback import format_stack

from django.test import TestCase
from agency.forms import RedactorCreationForm, RedactorUpdateNewspapersForm, SearchForm
from agency.models import Newspaper, Redactor, Topic
from django.contrib.auth import get_user_model


class TestRedactorCreationForm(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test Topic")
        self.newspaper = Newspaper.objects.create(title="Paper", content="Content", topic=self.topic)

    def test_form_valid_data(self):
        form_data = {
            "username": "testuser",
            "password1": "ComplexPassword!123",
            "password2": "ComplexPassword!123",
            "first_name": "Test",
            "last_name": "User",
            "years_of_experience": 1,
            "newspapers": [str(self.newspaper.id)],
        }
        form = RedactorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_empty_newspapers(self):
        form_data = {
            "username": "testuser2",
            "password1": "ComplexPassword!123",
            "password2": "ComplexPassword!123",
            "first_name": "Test2",
            "last_name": "User2",
            "years_of_experience": 2,
        }
        form = RedactorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestRedactorUpdateNewspapersForm(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test Topic")
        self.redactor = get_user_model().objects.create_user(username="user1", password="pass")
        self.newspaper1 = Newspaper.objects.create(title="Paper1", content="C1", topic_id=1)
        self.newspaper2 = Newspaper.objects.create(title="Paper2", content="C2", topic_id=1)
        self.redactor.newspapers.add(self.newspaper1)

    def test_initial_newspapers(self):
        form = RedactorUpdateNewspapersForm(instance=self.redactor)
        self.assertIn(self.newspaper1, form.fields["newspapers"].initial)
        self.assertNotIn(self.newspaper2, form.fields["newspapers"].initial)

    def test_form_valid_data(self):
        form_data = {"newspapers": [self.newspaper2.id]}
        form = RedactorUpdateNewspapersForm(data=form_data, instance=self.redactor)
        self.assertTrue(form.is_valid())


class TestSearchForm(TestCase):
    def test_form_valid_empty(self):
        form = SearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_form_valid_with_query(self):
        form = SearchForm(data={"query": "test"})
        self.assertTrue(form.is_valid())

    def test_form_invalid_too_long(self):
        form = SearchForm(data={"query": "x"*256})
        self.assertFalse(form.is_valid())
