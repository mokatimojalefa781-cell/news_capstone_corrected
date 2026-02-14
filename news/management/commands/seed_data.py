from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from news.models import Publisher, Article

class Command(BaseCommand):
    help = 'Seed initial data for the news app'

    def handle(self, *args, **kwargs):
        user_model = get_user_model()

        editor, _ = user_model.objects.get_or_create(
            username='editor1', defaults={'password': 'password123', 'role': 'editor', 'email': 'editor1@example.com'}
        )
        journalist, _ = user_model.objects.get_or_create(
            username='journalist1', defaults={'password': 'password123', 'role': 'journalist', 'email': 'journalist1@example.com'}
        )

        publisher, _ = Publisher.objects.get_or_create(name='Daily News')
        publisher.editors.add(editor)
        publisher.journalists.add(journalist)

        article, _ = Article.objects.get_or_create(
            title='Sample Article',
            defaults={
                'content': 'This is a sample approved article.',
                'journalist': journalist,
                'publisher': publisher,
                'is_approved': True,
                'approved_by': editor
            }
        )

        self.stdout.write(self.style.SUCCESS('Seed data created successfully.'))

