from django.core.management.base import BaseCommand
from django.utils import timezone
from listings.models import Listing


class Command(BaseCommand):
    help = 'Dzēš sludinājumus, kuriem beidzies publicēšanas termiņš'

    def handle(self, *args, **options):
        expired = Listing.objects.filter(
            expires_at__lt=timezone.now(),
            is_active=True,
        )
        count = expired.count()
        expired.delete()
        self.stdout.write(f'Dzēsti {count} izbeigtie sludinājumi.')
