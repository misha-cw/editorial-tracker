from django.test import TestCase

from catalog.forms import (
    RedactorCreateForm,
    RedactorUpdateForm,
)


class RedactorCreateFormTests(TestCase):
    def test_redactor_create_form_valid_data(self):
        data = {
            "username": "testuser",
            "password1": "strongpass123",
            "password2": "strongpass123",
            "first_name": "John",
            "last_name": "Doe",
            "years_of_experience": 5,
        }
        form = RedactorCreateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_redactor_create_form_invalid_years_of_experience(self):
        data = {
            "username": "testuser",
            "password1": "strongpass123",
            "password2": "strongpass123",
            "first_name": "John",
            "last_name": "Doe",
            "years_of_experience": 150,
        }
        form = RedactorCreateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "years_of_experience",
            "Years of experience must be between 0 and 100.",
        )


class RedactorUpdateFormTests(TestCase):
    def test_redactor_update_form_valid_data(self):
        data = {
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "years_of_experience": 10,
        }
        form = RedactorUpdateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_redactor_update_form_invalid_years_of_experience(self):
        data = {
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "years_of_experience": -5,
        }
        form = RedactorUpdateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "years_of_experience",
            "Years of experience must be between 0 and 100.",
        )
