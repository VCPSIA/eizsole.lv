import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platforma.settings')
django.setup()

from listings.models import Category

def slug_clean(s):
    lv = str.maketrans({
        'ā':'a','č':'c','ē':'e','ģ':'g','ī':'i','ķ':'k','ļ':'l','ņ':'n','š':'s','ū':'u','ž':'z',
        'Ā':'a','Č':'c','Ē':'e','Ģ':'g','Ī':'i','Ķ':'k','Ļ':'l','Ņ':'n','Š':'s','Ū':'u','Ž':'z',
        ' ':'-', '/':'-', '(':'' , ')':'', ',':'', '.':'',
    })
    s = s.translate(lv).lower()
    while '--' in s:
        s = s.replace('--', '-')
    return s.strip('-')[:60]

structure = {
    ('Lauksaimniecība', 'lauksaimnieciba', 'flower2'): {
        ('Traktori', 'lauks2-traktori', 'tractor'): [
            'John Deere', 'New Holland', 'Case IH', 'Fendt', 'Claas',
            'Massey Ferguson', 'Deutz-Fahr', 'Valtra', 'MTZ / Belarus',
            'Citas markas',
        ],
        ('Kombainieri', 'lauks2-kombainieri', 'tractor'): [
            'Graudu kombainieri', 'Kukurūzas kombainieri',
            'Pļaujmašīnas', 'Presēšanas tehnika',
            'Šķeldotāji', 'Cita novākšanas tehnika',
        ],
        ('Augsnes apstrāde', 'lauks2-augsne', 'arrows-expand'): [
            'Arkli', 'Ecēšas', 'Frēzes', 'Kultivatori',
            'Dīķeri, ritinātāji', 'Sēklu sējmašīnas',
            'Mēslošanas izkliedētāji', 'Cita augsnes tehnika',
        ],
        ('Lauksaimniecības piekabes', 'lauks2-piekabes', 'truck'): [
            'Pašizkraušanas piekabes', 'Graudu piekabes',
            'Cisternpiekabes', 'Universālās piekabes',
            'Citas lauksaimniecības piekabes',
        ],
        ('Augu aizsardzība un mēslošana', 'lauks2-augu-aizsardziba', 'droplet'): [
            'Smidzinātāji (piekabes)', 'Smidzinātāji (pašgājēji)',
            'Minerālmēslu izkliedētāji', 'Organisko mēslu sūknēšana',
            'Cita augu aizsardzības tehnika',
        ],
        ('Lopkopība', 'lauks2-lopkopiba', 'heart'): [
            'Slaukšanas iekārtas', 'Barības sagatavošana',
            'Kūts iekārtas', 'Cūkkopības aprīkojums',
            'Putnu audzēšanas aprīkojums', 'Žogi, aizgaldi',
            'Cita lopkopības tehnika',
        ],
        ('Meža tehnika', 'lauks2-meza-tehnika', 'tree'): [
            'Mežizstrādes tehnika (harvesteri)', 'Forwarderi',
            'Zāģi un zāģēšanas tehnika', 'Šķeldotāji',
            'Malkas skaldītāji', 'Meža piekabes',
            'Cita meža tehnika',
        ],
        ('Apūdeņošana', 'lauks2-apudenošana', 'droplet'): [
            'Laistīšanas sistēmas', 'Sūkņi',
            'Caurules un šļūtenes', 'Pilienveida apūdeņošana',
        ],
        ('Siltumnīcas un dārzkopība', 'lauks2-siltumnicas', 'sun'): [
            'Siltumnīcas', 'Siltumnīcu aprīkojums',
            'Augi un stādi (vairumtirdzniecība)', 'Substrāti, augsnes',
            'Cita dārzkopības tehnika',
        ],
        ('Graudu un produktu apstrāde', 'lauks2-graudu-apstr', 'box'): [
            'Graudu žāvētāji', 'Graudu tīrītāji un šķirotāji',
            'Uzglabāšanas silosi', 'Dzirnavas, granulatori',
            'Cita pārstrādes tehnika',
        ],
        ('Lauksaimniecības piederumi', 'lauks2-piederumi', 'bag'): [
            'Rezerves daļas', 'Eļļas, smērvielas',
            'Citas rezerves daļas un piederumi',
        ],
        ('Lauksaimniecības pakalpojumi', 'lauks2-pakalpojumi', 'tools'): [
            'Lauku apstrādes pakalpojumi', 'Novākšanas pakalpojumi',
            'Tehniskā apkope un remonts', 'Citi lauksaimniecības pakalpojumi',
        ],
        ('Zeme un lauku īpašumi', 'lauks2-zeme', 'map'): [
            'Lauksaimniecības zeme — pārdod',
            'Lauksaimniecības zeme — īrē/nomā',
            'Meža zeme', 'Lauku mājas un sētas',
        ],
    },

    ('Celtniecība', 'celtnieciba', 'building'): {
        ('Būvmateriāli', 'celt-buvmateriali', 'bricks'): [
            'Ķieģeļi, bloki', 'Betona izstrādājumi',
            'Akmens, granīts, šķembas', 'Smiltis, grants, māls',
            'Ģipškartons un plāksnes', 'Citi būvmateriāli',
        ],
        ('Jumti un fasādes', 'celt-jumti', 'house'): [
            'Dakstiņi (keramikas, betona)', 'Metāla jumta segums',
            'Ondulīns, bitumena šindeles', 'Saplacināti jumti (membr.)',
            'Fasādes apdare', 'Fasādes paneļi un siltumjosta',
            'Drenāžas sistēmas (notekas)', 'Citi jumta materiāli',
        ],
        ('Logi un durvis', 'celt-logi-durvis', 'window'): [
            'PVC logi', 'Koka logi', 'Alumīnija logi',
            'Ārdurvis (metāla)', 'Ārdurvis (koka)',
            'Iekšdurvis', 'Garāžas vārti', 'Slīdvārti, šūpolvārti',
            'Jumta logi (mansarda)', 'Citi logi un durvis',
        ],
        ('Siltumizolācija un hidroizolācija', 'celt-siltumiz', 'layers'): [
            'Akmens vate, stikla vate', 'Putuplasts (EPS, XPS)',
            'Pūstā izolācija (PUR)', 'Hidroizolācijas membrānas',
            'Tvaika barjeras', 'Cita izolācija',
        ],
        ('Betona darbi un mūrēšana', 'celt-betons', 'bricks'): [
            'Cementi, kaļķi', 'Betona maisītāji',
            'Ģipsis, špakteļmasas', 'Mūrēšanas maisījumi',
            'Veidnes, kofraži', 'Betona sūkņi',
            'Armēšanas tērauds, sieti', 'Citi betona materiāli',
        ],
        ('Koka konstrukcijas', 'celt-koks', 'tree'): [
            'Zāģmateriāli (dēļi, baļķi)', 'Lamēlkoks (LVL, CLT)',
            'Finiera plāksnes, OSB', 'Karkasa māju elementi',
            'Kāpnes', 'Terases dēļi', 'Citi koka materiāli',
        ],
        ('Grīdas un sienas apdare', 'celt-gridas', 'grid'): [
            'Flīzes (grīdas, sienas)', 'Lamināts', 'Parkets',
            'Vinila grīdsega (LVT/SPC)', 'Paklāji',
            'Tapetes', 'Sienu paneļi', 'Krāsas un laki',
            'Dekoratīvie apmetumi', 'Cita apdare',
        ],
        ('Santehnika', 'celt-santehnika', 'droplet'): [
            'Caurules un fitting', 'Radiatoru sistēmas',
            'Ūdens sildītāji (boileri)', 'Dušas kabīnes, vannas',
            'Tualetes podi, izlietnes', 'Jaucējkrāni',
            'Kanalizācija', 'Cita santehnika',
        ],
        ('Apkure un ventilācija', 'celt-apkure', 'thermometer'): [
            'Katli (gāzes, malkas, granulu)', 'Siltumsūkņi',
            'Grīdas apkure', 'Radiatoru sistēmas',
            'Rekuperācija un ventilācija', 'Kamīni un krāsnis',
            'Gaisa kondicionieri', 'Cita apkures tehnika',
        ],
        ('Elektromateriāli', 'celt-elektrika', 'lightning'): [
            'Kabeļi un vadi', 'Rozetes, slēdži',
            'Sadales skapji', 'Apgaismojums (ārpus tehnikas)',
            'Saules paneļi', 'Akumulatori, ģeneratori',
            'Citi elektromateriāli',
        ],
        ('Celtniecības tehnika un instrumenti', 'celt-tehnika', 'tools'): [
            'Ekskavatori', 'Buldozeri, skrēperi',
            'Celtņi, manipulatori', 'Betona jaucēji',
            'Sastatnes un torņi', 'Kompresor, pneimatika',
            'Elektriskie instrumenti', 'Rokasdarbarīki',
            'Mērierīces (lāzeri, nivieteri)', 'Teleskopiskās iekrāvēji',
            'Cita celtniecības tehnika',
        ],
        ('Atkritumi un demontāža', 'celt-atkritumi', 'trash'): [
            'Demontāžas pakalpojumi', 'Gružu izvešana',
            'Otrreizējie būvmateriāli', 'Citi atkritumu pakalpojumi',
        ],
        ('Celtniecības pakalpojumi', 'celt-pakalpojumi', 'hammer'): [
            'Projektēšana, arhitekti', 'Mūrēšana, betonēšana',
            'Jumta darbi', 'Fasādes darbi',
            'Logi un durvis (uzstādīšana)', 'Grīdas un sienas apdare',
            'Santehnikas montāža', 'Elektrisko darbu montāža',
            'Apkures montāža', 'Celtniecības vadība',
            'Citi celtniecības pakalpojumi',
        ],
    },
}

