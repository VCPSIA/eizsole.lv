from django.core.management.base import BaseCommand
from listings.matterhorn_sync import run_sync
from listings.models import MatterhornConfig


class Command(BaseCommand):
    help = 'Sinhronizē produktus no Matterhorn XML feed'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=None, help='Maks. produktu skaits (tests)')
        parser.add_argument('--force', action='store_true', help='Palaist pat ja sync_enabled=False')

    def handle(self, *args, **options):
        config = MatterhornConfig.get()

        if not config.sync_enabled and not options['force']:
            self.stdout.write('Sinhronizācija atspējota. Izmanto --force lai piespiedu kārtā.')
            return

        if not config.xml_feed_url:
            self.stderr.write('Nav XML feed URL. Konfigurē admin panelī.')
            return

        self.stdout.write(f'Sāk Matterhorn sinhronizāciju: {config.xml_feed_url[:60]}...')
        created, updated, errors = run_sync(config, limit=options['limit'])

        if isinstance(errors, str):
            self.stderr.write(f'Kļūda: {errors}')
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Pabeigts: {created} jauni, {updated} atjaunināti, {errors} kļūdas'
                )
            )
