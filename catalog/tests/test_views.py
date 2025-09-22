from django.test import TestCase
from django.urls import reverse

from catalog.models import Topic, Redactor


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

# Tests for Topic Views

class TopicListViewTests(TestCase):
    def test_topic_list_view_status_code(self):
        response = self.client.get(reverse("catalog:topic-list"))
        self.assertEqual(response.status_code, 200)

    def test_topic_list_view_template_used(self):
        response = self.client.get(reverse("catalog:topic-list"))
        self.assertTemplateUsed(response, "catalog/topic_list.html")

    def test_topic_list_view_context_data(self):
        response = self.client.get(reverse("catalog:topic-list"))
        self.assertIn("topics", response.context)

    def test_topic_list_view_pagination(self):
        Topic.objects.bulk_create([
            Topic(name=f"Topic {i}") for i in range(20)
        ])

        response = self.client.get(reverse("catalog:topic-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["topics"]), 15) 

        response = self.client.get(reverse("catalog:topic-list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["topics"]), 5)


class TopicCreateViewTests(TestCase):
    def test_topic_create_view_status_code(self):
        response = self.client.get(reverse("catalog:topic-create"))
        self.assertEqual(response.status_code, 200)

    def test_topic_create_view_template_used(self):
        response = self.client.get(reverse("catalog:topic-create"))
        self.assertTemplateUsed(response, "catalog/topic_form.html")

    def test_topic_create_view_post(self):
        response = self.client.post(reverse("catalog:topic-create"), {
            "name": "New Topic"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Topic.objects.filter(name="New Topic").exists())

    def test_topic_create_view_invalid_post(self):
        response = self.client.post(reverse("catalog:topic-create"), {
            "name": ""
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "name", "This field is required.")
        self.assertFalse(Topic.objects.filter(name="").exists())

class TopicUpdateViewTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Original Topic")

    def test_topic_update_view_status_code(self):
        response = self.client.get(reverse("catalog:topic-update", args=[self.topic.pk]))
        self.assertEqual(response.status_code, 200)

    def test_topic_update_view_template_used(self):
        response = self.client.get(reverse("catalog:topic-update", args=[self.topic.pk]))
        self.assertTemplateUsed(response, "catalog/topic_form.html")

    def test_topic_update_view_post(self):
        response = self.client.post(reverse("catalog:topic-update", args=[self.topic.pk]), {
            "name": "Updated Topic"
        })
        self.assertEqual(response.status_code, 302)
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.name, "Updated Topic")

    def test_topic_update_view_invalid_post(self):
        response = self.client.post(reverse("catalog:topic-update", args=[self.topic.pk]), {
            "name": ""
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "name", "This field is required.")
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.name, "Original Topic")


class TopicDeleteViewTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Topic to be deleted")
    
    def test_topic_delete_view_status_code(self):
        response = self.client.get(reverse("catalog:topic-delete", args=[self.topic.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_topic_delete_view_template_used(self):
        response = self.client.get(reverse("catalog:topic-delete", args=[self.topic.pk]))
        self.assertTemplateUsed(response, "catalog/topic_confirm_delete.html")
    
    def test_topic_delete_view_post(self):
        response = self.client.post(reverse("catalog:topic-delete", args=[self.topic.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Topic.objects.filter(pk=self.topic.pk).exists())

# Tests for Redactor Views

class RedactorListViewTests(TestCase):
    def test_redactor_list_view_status_code(self):
        response = self.client.get(reverse("catalog:redactor-list"))
        self.assertEqual(response.status_code, 200)

    def test_redactor_list_view_template_used(self):
        response = self.client.get(reverse("catalog:redactor-list"))
        self.assertTemplateUsed(response, "catalog/redactor_list.html")
    
    def test_redactor_list_view_context_data(self):
        response = self.client.get(reverse("catalog:redactor-list"))
        self.assertIn("redactors", response.context)

    def test_redactor_list_view_pagination(self):
        Redactor.objects.bulk_create([
            Redactor(username=f"user{i}") for i in range(20)
        ])

        response = self.client.get(reverse("catalog:redactor-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["redactors"]), 15)

        response = self.client.get(reverse("catalog:redactor-list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["redactors"]), 5)


class RedactorCreateViewTests(TestCase):
    def test_redactor_create_view_status_code(self):
        response = self.client.get(reverse("catalog:redactor-create"))
        self.assertEqual(response.status_code, 200)
    
    def test_redactor_create_view_template_used(self):
        response = self.client.get(reverse("catalog:redactor-create"))
        self.assertTemplateUsed(response, "catalog/redactor_form.html")
    
    def test_redactor_create_view_post(self):
        data = {
            "username": "newuser",
            "password1": "strongpass123",
            "password2": "strongpass123",
            "first_name": "New",
            "last_name": "User",
            "years_of_experience": 5,
        }
        response = self.client.post(reverse("catalog:redactor-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Redactor.objects.filter(username="newuser").exists())

    def test_redactor_create_view_invalid_post(self):
        data = {
            "username": "",
            "password1": "strongpass123",
            "password2": "strongpass123",
            "first_name": "New",
            "last_name": "User",
            "years_of_experience": 5,
        }
        response = self.client.post(reverse("catalog:redactor-create"), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "username", "This field is required.")
        self.assertFalse(Redactor.objects.filter(username="").exists())


class RedactorUpdateViewTests(TestCase):
    def setUp(self):
        self.redactor = Redactor.objects.create_user(
            username="existinguser",
            password="strongpass123",
            first_name="Existing",
            last_name="User",
            years_of_experience=10
        )
    
    def test_redactor_update_view_status_code(self):
        response = self.client.get(reverse("catalog:redactor-update", args=[self.redactor.pk]))
        self.assertEqual(response.status_code, 200)

    def test_redactor_update_view_template_used(self):
        response = self.client.get(reverse("catalog:redactor-update", args=[self.redactor.pk]))
        self.assertTemplateUsed(response, "catalog/redactor_form.html")
    
    def test_redactor_update_view_post(self):
        data = {
            "username": "updateduser",
            "first_name": "Updated",
            "last_name": "User",
            "years_of_experience": 15,
        }
        response = self.client.post(reverse("catalog:redactor-update", args=[self.redactor.pk]), data)
        self.assertEqual(response.status_code, 302)
        self.redactor.refresh_from_db()
        self.assertEqual(self.redactor.username, "updateduser")
        self.assertEqual(self.redactor.first_name, "Updated")
        self.assertEqual(self.redactor.years_of_experience, 15)

    def test_redactor_update_view_invalid_post(self):
        data = {
            "username": "",
            "first_name": "Updated",
            "last_name": "User",
            "years_of_experience": 15,
        }
        response = self.client.post(reverse("catalog:redactor-update", args=[self.redactor.pk]), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "username", "This field is required.")
        self.redactor.refresh_from_db()
        self.assertEqual(self.redactor.username, "existinguser")

class RedactorDeleteViewTests(TestCase):
    def setUp(self):
        self.redactor = Redactor.objects.create_user(
            username="user_to_delete",
            password="strongpass123",
            first_name="User",
            last_name="ToDelete",
            years_of_experience=8
        )
    
    def test_redactor_delete_view_status_code(self):
        response = self.client.get(reverse("catalog:redactor-delete", args=[self.redactor.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_redactor_delete_view_template_used(self):
        response = self.client.get(reverse("catalog:redactor-delete", args=[self.redactor.pk]))
        self.assertTemplateUsed(response, "catalog/redactor_confirm_delete.html")
    
    def test_redactor_delete_view_post(self):
        response = self.client.post(reverse("catalog:redactor-delete", args=[self.redactor.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Redactor.objects.filter(pk=self.redactor.pk).exists())
