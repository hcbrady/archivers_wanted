from django.core.management.base import BaseCommand
from participation.models import Opportunity
from faker import Faker
import random

# run with python manage.py seed_opportunities
class Command(BaseCommand):
    help = 'Seed the database with sample Opportunity data'

    def handle(self, *args, **options):
        fake = Faker()
        num_to_create = 20

        for _ in range(num_to_create):
            title = fake.sentence(nb_words=6)
            summary = fake.paragraph(nb_sentences=3)
            Opportunity.objects.create(title=title, summary=summary)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_to_create} fake opportunities.'))
