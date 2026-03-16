"""Database models for publishers, articles, and newsletters."""

from django.conf import settings
from django.db import models


class Publisher(models.Model):
    """An organisation that publishes articles and newsletters."""

    name = models.CharField(max_length=150, unique=True)

    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="publisher_editor_roles",
        limit_choices_to={"role": "editor"},
    )

    journalists = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="publisher_journalist_roles",
        limit_choices_to={"role": "journalist"},
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Article(models.Model):
    """Article content submitted by a journalist for approval."""

    title = models.CharField(max_length=200)
    content = models.TextField()

    journalist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
        limit_choices_to={"role": "journalist"},
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )

    approved = models.BooleanField(default=False)

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_articles",
        limit_choices_to={"role": "editor"},
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    """Newsletter content submitted by a journalist for approval."""

    title = models.CharField(max_length=200)
    description = models.TextField()

    journalist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="newsletters",
        limit_choices_to={"role": "journalist"},
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="newsletters",
    )

    articles = models.ManyToManyField(
        Article,
        blank=True,
        related_name="newsletters",
    )

    approved = models.BooleanField(default=False)

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_newsletters",
        limit_choices_to={"role": "editor"},
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ArticleSubscription(models.Model):
    """Reader subscriptions to specific approved articles."""

    reader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="article_subscriptions",
        limit_choices_to={"role": "reader"},
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="reader_subscriptions",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("reader", "article")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reader.username} -> {self.article.title}"