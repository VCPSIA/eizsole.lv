import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platforma.settings')
django.setup()

from listings.models import Category

LV_MAP = str.maketrans({
    'ā': 'a', 'č': 'c', 'ē': 'e', 'ģ': 'g', 'ī': 'i',
    'ķ': 'k', 'ļ': 'l', 'ņ': 'n', 'š': 's', 'ū': 'u', 'ž': 'z',
    'Ā': 'a', 'Č': 'c', 'Ē': 'e', 'Ģ': 'g', 'Ī': 'i',
    'Ķ': 'k', 'Ļ': 'l', 'Ņ': 'n', 'Š': 's', 'Ū': 'u', 'Ž': 'z',
    ' ': '-', '/': '-', '.': '', '(': '', ')': '', ',': '', "'": '',
})

fixed = 0
for cat in Category.objects.all():
    clean = cat.slug.translate(LV_MAP)
    # Tīra dubultos '-'
    while '--' in clean:
        clean = clean.replace('--', '-')
    clean = clean.strip('-')[:60]

    if clean != cat.slug:
        # Ja jau eksistē tāds slug, pievieno pk
        if Category.objects.filter(slug=clean).exclude(pk=cat.pk).exists():
            clean = f"{clean}-{cat.pk}"
        print(f'  {cat.slug} -> {clean}')
        cat.slug = clean
        cat.save()
        fixed += 1

print(f'\nLaboti {fixed} slug ieraksti.')
