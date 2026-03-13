from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        # Import signals module to register signal handlers.
        # It is imported for its side effects.
        import accounts.signals  # noqa: F401
