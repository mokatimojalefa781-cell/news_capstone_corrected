from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

CustomUser = get_user_model()

class CustomUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create users
        cls.reader = CustomUser.objects.create_user(
            username="reader_test",
            password="Mojalefa1999",
            role="reader"
        )
        cls.journalist = CustomUser.objects.create_user(
            username="journalist_test",
            password="Mojalefa1999",
            role="journalist"
        )
        cls.editor = CustomUser.objects.create_user(
            username="editor_test",
            password="Mojalefa1999",
            role="editor",
            is_staff=True  # Editors should have staff status
        )

    def test_user_roles(self):
        """Check that each user has the correct role and staff status"""
        self.assertEqual(self.reader.role, "reader")
        self.assertFalse(self.reader.is_staff)

        self.assertEqual(self.journalist.role, "journalist")
        self.assertFalse(self.journalist.is_staff)

        self.assertEqual(self.editor.role, "editor")
        self.assertTrue(self.editor.is_staff)

    def test_user_group_assignment(self):
        """Check that users are assigned to the correct groups"""
        reader_group = Group.objects.get(name="Reader")
        journalist_group = Group.objects.get(name="Journalist")
        editor_group = Group.objects.get(name="Editor")

        self.assertIn(reader_group, self.reader.groups.all())
        self.assertIn(journalist_group, self.journalist.groups.all())
        self.assertIn(editor_group, self.editor.groups.all())

    def test_group_permissions(self):
        """Check that groups have the correct permissions"""
        reader_group = Group.objects.get(name="Reader")
        journalist_group = Group.objects.get(name="Journalist")
        editor_group = Group.objects.get(name="Editor")

        # Reader permissions
        reader_codenames = set(reader_group.permissions.values_list("codename", flat=True))
        self.assertSetEqual(reader_codenames, {"view_article", "view_newsletter"})

        # Journalist permissions
        journalist_codenames = set(journalist_group.permissions.values_list("codename", flat=True))
        expected_journalist = {
            "add_article", "view_article", "change_article", "delete_article",
            "add_newsletter", "view_newsletter", "change_newsletter", "delete_newsletter"
        }
        self.assertSetEqual(journalist_codenames, expected_journalist)

        # Editor permissions
        editor_codenames = set(editor_group.permissions.values_list("codename", flat=True))
        expected_editor = {
            "view_article", "change_article", "delete_article",
            "view_newsletter", "change_newsletter", "delete_newsletter"
        }
        self.assertSetEqual(editor_codenames, expected_editor)



