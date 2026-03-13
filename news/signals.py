from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    """Create user groups and assign permissions."""

    # Define permissions for each group
    reader_permissions = [
        # Readers can only view
    ]

    journalist_permissions = [
        ('news', 'article', 'add_article'),
        ('news', 'article', 'change_article'),
        ('news', 'article', 'delete_article'),
        ('news', 'newsletter', 'add_newsletter'),
        ('news', 'newsletter', 'change_newsletter'),
        ('news', 'newsletter', 'delete_newsletter'),
    ]

    editor_permissions = [
        ('news', 'article', 'view_article'),
        ('news', 'article', 'change_article'),
        ('news', 'article', 'delete_article'),
        ('news', 'newsletter', 'view_newsletter'),
        ('news', 'newsletter', 'change_newsletter'),
        ('news', 'newsletter', 'delete_newsletter'),
    ]

    def create_group_with_permissions(group_name, permissions):
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            for app_label, model_name, codename in permissions:
                try:
                    perm = Permission.objects.get(
                        content_type__app_label=app_label,
                        content_type__model=model_name,
                        codename=codename
                    )
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    pass  # Permission might not exist yet
        return group

    create_group_with_permissions('Reader', reader_permissions)
    create_group_with_permissions('Journalist', journalist_permissions)
    create_group_with_permissions('Editor', editor_permissions)


@receiver(post_migrate)
def create_bootstrap_content(sender, **kwargs):
    """Initial data is now created via migration 0007_initial_data."""
    pass
