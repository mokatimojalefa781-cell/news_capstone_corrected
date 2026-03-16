# Generated manually for initial data

from django.db import migrations
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import make_password


def create_initial_data(apps, schema_editor):
    user_model = get_user_model()
    User = apps.get_model('accounts', 'CustomUser')
    Publisher = apps.get_model('news', 'Publisher')
    Article = apps.get_model('news', 'Article')
    Newsletter = apps.get_model('news', 'Newsletter')
    Group = apps.get_model('auth', 'Group')

    # Create groups
    reader_group, _ = Group.objects.get_or_create(name='Reader')
    journalist_group, _ = Group.objects.get_or_create(name='Journalist')
    editor_group, _ = Group.objects.get_or_create(name='Editor')

    # Create users
    editor, created = User.objects.get_or_create(
        username='editor1',
        defaults={
            'role': 'editor',
            'email': 'editor1@example.com',
            'is_staff': True,
            'password': make_password('Mojalefa1999')
        }
    )

    journalist, created = User.objects.get_or_create(
        username='journalist1',
        defaults={
            'role': 'journalist',
            'email': 'journalist1@example.com',
            'password': make_password('Mojalefa1999')
        }
    )

    reader, created = User.objects.get_or_create(
        username='reader1',
        defaults={
            'role': 'reader',
            'email': 'reader1@example.com',
            'password': make_password('Mojalefa1999')
        }
    )

    # Create publishers
    publishers = []
    for name in ['Daily News', 'Global Times', 'Tech Today']:
        pub, _ = Publisher.objects.get_or_create(name=name)
        pub.editors.add(editor)
        pub.journalists.add(journalist)
        publishers.append(pub)

    # Subscribe reader
    reader.reader_subscriptions.set(publishers)
    reader.journalist_subscriptions.add(journalist)

    # Create articles
    for pub in publishers:
        article, _ = Article.objects.get_or_create(
            title=f"{pub.name} Breaking Story",
            defaults={
                'content': f"Latest verified update from {pub.name}.",
                'publisher': pub,
                'journalist': journalist,
                'approved': True,
                'approved_by': editor
            }
        )

    # Create newsletters
    for pub in publishers:
        newsletter, _ = Newsletter.objects.get_or_create(
            title=f"{pub.name} Weekly Digest",
            defaults={
                'description': f"Weekly highlights from {pub.name}.",
                'publisher': pub,
                'journalist': journalist,
                'approved': True
            }
        )
        # Add articles to newsletter
        articles = Article.objects.filter(publisher=pub)
        newsletter.articles.set(articles)


def reverse_initial_data(apps, schema_editor):
    # Reverse is optional, but for completeness
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_rename_is_approved_article_approved_and_more'),
        ('accounts', '0002_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_initial_data, reverse_initial_data),
    ]