import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platforma.settings')
django.setup()

from listings.profanity import contains_profanity, find_profanity

tests = [
    ('Pārdodu velosipēdu', False),
    ('Laba automašīna', False),
    ('Selling bicycle', False),
    ('what the fuck is this', True),
    ('sūda lieta', True),
    ('купить хуйню', True),
    ('Best shit ever', True),
    ('Sludinājums ar bitch vārdu', True),
    ('пизда всему', True),
    ('mudaks', True),
    ('Normal text without bad words', False),
]

all_ok = True
for text, expected in tests:
    result = contains_profanity(text)
    status = 'OK  ' if result == expected else 'KLUDDA'
    if result != expected:
        all_ok = False
    found = find_profanity(text) if result else []
    label = 'BLOKETS' if result else 'ATLAUTS'
    print(f'{status}  [{label}]  "{text}"' + (f'  -> {found}' if found else ''))

print()
print('Visi testi OK!' if all_ok else 'Ir kludas!')
