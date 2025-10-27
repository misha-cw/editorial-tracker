from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from catalog.models import Topic, Redactor, Newspaper


class IndexViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="strongpass123"
        )
        self.client.force_login(self.user)
        self.url = reverse("catalog:index")

    def test_index_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_index_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "catalog/index.html")

    def test_index_view_context_data(self):
        response = self.client.get(self.url)
        self.assertIn("num_newspapers", response.context)
        self.assertIn("num_topics", response.context)
        self.assertIn("num_redactors", response.context)

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  
        self.assertIn("/accounts/login/", response.url)

# Tests for Topic Views

class TopicListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="strongpass123"
        )
        self.client.force_login(self.user)
        self.url = reverse("catalog:topic-list")

    def test_topic_list_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_topic_list_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "catalog/topic_list.html")

    def test_topic_list_view_context_data(self):
        response = self.client.get(self.url)
        self.assertIn("topics", response.context)

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  
        self.assertIn("/accounts/login/", response.url)

    def test_topic_list_view_pagination(self):
        Topic.objects.bulk_create([
            Topic(name=f"Topic {i}") for i in range(20)
        ])

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["topics"]), 15) 

        response = self.client.get(self.url + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["topics"]), 5)

    def test_search_topic_list_view(self):
        Topic.objects.bulk_create([
            Topic(name="Science"),
            Topic(name="Sports"),
            Topic(name="Technology"),
        ])

        response = self.client.get(self.url + "?name=Tech")
        self.assertEqual(response.status_code, 200)
        self.assertIn("topics", response.context)
        topics = response.context["topics"]
        self.assertEqual(topics[0].name, "Technology")
        self.assertEqual(len(topics), 1)

    def test_search_topic_list_view_no_results(self):
        Topic.objects.bulk_create([
            Topic(name="Science"),
            Topic(name="Sports"),
            Topic(name="Technology"),
        ])

        response = self.client.get(self.url + "?name=Health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("topics", response.context)
        topics = response.context["topics"]
        self.assertEqual(len(topics), 0)

    def test_search_topic_list_view_empty_query(self):
        Topic.objects.bulk_create([
            Topic(name="Science"),
            Topic(name="Sports"),
            Topic(name="Technology"),
        ])

        response = self.client.get(self.url + "?name=")
        self.assertEqual(response.status_code, 200)
        self.assertIn("topics", response.context)
        topics = response.context["topics"]
        self.assertEqual(len(topics), 3)

    def test_search_topic_list_view_with_pagination(self):
        Topic.objects.bulk_create([
            Topic(name=f"Topic {i}") for i in range(20)
        ])

        response = self.client.get(self.url + "?name=Topic&page=2")
        self.assertEqual(response.status_code, 200)
        self.assertIn("topics", response.context)
        self.assertTrue(response.context["is_paginated"])
        topics = response.context["topics"]
        self.assertEqual(len(topics), 5)


class TopicCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="strongpass123"
        )
        self.client.force_login(self.user)
        self.url = reverse("catalog:topic-create")

    def test_topic_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_topic_create_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "catalog/topic_form.html")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  
        self.assertIn("/accounts/login/", response.url)

    def test_topic_create_view_post(self):
        response = self.client.post(self.url, {
            "name": "New Topic"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Topic.objects.filter(name="New Topic").exists())

    def test_topic_create_view_invalid_post(self):
        response = self.client.post(self.url, {
            "name": ""
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "name", "This field is required.")
        self.assertFalse(Topic.objects.filter(name="").exists())


class TopicUpdateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="strongpass123"
        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(name="Original Topic")
        self.url = reverse("catalog:topic-update", args=[self.topic.pk])

    def test_topic_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_topic_update_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "catalog/topic_form.html")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  
        self.assertIn("/accounts/login/", response.url)

    def test_topic_update_view_post(self):
        response = self.client.post(self.url, {
            "name": "Updated Topic"
        })
        self.assertEqual(response.status_code, 302)
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.name, "Updated Topic")

    def test_topic_update_view_invalid_post(self):
        response = self.client.post(self.url, {
            "name": ""
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "name", "This field is required.")
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.name, "Original Topic")


class TopicDeleteViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="strongpass123"
        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(name="Topic to be deleted")
        self.url = reverse("catalog:topic-delete", args=[self.topic.pk])
    
    def test_topic_delete_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_topic_delete_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "catalog/topic_confirm_delete.html")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  
        self.assertIn("/accounts/login/", response.url)
    
    def test_topic_delete_view_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Topic.objects.filter(pk=self.topic.pk).exists())

# Tests for Redactor Views

class RedactorListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="strongpass123"
        )
        self.client.force_login(self.user)
        self.url = reverse("catalog:redactor-list")

    def test_redactor_list_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_redactor_list_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "catalog/redactor_list.html")
    
    def test_redactor_list_view_context_data(self):
        response = self.client.get(self.url)
        self.assertIn("redactors", response.context)

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  
        self.assertIn("/accounts/login/", response.url)

    def test_redactor_list_view_pagination(self):
        get_user_model().objects.bulk_create([
            Redactor(username=f"user{i}") for i in range(20)
        ])

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["redactors"]), 15)

        response = self.client.get(self.url + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["redactors"]), 6)

    def test_search_redactor_list_view(self):
        get_user_model().objects.bulk_create([
            Redactor(username="alice"),
            Redactor(username="bob"),
            Redactor(username="charlie"),
        ])
        response = self.client.get(self.url + "?username=bo")
        self.assertEqual(response.status_code, 200)
        self.assertIn("redactors", response.context)
        redactors = response.context["redactors"]
        self.assertEqual(redactors[0].username, "bob")
        self.assertEqual(len(redactors), 1)

    def test_search_redactor_list_view_no_results(self):
        get_user_model().objects.bulk_create([
            Redactor(username="alice"),
            Redactor(username="bob"),
            Redactor(username="charlie"),
        ])
        response = self.client.get(self.url + "?username=dan")
        self.assertEqual(response.status_code, 200)
        self.assertIn("redactors", response.context)
        redactors = response.context["redactors"]
        self.assertEqual(len(redactors), 0)
    
    def test_search_redactor_list_view_empty_query(self):
        get_user_model().objects.bulk_create([
            Redactor(username="alice"),
            Redactor(username="bob"),
            Redactor(username="charlie"),
        ])
        response = self.client.get(self.url + "?username=")
        self.assertEqual(response.status_code, 200)
        self.assertIn("redactors", response.context)
        redactors = response.context["redactors"]
        self.assertEqual(len(redactors), 4)

    def test_search_redactor_list_view_with_pagination(self):
        get_user_model().objects.bulk_create([
            Redactor(username=f"user{i}") for i in range(20)
        ])

        response = self.client.get(self.url + "?username=user&page=2")
        self.assertEqual(response.status_code, 200)
        self.assertIn("redactors", response.context)
        self.assertTrue(response.context["is_paginated"])
        redactors = response.context["redactors"]
        self.assertEqual(len(redactors), 6)


class RedactorDetailViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="strongpass123",
            first_name="Test",
            last_name="User",
            years_of_experience=5
        )
        self.client.force_login(self.user)
        self.url = reverse("catalog:redactor-detail", args=[self.user.pk])
    
    def test_redactor_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_redactor_detail_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "catalog/redactor_detail.html")
    
    def test_redactor_detail_view_context_data(self):
        response = self.client.get(self.url)
        self.assertIn("redactor", response.context)
        self.assertEqual(response.context["redactor"], self.user)

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  
        self.assertIn("/accounts/login/", response.url)


class RedactorCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="strongpass123"
        )
        self.client.force_login(self.user)
        self.url = reverse("catalog:redactor-create")

    def test_redactor_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_redactor_create_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "catalog/redactor_form.html")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  
        self.assertIn("/accounts/login/", response.url)
    
    def test_redactor_create_view_post(self):
        data = {
            "username": "newuser",
            "password1": "strongpass123",
            "password2": "strongpass123",
            "first_name": "New",
            "last_name": "User",
            "years_of_experience": 5,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username="newuser").exists())

    def test_redactor_create_view_invalid_post(self):
        data = {
            "username": "",
            "password1": "strongpass123",
            "password2": "strongpass123",
            "first_name": "New",
            "last_name": "User",
            "years_of_experience": 5,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "username", "This field is required.")
        self.assertFalse(get_user_model().objects.filter(username="").exists())


class RedactorUpdateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="existinguser",
            password="strongpass123",
            first_name="Existing",
            last_name="User",
            years_of_experience=10
        )
        self.client.force_login(self.user)
        self.url = reverse("catalog:redactor-update", args=[self.user.pk])
    
    def test_redactor_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_redactor_update_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "catalog/redactor_form.html")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  
        self.assertIn("/accounts/login/", response.url)
    
    def test_redactor_update_view_post(self):
        data = {
            "username": "updateduser",
            "first_name": "Updated",
            "last_name": "User",
            "years_of_experience": 15,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.years_of_experience, 15)

    def test_redactor_update_view_invalid_post(self):
        data = {
            "username": "",
            "first_name": "Updated",
            "last_name": "User",
            "years_of_experience": 15,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "username", "This field is required.")
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "existinguser")

class RedactorDeleteViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user_to_delete",
            password="strongpass123",
            first_name="User",
            last_name="ToDelete",
            years_of_experience=8
        )
        self.client.force_login(self.user)
        self.url = reverse("catalog:redactor-delete", args=[self.user.pk])
    
    def test_redactor_delete_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_redactor_delete_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "catalog/redactor_confirm_delete.html")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  
        self.assertIn("/accounts/login/", response.url)
    
    def test_redactor_delete_view_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(get_user_model().objects.filter(pk=self.user.pk).exists())

# Tests for Newspaper Views

class NewspaperListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="strongpass123"
        )
        self.client.force_login(self.user)
        self.url = reverse("catalog:newspaper-list")

    def test_newspaper_list_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_newspaper_list_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "catalog/newspaper_list.html")
    
    def test_newspaper_list_view_context_data(self):
        response = self.client.get(self.url)
        self.assertIn("newspapers", response.context)

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  
        self.assertIn("/accounts/login/", response.url)

    def test_newspaper_list_view_pagination(self):
        Newspaper.objects.bulk_create([
            Newspaper(title=f"Newspaper {i}", content="Sample content") for i in range(12)
        ])

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["newspapers"]), 9)

        response = self.client.get(self.url + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["newspapers"]), 3)

    def test_search_newspaper_list_view(self):
        Newspaper.objects.bulk_create([
            Newspaper(title="Daily News", content="Content 1"),
            Newspaper(title="Global Times", content="Content 2"),
            Newspaper(title="Tech Today", content="Content 3"),
        ])
        response = self.client.get(self.url + "?title=Tech")
        self.assertEqual(response.status_code, 200)
        self.assertIn("newspapers", response.context)
        newspapers = response.context["newspapers"]
        self.assertEqual(newspapers[0].title, "Tech Today")
        self.assertEqual(len(newspapers), 1)

    def test_search_newspaper_list_view_no_results(self):
        Newspaper.objects.bulk_create([
            Newspaper(title="Daily News", content="Content 1"),
            Newspaper(title="Global Times", content="Content 2"),
            Newspaper(title="Tech Today", content="Content 3"),
        ])
        response = self.client.get(self.url + "?title=Health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("newspapers", response.context)
        newspapers = response.context["newspapers"]
        self.assertEqual(len(newspapers), 0)

    def test_search_newspaper_list_view_empty_query(self):
        Newspaper.objects.bulk_create([
            Newspaper(title="Daily News", content="Content 1"),
            Newspaper(title="Global Times", content="Content 2"),
            Newspaper(title="Tech Today", content="Content 3"),
        ])
        response = self.client.get(self.url + "?title=")
        self.assertEqual(response.status_code, 200)
        self.assertIn("newspapers", response.context)
        newspapers = response.context["newspapers"]
        self.assertEqual(len(newspapers), 3)

    def test_search_newspaper_list_view_with_pagination(self):
        Newspaper.objects.bulk_create([
            Newspaper(title=f"Newspaper {i}", content="Sample content") for i in range(14)
        ])

        response = self.client.get(self.url + "?title=Newspaper&page=2")
        self.assertEqual(response.status_code, 200)
        self.assertIn("newspapers", response.context)
        self.assertTrue(response.context["is_paginated"])
        newspapers = response.context["newspapers"]
        self.assertEqual(len(newspapers), 5)


class NewspaperCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="strongpass123"
        )
        self.client.force_login(self.user)
        self.url = reverse("catalog:newspaper-create")

    def test_newspaper_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_newspaper_create_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "catalog/newspaper_form.html")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  
        self.assertIn("/accounts/login/", response.url)
    
    def test_newspaper_create_view_post(self):
        topic = Topic.objects.create(name="Sample Topic")

        data = {
            "title": "New Newspaper",
            "content": "This is the content of the newspaper.",
            "publishers": [self.user.pk],
            "topics": [topic.pk],
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Newspaper.objects.filter(title="New Newspaper").exists())

    def test_newspaper_create_view_invalid_post(self):
        data = {
            "title": "",
            "content": "This is the content of the newspaper.",
            "publishers": [],
            "topics": [],
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "title", "This field is required.")
        self.assertFalse(Newspaper.objects.filter(title="").exists())


