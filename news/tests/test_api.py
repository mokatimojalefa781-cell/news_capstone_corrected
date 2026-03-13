from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from news.models import Article, Publisher, Newsletter


class ReaderSubscriptionAPITest(TestCase):
    def setUp(self):
        # wipe any data created by the migration so tests can assume a clean slate
        Article.objects.all().delete()
        Publisher.objects.all().delete()
        Newsletter.objects.all().delete()

        self.client = APIClient()
        user_model = get_user_model()
        # create fresh users with unique names so we never collide with migration seeds
        self.reader = user_model.objects.create_user(username="test_reader", password="pass12345", role="reader")
        self.journalist = user_model.objects.create_user(username="test_journalist", password="pass12345", role="journalist")
        self.journalist_two = user_model.objects.create_user(username="test_journalist2", password="pass12345", role="journalist")
        self.editor = user_model.objects.create_user(username="test_editor", password="pass12345", role="editor")

        # use a distinct publisher name
        self.publisher = Publisher.objects.create(name="Test Daily News")
        self.publisher.journalists.add(self.journalist)

        self.reader.reader_subscriptions.add(self.publisher)
        self.reader.journalist_subscriptions.add(self.journalist)

        self.matching_article = Article.objects.create(
            title="Matched Article", content="Visible to this reader", approved=True,
            journalist=self.journalist, publisher=self.publisher,
        )
        Article.objects.create(title="Unmatched Article", content="Should not be included", approved=True, journalist=self.journalist_two)
        Article.objects.create(title="Pending Article", content="Pending status should hide this", approved=False, journalist=self.journalist, publisher=self.publisher)

    def test_reader_gets_only_subscribed_approved_articles(self):
        token = Token.objects.create(user=self.reader)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse("news_api:reader_articles")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.matching_article.id)

    def test_non_reader_is_forbidden(self):
        token = Token.objects.create(user=self.journalist)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse("news_api:reader_articles")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_all_articles_endpoint(self):
        token = Token.objects.create(user=self.reader)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse("news_api:all_articles")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Should return 2 approved articles
        self.assertEqual(len(response.data), 2)

    def test_article_detail(self):
        token = Token.objects.create(user=self.reader)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse("news_api:article_detail", kwargs={"pk": self.matching_article.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Matched Article")

    def test_journalist_can_create_article(self):
        token = Token.objects.create(user=self.journalist)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse("news_api:article_list_create")
        data = {
            "title": "New Article",
            "content": "Content",
            "publisher": self.publisher.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_reader_cannot_create_article(self):
        token = Token.objects.create(user=self.reader)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse("news_api:article_list_create")
        data = {
            "title": "New Article",
            "content": "Content",
            "publisher": self.publisher.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_editor_can_update_article(self):
        token = Token.objects.create(user=self.editor)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse("news_api:article_update_delete", kwargs={"pk": self.matching_article.pk})
        data = {"title": "Updated Title"}
        # use PATCH to avoid needing to supply all required fields
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)

    def test_editor_can_delete_article(self):
        token = Token.objects.create(user=self.editor)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse("news_api:article_update_delete", kwargs={"pk": self.matching_article.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
