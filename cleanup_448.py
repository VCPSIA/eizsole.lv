import django, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'platforma.settings'
django.setup()
from listings.models import Listing
try:
    l = Listing.objects.get(pk=448)
    print(f'Dzest: {l.title}')
    l.delete()
    print('Dzests.')
except Listing.DoesNotExist:
    print('Nav atrasts.')
