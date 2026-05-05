import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platforma.settings')
django.setup()

from listings.models import Category

subcategories = {
    'auto': [
        ('Automašīnas', 'auto-automasinas', 'car-front'),
        ('Motocikli, motorolleri', 'auto-motocikli', 'bicycle'),
        ('Kravas auto, autobusi', 'auto-kravas', 'truck'),
        ('Lauksaimniecības tehnika', 'auto-lauksaimnieciba', 'tractor'),
        ('Ūdens transports', 'auto-udens', 'water'),
        ('Rezerves daļas', 'auto-rezerves-dalas', 'gear'),
        ('Riepas, diski', 'auto-riepas', 'circle'),
        ('Auto piederumi', 'auto-piederumi', 'bag'),
        ('Auto serviss', 'auto-serviss', 'tools'),
        ('Nomā', 'auto-noma', 'key'),
    ],
    'nekustamais-ipasums': [
        ('Dzīvokļi - pārdod', 'ni-dzivokli-pardod', 'house-door'),
        ('Dzīvokļi - īrē', 'ni-dzivokli-ire', 'house'),
        ('Mājas - pārdod', 'ni-majas-pardod', 'house-heart'),
        ('Mājas - īrē', 'ni-majas-ire', 'house-check'),
        ('Vasarnīcas, dārziņi', 'ni-vasarnicas', 'tree'),
        ('Zeme', 'ni-zeme', 'map'),
        ('Telpas biznesam', 'ni-bizness', 'building'),
        ('Noliktavas, ražotnes', 'ni-noliktavas', 'boxes'),
        ('Garāžas, stāvvietas', 'ni-garazas', 'car-garage'),
        ('Ārzemēs', 'ni-arzemes', 'globe'),
    ],
    'tehnika': [
        ('Datori, planšetes', 'tehnika-datori', 'laptop'),
        ('Telefoni', 'tehnika-telefoni', 'phone'),
        ('TV, audio, video', 'tehnika-tv', 'tv'),
        ('Sadzīves tehnika', 'tehnika-sadzive', 'plug'),
        ('Foto, optika', 'tehnika-foto', 'camera'),
        ('Spēļu konsoles', 'tehnika-speles', 'controller'),
        ('Biroja tehnika', 'tehnika-birojs', 'printer'),
        ('Tīkla iekārtas', 'tehnika-tikls', 'router'),
        ('Rezerves daļas', 'tehnika-dalas', 'cpu'),
        ('Programmatūra', 'tehnika-software', 'code-slash'),
    ],
    'sadzives-preces': [
        ('Mēbeles', 'sp-mebeles', 'columns-gap'),
        ('Virtuves preces', 'sp-virtuve', 'cup-hot'),
        ('Apgaismojums', 'sp-apgaismojums', 'lightbulb'),
        ('Mājas tekstils', 'sp-tekstils', 'border-all'),
        ('Vannas istaba', 'sp-vanna', 'droplet'),
        ('Dekorācijas', 'sp-dekoracijas', 'stars'),
        ('Remonta materiāli', 'sp-remonts', 'hammer'),
        ('Instrumenti', 'sp-instrumenti', 'tools'),
        ('Trauki, servīzes', 'sp-trauki', 'cup'),
        ('Citas preces mājai', 'sp-citas', 'house-gear'),
    ],
    'apgerbs': [
        ('Sieviešu apģērbs', 'apg-sieviesu', 'gender-female'),
        ('Vīriešu apģērbs', 'apg-virieSU', 'gender-male'),
        ('Bērnu apģērbs', 'apg-bernu', 'emoji-smile'),
        ('Apavi - sieviešu', 'apg-apavi-s', 'boot'),
        ('Apavi - vīriešu', 'apg-apavi-v', 'boot'),
        ('Apavi - bērnu', 'apg-apavi-b', 'boot'),
        ('Somas, mugursomas', 'apg-somas', 'bag'),
        ('Rotaslietas, pulksteņi', 'apg-rotaslietas', 'gem'),
        ('Sporta apģērbs', 'apg-sports', 'bicycle'),
        ('Cepures, šalles', 'apg-aksesuari', 'palette'),
    ],
    'sports': [
        ('Velosipēdi', 'sp-velosipedi', 'bicycle'),
        ('Ziemas sports', 'sp-ziema', 'snow'),
        ('Ūdens sports', 'sp-udens-sports', 'water'),
        ('Fitnesa inventārs', 'sp-fitness', 'heart-pulse'),
        ('Medības', 'sp-medibas', 'crosshair'),
        ('Makšķerēšana', 'sp-makskere', 'water'),
        ('Tūrisms, kempings', 'sp-turisMs', 'compass'),
        ('Futbols, bumbu spēles', 'sp-futbols', 'dribbble'),
        ('Teniss, badmintons', 'sp-teniss', 'circle'),
        ('Cits sports', 'sp-cits', 'trophy'),
    ],
    'darzniecia': [
        ('Dārza instrumenti', 'darz-instrumenti', 'scissors'),
        ('Augi, stādi, sēklas', 'darz-augi', 'flower1'),
        ('Dārza mēbeles', 'darz-mebeles', 'columns-gap'),
        ('Siltumnīcas', 'darz-siltumnicas', 'sun'),
        ('Laistīšanas sistēmas', 'darz-laistisana', 'droplet'),
        ('Dārza mājiņas', 'darz-majinas', 'house'),
        ('Mēslojums, augu kopšana', 'darz-meslojums', 'bag'),
        ('Dārza tehnika', 'darz-tehnika', 'gear'),
    ],
    'berniem': [
        ('Rotaļlietas', 'bern-rotallietas', 'emoji-laughing'),
        ('Ratiņi, autokrēsli', 'bern-ratini', 'person-walking'),
        ('Bērnu mēbeles', 'bern-mebeles', 'columns-gap'),
        ('Bērnu apģērbs (0-2 g.)', 'bern-apg-mazuli', 'heart'),
        ('Bērnu apģērbs (3-7 g.)', 'bern-apg-mazie', 'emoji-smile'),
        ('Bērnu apģērbs (8+ g.)', 'bern-apg-lielaki', 'person'),
        ('Skolas piederumi', 'bern-skola', 'pencil'),
        ('Grāmatas, mūzika', 'bern-gramatas', 'book'),
        ('Sporta preces bērniem', 'bern-sports', 'bicycle'),
        ('Barošana, aprūpe', 'bern-aprupe', 'droplet'),
    ],
    'dzivnieki': [
        ('Suņi', 'dz-suni', 'heart'),
        ('Kaķi', 'dz-kaki', 'heart'),
        ('Putni', 'dz-putni', 'twitter'),
        ('Zivis, akvāriji', 'dz-zivis', 'water'),
        ('Grauzēji, truši', 'dz-grauzegi', 'emoji-smile'),
        ('Rāpuļi, eksotiskie', 'dz-rapuli', 'bug'),
        ('Barība', 'dz-bariba', 'bag'),
        ('Piederumi, aksesuāri', 'dz-piederumi', 'box'),
        ('Veterinārija', 'dz-veterinarija', 'plus-circle'),
        ('Zoopreču veikali', 'dz-veikali', 'shop'),
    ],
    'darbs': [
        ('Pilna laika darbs', 'darbs-pilns', 'briefcase'),
        ('Nepilna laika darbs', 'darbs-nepilns', 'clock'),
        ('Darbs ārzemēs', 'darbs-arzemes', 'globe'),
        ('Meklē darbu', 'darbs-mekle', 'person'),
        ('Freelance, attālinātais', 'darbs-freelance', 'laptop'),
        ('Prakses vietas', 'darbs-prakse', 'mortarboard'),
        ('Uzņēmējdarbība', 'darbs-uznemejdarbiba', 'graph-up'),
        ('Kursi, apmācība', 'darbs-apmaciba', 'book'),
    ],
    'pakalpojumi': [
        ('Remontdarbi, būvniecība', 'pak-remonts', 'hammer'),
        ('Santehnika, elektrika', 'pak-santehnika', 'wrench'),
        ('Tīrīšana', 'pak-tirisana', 'stars'),
        ('Pārvākšanās', 'pak-parvaksanas', 'truck'),
        ('IT pakalpojumi', 'pak-it', 'code-slash'),
        ('Apmācība, tulkošana', 'pak-apmaciba', 'book'),
        ('Skaistums, veselība', 'pak-skaistums', 'heart-pulse'),
        ('Foto, video, dizains', 'pak-foto', 'camera'),
        ('Juridiskā palīdzība', 'pak-juridiska', 'file-text'),
        ('Pārējie pakalpojumi', 'pak-parejo', 'three-dots'),
    ],
    'kolekcionesana': [
        ('Monētas, naudaszīmes', 'kol-monetas', 'coin'),
        ('Pastmarkas, filokartija', 'kol-pastmarkas', 'envelope'),
        ('Antīkās lietas', 'kol-antika', 'clock-history'),
        ('Māksla, gleznas', 'kol-maksla', 'palette'),
        ('Grāmatas, žurnāli', 'kol-gramatas', 'book'),
        ('Mūzika, vinils', 'kol-muzika', 'music-note'),
        ('Filmas, DVD', 'kol-filmas', 'film'),
        ('Sporta suvenīri', 'kol-sporta', 'trophy'),
        ('Rotaļlietas, figūriņas', 'kol-figurinas', 'stars'),
        ('Militārā vēsture', 'kol-militara', 'shield'),
    ],
}

created_count = 0
for parent_slug, children in subcategories.items():
    try:
        parent = Category.objects.get(slug=parent_slug)
    except Category.DoesNotExist:
        print(f'KĻŪDA: Vecākkategorija "{parent_slug}" nav atrasta!')
        continue

    for name, slug, icon in children:
        obj, created = Category.objects.get_or_create(
            slug=slug,
            defaults={'name': name, 'icon': icon, 'parent': parent}
        )
        if created:
            created_count += 1
            print(f'  + {parent.name} - {name}')

print(f'\nKopā izveidotas {created_count} apakškategorijas.')
