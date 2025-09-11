from django.test import TestCase
from django.urls import reverse


class IndexViewTests(TestCase):
    def test_index_view_status_code(self):
        response = self.client.get(reverse("catalog:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template_used(self):
        response = self.client.get(reverse("catalog:index"))
        self.assertTemplateUsed(response, "catalog/index.html")

    def test_index_view_context_data(self):
        response = self.client.get(reverse("catalog:index"))
        self.assertIn("num_newspapers", response.context)
        self.assertIn("num_topics", response.context)
        self.assertIn("num_redactors", response.context)
