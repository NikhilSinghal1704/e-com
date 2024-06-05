from django.core.management.base import BaseCommand
from Website.models import Category

class Command(BaseCommand):
    help = 'Add default categories to the database'

    def handle(self, *args, **kwargs):
        categories = [
            {"name": "Science Fiction", "description": "A genre of speculative fiction that typically deals with imaginative and futuristic concepts."},
            {"name": "Fantasy", "description": "A genre of speculative fiction set in a fictional universe, often inspired by real world myth and folklore."},
            {"name": "Mystery", "description": "A genre of fiction that involves a mysterious death or a crime to be solved."},
            {"name": "Thriller", "description": "A genre characterized by excitement and suspense."},
            {"name": "Romance", "description": "A genre centered on romantic relationships between characters."},
            {"name": "Horror", "description": "A genre intended to scare, unsettle, or horrify the audience."},
            {"name": "Non-Fiction", "description": "A genre that is based on factual information and real events."},
            {"name": "Historical Fiction", "description": "A genre that takes place in the past, often during a significant time period."},
            {"name": "Biography", "description": "A detailed description of a person's life."},
            {"name": "Self-Help", "description": "A genre intended to help readers solve personal problems and improve their lives."}
        ]

        for category in categories:
            obj, created = Category.objects.get_or_create(name=category["name"], defaults={"description": category["description"]})
            if created:
                self.stdout.write(self.style.SUCCESS(f'Category "{category["name"]}" created.'))
            else:
                self.stdout.write(self.style.WARNING(f'Category "{category["name"]}" already exists.'))
