from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from listings.models import Listing


class Command(BaseCommand):
    help = 'Dzēš šablonus, kas nav publicēti 30 dienu laikā'

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(days=30)
        old = Listing.objects.filter(
            is_template=True,
            template_created_at__lt=cutoff,
        )
        count = old.count()
        old.delete()
        self.stdout.write(f'Dzēsti {count} novecojuši šabloni.')
