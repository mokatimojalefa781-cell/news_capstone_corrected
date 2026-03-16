"""
App configuration for the News application.

This configuration ensures that Django loads the
signals module when the application starts. Signals
are used to trigger actions automatically, such as
sending notifications or newsletters when content
is created or updated.
"""

from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "news"

    def ready(self):
        import news.signals
