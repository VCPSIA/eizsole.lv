from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from listings.models import SavedSearch


class Command(BaseCommand):
    help = 'Sūta e-pasta paziņojumus par jauniem sludinājumiem saglabātajām meklēšanām'

    def handle(self, *args, **options):
        sent = 0
        for saved in SavedSearch.objects.select_related('user', 'category').iterator():
            since = saved.last_notified or saved.created_at
            new_listings = saved.get_matching_listings(since=since)[:10]

            if not new_listings:
                continue

            count = len(new_listings)
            label = saved.get_label()
            search_url = f'https://eizsole.lv{saved.get_url()}'

            lines = [f'Sveiki, {saved.user.username}!\n']
            lines.append(f'Parādījās {count} jaun{"s sludinājums" if count == 1 else "i sludinājumi"} jūsu saglabātajai meklēšanai: {label}\n')
            for listing in new_listings:
                price = f'€{listing.price}' if listing.price else 'Cena pēc vienošanās'
                lines.append(f'• {listing.title} — {price}')
                lines.append(f'  https://eizsole.lv/sludinajums/{listing.pk}/')
            lines.append(f'\nSkatīt visus rezultātus: {search_url}')
            lines.append('\n— eizsole.lv komanda')
            lines.append('\nLai atteiktos no paziņojumiem, dzēsiet saglabāto meklēšanu: https://eizsole.lv/saglabatas-meklesanas/')

            try:
                send_mail(
                    subject=f'Jauni sludinājumi: {label} — eizsole.lv',
                    message='\n'.join(lines),
                    from_email='info@eizsole.lv',
                    recipient_list=[saved.user.email],
                    fail_silently=False,
                )
                saved.last_notified = timezone.now()
                saved.save(update_fields=['last_notified'])
                sent += 1
            except Exception as e:
                self.stderr.write(f'Kļūda sūtot uz {saved.user.email}: {e}')

        self.stdout.write(f'Nosūtīti {sent} paziņojumi.')
