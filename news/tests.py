from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Article, Newsletter, Publisher

CustomUser = get_user_model()

class NewsModelsTest(TestCase):
    """Unit tests for Publisher, Article, and Newsletter models."""

    def setUp(self):
        # Create users
        self.journalist = CustomUser.objects.create_user(
            username="journalist1",
            password="Mojalefa1999",
            role="journalist"
        )
        self.editor = CustomUser.objects.create_user(
            username="editor1",
            password="Mojalefa1999",
            role="editor"
        )

        # Create Publisher and assign roles
        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.publisher.journalists.add(self.journalist)
        self.publisher.editors.add(self.editor)

        # Create Article
        self.article = Article.objects.create(
            title="Test Article",
            content="This is a test article.",
            journalist=self.journalist,
            publisher=self.publisher,
        )

        # Create Newsletter
        self.newsletter = Newsletter.objects.create(
            title="Test Newsletter",
            content="Newsletter content",
            journalist=self.journalist,
            publisher=self.publisher,
        )

    def test_article_creation(self):
        """Test that Article instance is created correctly."""
        self.assertEqual(self.article.title, "Test Article")
        self.assertFalse(self.article.is_approved)
        self.assertEqual(self.article.journalist.username, "journalist1")
        self.assertEqual(self.article.publisher.name, "Test Publisher")
        self.assertIsNone(self.article.approved_by)

    def test_newsletter_creation(self):
        """Test that Newsletter instance is created correctly."""
        self.assertEqual(self.newsletter.title, "Test Newsletter")
        self.assertFalse(self.newsletter.is_approved)
        self.assertEqual(self.newsletter.journalist.username, "journalist1")
        self.assertEqual(self.newsletter.publisher.name, "Test Publisher")

    def test_publisher_roles(self):
        """Test that Publisher correctly links journalists and editors."""
        self.assertIn(self.journalist, self.publisher.journalists.all())
        self.assertIn(self.editor, self.publisher.editors.all())


