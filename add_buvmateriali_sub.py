import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platforma.settings')
django.setup()

from listings.models import Category

parent = Category.objects.get(slug='celt-buvmateriali')

subcats = {
    ('Kokmateriāli', 'celt-buvm-koks', 'tree'): [
        ('Baļķi un zāģmateriāli', 'celt-buvm-koks-balkji'),
        ('Dēļi un plankas', 'celt-buvm-koks-deli'),
        ('Sijas un latas', 'celt-buvm-koks-sijas'),
        ('Finiera plāksnes', 'celt-buvm-koks-finiera'),
        ('OSB plāksnes', 'celt-buvm-koks-osb'),
        ('Lamēlkoks (LVL, CLT, BSH)', 'celt-buvm-koks-lamelkoks'),
        ('Karkasa māju elementi', 'celt-buvm-koks-karkass'),
        ('Terases dēļi un klājumi', 'celt-buvm-koks-terases'),
        ('Koka paneļi un listes', 'celt-buvm-koks-paneli'),
        ('Malka un šķelda', 'celt-buvm-koks-malka'),
        ('Citi kokmateriāli', 'celt-buvm-koks-citi'),
    ],
    ('Metāli', 'celt-buvm-metali', 'grid-3x3'): [
        ('Tērauda sijas un profili', 'celt-buvm-met-sijas'),
        ('Armatūras tērauds', 'celt-buvm-met-armatura'),
        ('Metāla loksnes un ruļļi', 'celt-buvm-met-loksnes'),
        ('Alumīnija profili', 'celt-buvm-met-al-profili'),
        ('Metāla caurules', 'celt-buvm-met-caurules'),
        ('Nerūsošais tērauds', 'celt-buvm-met-nerustejoss'),
        ('Vara un misiņa izstrādājumi', 'celt-buvm-met-vara'),
        ('Metāla režģi un sieti', 'celt-buvm-met-rezgi'),
        ('Kalti izstrādājumi', 'celt-buvm-met-kalti'),
        ('Metāla atlikumi un lūžņi', 'celt-buvm-met-atkritumi'),
        ('Citi metāli', 'celt-buvm-met-citi'),
    ],
}

total = 0
for (name, slug, icon), items in subcats.items():
    sub, _ = Category.objects.get_or_create(
        slug=slug, defaults={'name': name, 'icon': icon, 'parent': parent}
    )
    print(f'+ {parent.name} > {name}')
    for item_name, item_slug in items:
        _, created = Category.objects.get_or_create(
            slug=item_slug, defaults={'name': item_name, 'icon': 'chevron-right', 'parent': sub}
        )
        if created:
            total += 1
            print(f'    - {item_name}')

print(f'\nKopa pievienots: {total} apaksapakskategorijas.')