class NewspaperUpdateViewTests(TestCase):
    def setUp(self):
        self.newspaper = Newspaper.objects.create(
            title="Original Newspaper",
            content="Original content"
        )
        self.user = get_user_model().objects.create_user(
            username="publisher1",
            password="strongpass123"
        )
        self.topic = Topic.objects.create(name="Sample Topic")
        self.newspaper.publishers.add(self.user)
        self.newspaper.topics.add(self.topic)
        self.client.force_login(self.user)
        self.url = reverse("catalog:newspaper-update", args=[self.newspaper.pk])
    
    def test_newspaper_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_newspaper_update_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "catalog/newspaper_form.html")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  
        self.assertIn("/accounts/login/", response.url)
    
    def test_newspaper_update_view_post(self):
        new_user = get_user_model().objects.create_user(username="publisher2", password="strongpass123")
        new_topic = Topic.objects.create(name="New Topic")

        data = {
            "title": "Updated Newspaper",
            "content": "Updated content",
            "publishers": [new_user.pk],
            "topics": [new_topic.pk],
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.newspaper.refresh_from_db()
        self.assertEqual(self.newspaper.title, "Updated Newspaper")
        self.assertEqual(self.newspaper.content, "Updated content")
        self.assertIn(new_user, self.newspaper.publishers.all())
        self.assertIn(new_topic, self.newspaper.topics.all())

    def test_newspaper_update_view_invalid_post(self):
        data = {
            "title": "",
            "content": "Updated content",
            "publishers": [],
            "topics": [],
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "title", "This field is required.")
        self.newspaper.refresh_from_db()
        self.assertEqual(self.newspaper.title, "Original Newspaper")


class NewspaperDeleteViewTests(TestCase):
    def setUp(self):
        self.newspaper = Newspaper.objects.create(
            title="Newspaper to be deleted",
            content="Content to be deleted"
        )
        self.user = get_user_model().objects.create_user(
            username="publisher1",
            password="strongpass123"
        )
        self.client.force_login(self.user)
        self.url = reverse("catalog:newspaper-delete", args=[self.newspaper.pk])
    
    def test_newspaper_delete_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_newspaper_delete_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "catalog/newspaper_confirm_delete.html")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  
        self.assertIn("/accounts/login/", response.url)
    
    def test_newspaper_delete_view_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Newspaper.objects.filter(pk=self.newspaper.pk).exists())


class NewspaperDetailViewTests(TestCase):
    def setUp(self):
        self.newspaper = Newspaper.objects.create(
            title="Sample Newspaper",
            content="Sample content"
        )
        self.user = get_user_model().objects.create_user(
            username="publisher1", 
            password="strongpass123"
        )
        self.topic = Topic.objects.create(name="Sample Topic")
        self.newspaper.publishers.add(self.user)
        self.newspaper.topics.add(self.topic)
        self.client.force_login(self.user)
        self.url = reverse("catalog:newspaper-detail", args=[self.newspaper.pk])
    
    def test_newspaper_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_newspaper_detail_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "catalog/newspaper_detail.html")
    
    def test_newspaper_detail_view_context_data(self):
        response = self.client.get(self.url)
        self.assertIn("newspaper", response.context)
        self.assertEqual(response.context["newspaper"], self.newspaper)

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  
        self.assertIn("/accounts/login/", response.url)
    