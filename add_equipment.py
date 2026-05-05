import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platforma.settings')
django.setup()

from listings.models import Equipment

items = [
    # Komforts
    ('Gaisa kondicionieris', 'comfort', 'thermometer-half', 1),
    ('Klimata kontrole', 'comfort', 'thermometer', 2),
    ('Ādas salons', 'comfort', 'star', 3),
    ('Apkurināmi priekšējie sēdekļi', 'comfort', 'fire', 4),
    ('Apkurināmi aizmugurējie sēdekļi', 'comfort', 'fire', 5),
    ('Elektriski regulējami sēdekļi', 'comfort', 'sliders', 6),
    ('Masāžas sēdekļi', 'comfort', 'person', 7),
    ('Elektriskie logi', 'comfort', 'layout-wtf', 8),
    ('Elektriski regulējami spoguļi', 'comfort', 'symmetry-horizontal', 9),
    ('Apkurināmi spoguļi', 'comfort', 'fire', 10),
    ('Panorāmas jumts', 'comfort', 'sun', 11),
    ('Atvērams jumts (kabrio)', 'comfort', 'sun', 12),
    ('Stūres apkure', 'comfort', 'fire', 13),
    ('Regulējams stūres rats', 'comfort', 'circle', 14),
    ('Atmiņas sēdekļi', 'comfort', 'bookmark', 15),
    ('Trokšņa izolācija (akustiskais stikls)', 'comfort', 'volume-mute', 16),

    # Drošība
    ('ABS (pretbloķēšanas bremzes)', 'safety', 'shield-check', 1),
    ('ESP (stabilitātes kontrole)', 'safety', 'shield-check', 2),
    ('Gaisa spilveni priekšā', 'safety', 'shield', 3),
    ('Sānu gaisa spilveni', 'safety', 'shield', 4),
    ('Aizmugurējie gaisa spilveni', 'safety', 'shield', 5),
    ('Priekšpusē gājēju aizsardzība', 'safety', 'person', 6),
    ('Kruīza kontrole', 'safety', 'speedometer2', 7),
    ('Adaptīvais kruīza kontrole (ACC)', 'safety', 'speedometer2', 8),
    ('Joslu maiņas brīdinājums', 'safety', 'arrows-expand', 9),
    ('Joslu noturēšanas palīgs', 'safety', 'arrows-expand', 10),
    ('Aklā punkta uzraudzība', 'safety', 'eye', 11),
    ('Avārijas bremzēšanas sistēma', 'safety', 'shield-exclamation', 12),
    ('Riepu spiediena kontrole', 'safety', 'circle', 13),
    ('Ieejas brīdināšanas sistēma', 'safety', 'bell', 14),
    ('Imobilaizers', 'safety', 'lock', 15),
    ('Signalizācija', 'safety', 'alarm', 16),
    ('Centrālā slēdzene', 'safety', 'lock', 17),
    ('Bērnu drošības slēdzenes', 'safety', 'shield', 18),

    # Mediji un navigācija
    ('GPS navigācija (iebūvēta)', 'media', 'geo-alt', 1),
    ('Android Auto / Apple CarPlay', 'media', 'phone', 2),
    ('Bluetooth', 'media', 'bluetooth', 3),
    ('Multivides ekrāns (touch)', 'media', 'display', 4),
    ('USB / AUX savienojums', 'media', 'usb-symbol', 5),
    ('Bezvadu uzlāde', 'media', 'lightning-charge', 6),
    ('Wi-Fi hotspot', 'media', 'wifi', 7),
    ('Premium audio sistēma', 'media', 'speaker', 8),
    ('Digitālā radio (DAB)', 'media', 'broadcast', 9),
    ('Head-Up displejs (HUD)', 'media', 'window', 10),
    ('Atpakaļskata kamera', 'media', 'camera-video', 11),
    ('360° kameras sistēma', 'media', 'camera', 12),

    # Tehnika
    ('Automātiskā ātrumkārba', 'tech', 'gear', 1),
    ('Robots (robotizēta ātrumkārba)', 'tech', 'gear', 2),
    ('Bezpakāpju variators (CVT)', 'tech', 'gear', 3),
    ('Pilnpiedziņa 4x4 (pastāvīga)', 'tech', 'truck', 4),
    ('Pilnpiedziņa 4x4 (atslēdzama)', 'tech', 'truck', 5),
    ('Elektriskā stūres pastiprinātājs', 'tech', 'circle', 6),
    ('Pneimatiskā piekare', 'tech', 'arrows-vertical', 7),
    ('Adaptīvā piekare', 'tech', 'arrows-vertical', 8),
    ('Start/Stop sistēma', 'tech', 'toggle-on', 9),
    ('Hibrīds (MHEV/HEV)', 'tech', 'lightning-charge', 10),
    ('Plug-in hibrīds (PHEV)', 'tech', 'plug', 11),
    ('Elektriskais (BEV)', 'tech', 'ev-station', 12),
    ('Parkošanās sensors (priekšā)', 'tech', 'radar', 13),
    ('Parkošanās sensors (aizmugurē)', 'tech', 'radar', 14),
    ('Automātiskā stāvēšana (Park Assist)', 'tech', 'p-circle', 15),
    ('Elektriskie bremžu suporti', 'tech', 'circle', 16),

    # Papildus
    ('Sakabes āķis', 'extra', 'link', 1),
    ('Jumta bagāžnieks / sliedes', 'extra', 'box', 2),
    ('Sniega ķēžu komplekts', 'extra', 'snow', 3),
    ('Rezerves ritenis (pilna izmēra)', 'extra', 'circle', 4),
    ('Rezerves ritenis (neparastais)', 'extra', 'circle', 5),
    ('Pirmās palīdzības komplekts', 'extra', 'heart-pulse', 6),
    ('Ugunsdzēšamais aparāts', 'extra', 'fire', 7),
    ('Tumsas braukšanas palīgs', 'extra', 'moon', 8),
    ('Automātiskās gaismas', 'extra', 'lightbulb', 9),
    ('LED lukturi', 'extra', 'lightbulb', 10),
    ('Ksenona lukturi', 'extra', 'lightbulb', 11),
    ('Miglas lukturi', 'extra', 'cloud-fog', 12),
    ('Adaptīvie lukturi', 'extra', 'lightbulb', 13),
    ('Dūmu vai putekļu filtrs (salonā)', 'extra', 'wind', 14),
    ('Ziemas riepas komplektā', 'extra', 'snow', 15),
    ('Vasaras riepas komplektā', 'extra', 'sun', 16),
]

created = 0
for name, group, icon, order in items:
    obj, was_created = Equipment.objects.get_or_create(
        name=name,
        defaults={'group': group, 'icon': icon, 'order': order}
    )
    if was_created:
        created += 1

print(f'Izveidoti {created} aprīkojuma ieraksti. Kopā: {Equipment.objects.count()}')
