from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from catalog.admin import RedactorAdmin
from catalog.models import Redactor

class RedactorAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = RedactorAdmin(Redactor, self.site)

    def test_list_display(self):
        expected = ("username", "email", "first_name", "last_name", "is_staff", "years_of_experience")
        self.assertEqual(self.admin.list_display, expected)

    def test_fieldsets(self):
        fieldsets = dict(self.admin.fieldsets)
        self.assertIn("Additional info", fieldsets)
        self.assertIn("years_of_experience", fieldsets["Additional info"]["fields"])

    def test_add_fieldsets(self):
        add_fs_dict = {name: opts for name, opts in self.admin.add_fieldsets}
        self.assertIn("Additional info", add_fs_dict)
        self.assertIn("years_of_experience", add_fs_dict["Additional info"]["fields"])
