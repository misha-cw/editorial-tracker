from django.test import TestCase
from django.utils import timezone

from catalog.models import Topic, Redactor, Newspaper


class TopicModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Science")

    def test_topic_creation(self):
        self.assertEqual(self.topic.name, "Science")

    def test_topic_str(self):
        self.assertEqual(str(self.topic), "Science")


class RedactorModelTest(TestCase):
    def setUp(self):
        self.redactor = Redactor.objects.create_user(
            username="john_doe", password="password123", years_of_experience=5
        )

    def test_redactor_creation(self):
        self.assertEqual(self.redactor.username, "john_doe")
        self.assertEqual(self.redactor.years_of_experience, 5)

    def test_redactor_str(self):
        self.assertEqual(str(self.redactor), "john_doe")


class NewspaperModelTest(TestCase):
    def setUp(self):
        self.topic1 = Topic.objects.create(name="Science")
        self.topic2 = Topic.objects.create(name="Technology")
        self.redactor1 = Redactor.objects.create_user(
            username="john_doe", password="password123", years_of_experience=5
        )
        self.redactor2 = Redactor.objects.create_user(
            username="jane_smith", password="password456", years_of_experience=3
        )
        self.newspaper = Newspaper.objects.create(
            title="Tech Innovations",
            content="Latest advancements in technology.",
        )
        self.created_time = timezone.now()
        self.newspaper.topics.set([self.topic1, self.topic2])
        self.newspaper.publishers.set([self.redactor1, self.redactor2])

    def test_newspaper_creation(self):
        self.assertEqual(self.newspaper.title, "Tech Innovations")
        self.assertEqual(self.newspaper.content, "Latest advancements in technology.")
        self.assertTrue(
            (self.created_time - self.newspaper.published_date).total_seconds() < 1
        )
        self.assertEqual(self.newspaper.topics.count(), 2)
        self.assertEqual(self.newspaper.publishers.count(), 2)

    def test_newspaper_str(self):
        expected_str = "Tech Innovations by john_doe, jane_smith"
        self.assertEqual(str(self.newspaper), expected_str)
