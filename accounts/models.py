from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Attributes:
        role (str): The role of the user. Can be 'reader', 'journalist', or 'editor'.
        reader_subscriptions (ManyToManyField): List of publishers a reader is subscribed to.
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

    def __str__(self):
        """
        Return the username and role for display purposes.
        """
        return f"{self.username} ({self.role})"


