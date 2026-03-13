"""
Custom user model for the News Application.
# Feature: Added user profile enhancements

This model extends Django's AbstractUser to support
role-based access control and subscription features.

Roles supported:
- Reader
- Journalist
- Editor

Readers can subscribe to publishers and journalists
to receive updates and newsletters.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model with role-based access control.
    """

    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ('journalist', 'Journalist'),
        ('editor', 'Editor'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        help_text="Role of the user: reader, journalist, or editor."
    )

    reader_subscriptions = models.ManyToManyField(
        'news.Publisher',
        blank=True,
        related_name='subscribed_readers',
        help_text="Publishers that this reader is subscribed to."
    )

    journalist_subscriptions = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='journalist_subscribers',
        limit_choices_to={'role': 'journalist'},
        help_text="Journalists that this reader is subscribed to."
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