total_main = total_sub = total_subsub = 0

for (main_name, main_slug, main_icon), subcats in structure.items():
    main, created = Category.objects.get_or_create(
        slug=main_slug,
        defaults={'name': main_name, 'icon': main_icon, 'parent': None}
    )
    if created:
        total_main += 1
        print(f'+ {main_name}')

    for (sub_name, sub_slug, sub_icon), items in subcats.items():
        sub, created = Category.objects.get_or_create(
            slug=sub_slug,
            defaults={'name': sub_name, 'icon': sub_icon, 'parent': main}
        )
        if created:
            total_sub += 1

        for item_name in items:
            item_slug = sub_slug + '-' + slug_clean(item_name)
            item_slug = item_slug[:60]
            if Category.objects.filter(slug=item_slug).exists():
                item_slug = item_slug[:55] + f'-{hash(item_name) % 999}'
            _, created = Category.objects.get_or_create(
                slug=item_slug,
                defaults={'name': item_name, 'icon': 'chevron-right', 'parent': sub}
            )
            if created:
                total_subsub += 1

print(f'\nGalvenās kategorijas: {total_main}')
print(f'Apakškategorijas:     {total_sub}')
print(f'Apakšapakš:           {total_subsub}')
print(f'Kopā pievienots:      {total_main + total_sub + total_subsub}')
