from django.core.management.base import BaseCommand
from django.utils import timezone
from listings.models import Listing


class Command(BaseCommand):
    help = 'Pārvērš beigušos sludinājumus par šabloniem'

    def handle(self, *args, **options):
        now = timezone.now()
        expired = Listing.objects.filter(
            expires_at__lt=now,
            is_active=True,
            is_template=False,
        )
        count = expired.count()
        expired.update(
            is_active=False,
            is_template=True,
            template_created_at=now,
            is_featured=False,
        )
        self.stdout.write(f'Pārvērsti {count} sludinājumi par šabloniem.')
