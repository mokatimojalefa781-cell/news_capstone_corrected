from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from news.models import Publisher, Article, Newsletter

class Command(BaseCommand):
    help = 'Seed initial data for the news app'

    def handle(self, *args, **kwargs):
        user_model = get_user_model()

        # -------------------------
        # Create editor and journalist
        # -------------------------
        editor, _ = user_model.objects.get_or_create(
            username='editor1',
            defaults={'password': 'Mojalefa1999', 'role': 'editor', 'email': 'editor1@example.com'}
        )
        journalist, _ = user_model.objects.get_or_create(
            username='journalist1',
            defaults={'password': 'Mojalefa1999', 'role': 'journalist', 'email': 'journalist1@example.com'}
        )

        # -------------------------
        # Create publishers
        # -------------------------
        publishers = []
        for name in ['Daily News', 'Global Times', 'Tech Today']:
            pub, _ = Publisher.objects.get_or_create(name=name)
            # Add editor/journalist to the publisher if your model supports these relationships
            if hasattr(pub, 'editors'):
                pub.editors.add(editor)
            if hasattr(pub, 'journalists'):
                pub.journalists.add(journalist)
            publishers.append(pub)

        # -------------------------
        # Create readers
        # -------------------------
        readers = []
        for i in range(1, 4):
            reader, created = user_model.objects.get_or_create(
                username=f'reader{i}',
                defaults={'password': 'Mojalefa1999', 'role': 'reader'}
            )
            # Subscribe reader to all publishers
            if hasattr(reader, 'reader_subscriptions'):
                reader.reader_subscriptions.set(publishers)
            readers.append(reader)

        # -------------------------
        # Create articles
        # -------------------------
        for pub in publishers:
            for j in range(1, 3):
                Article.objects.get_or_create(
                    title=f"{pub.name} Article {j}",
                    defaults={
                        'content': f"This is article {j} from {pub.name}.",
                        'publisher': pub,
                        'journalist': journalist,
                        'approved': True,
                        'approved_by': editor
                    }
                )

        # -------------------------
        # Create newsletters
        # -------------------------
        for pub in publishers:
            Newsletter.objects.get_or_create(
                title=f"{pub.name} Newsletter",
                defaults={
                    'description': f"Weekly highlights from {pub.name}.",
                    'publisher': pub,
                    'journalist': journalist,
                    'approved': True
                }
            )

        self.stdout.write(self.style.SUCCESS('✅ Seed data created successfully!'))
