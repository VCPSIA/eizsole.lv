import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platforma.settings')
django.setup()

from listings.models import Category

data = {
    'auto-automasinas': [
        ('Audi', 'am-audi', 'car-front'),
        ('BMW', 'am-bmw', 'car-front'),
        ('Chevrolet', 'am-chevrolet', 'car-front'),
        ('Chrysler / Dodge', 'am-chrysler', 'car-front'),
        ('Citroen', 'am-citroen', 'car-front'),
        ('Dacia', 'am-dacia', 'car-front'),
        ('Fiat', 'am-fiat', 'car-front'),
        ('Ford', 'am-ford', 'car-front'),
        ('Honda', 'am-honda', 'car-front'),
        ('Hyundai', 'am-hyundai', 'car-front'),
        ('Jaguar', 'am-jaguar', 'car-front'),
        ('Jeep', 'am-jeep', 'car-front'),
        ('Kia', 'am-kia', 'car-front'),
        ('Land Rover', 'am-landrover', 'car-front'),
        ('Lexus', 'am-lexus', 'car-front'),
        ('Mazda', 'am-mazda', 'car-front'),
        ('Mercedes-Benz', 'am-mercedes', 'car-front'),
        ('Mitsubishi', 'am-mitsubishi', 'car-front'),
        ('Nissan', 'am-nissan', 'car-front'),
        ('Opel', 'am-opel', 'car-front'),
        ('Peugeot', 'am-peugeot', 'car-front'),
        ('Porsche', 'am-porsche', 'car-front'),
        ('Renault', 'am-renault', 'car-front'),
        ('Seat', 'am-seat', 'car-front'),
        ('Skoda', 'am-skoda', 'car-front'),
        ('Subaru', 'am-subaru', 'car-front'),
        ('Suzuki', 'am-suzuki', 'car-front'),
        ('Tesla', 'am-tesla', 'lightning-charge'),
        ('Toyota', 'am-toyota', 'car-front'),
        ('Volkswagen', 'am-volkswagen', 'car-front'),
        ('Volvo', 'am-volvo', 'car-front'),
        ('Citas markas', 'am-citas', 'car-front'),
    ],
    'auto-motocikli': [
        ('BMW Motorrad', 'moto-bmw', 'bicycle'),
        ('Ducati', 'moto-ducati', 'bicycle'),
        ('Harley-Davidson', 'moto-harley', 'bicycle'),
        ('Honda', 'moto-honda', 'bicycle'),
        ('Kawasaki', 'moto-kawasaki', 'bicycle'),
        ('KTM', 'moto-ktm', 'bicycle'),
        ('Suzuki', 'moto-suzuki', 'bicycle'),
        ('Triumph', 'moto-triumph', 'bicycle'),
        ('Yamaha', 'moto-yamaha', 'bicycle'),
        ('Motorolleri', 'moto-motorolleri', 'scooter'),
        ('Kvadracikli (ATV)', 'moto-atv', 'bicycle'),
        ('Citas markas', 'moto-citas', 'bicycle'),
    ],
    'auto-kravas': [
        ('Kravas auto lidz 3.5t', 'kravas-lidz35', 'truck'),
        ('Kravas auto virs 3.5t', 'kravas-virs35', 'truck'),
        ('Mikroautobusi (8+ vietas)', 'kravas-mikroautobusi', 'bus-front'),
        ('Autobusi', 'kravas-autobusi', 'bus-front'),
        ('Piekabes', 'kravas-piekabes', 'truck'),
        ('Puspiekabes', 'kravas-puspiekabes', 'truck'),
        ('Autocisternas', 'kravas-cisternas', 'truck'),
        ('Speciala tehnika', 'kravas-spectehn', 'gear'),
    ],
    'auto-lauksaimnieciba': [
        ('Traktori', 'lauks-traktori', 'tractor'),
        ('Kombaini', 'lauks-kombaini', 'tractor'),
        ('Lauksaimniecibas piekabes', 'lauks-piekabes', 'tractor'),
        ('Rikosi un agregati', 'lauks-rikosi', 'gear'),
        ('Mietsaimniecibas tehnika', 'lauks-miets', 'tree'),
        ('Cita lauksaimniecibas tehnika', 'lauks-cita', 'tractor'),
    ],
    'auto-udens': [
        ('Motorlaivas', 'udens-motorlaivas', 'water'),
        ('Jahtas, buru laivas', 'udens-jahtas', 'water'),
        ('Gumijas laivas', 'udens-gumijas', 'water'),
        ('Laivmotori', 'udens-laivmotori', 'water'),
        ('Udens motocikli (PWC)', 'udens-pwc', 'water'),
        ('Kanoe, kajaki', 'udens-kanoe', 'water'),
        ('Piederumi un rezerves dalas', 'udens-piederumi', 'gear'),
    ],
    'auto-rezerves-dalas': [
        ('Dzinejs, transmisija', 'rd-dzinejs', 'gear'),
        ('Virsbuve, ramas', 'rd-virsbuve', 'car-front'),
        ('Elektronikas dalas', 'rd-elektronika', 'cpu'),
        ('Bremzes, piekare', 'rd-bremzes', 'circle'),
        ('Dzesanas, kondicionesanas sistemas', 'rd-dzesana', 'thermometer'),
        ('Degvielas sistema', 'rd-degviela', 'droplet'),
        ('Izpudu sistema', 'rd-izpuds', 'gear'),
        ('Citas rezerves dalas', 'rd-citas', 'box'),
    ],
    'auto-riepas': [
        ('Vasaras riepas', 'riepas-vasara', 'circle'),
        ('Ziemas riepas', 'riepas-ziema', 'snow'),
        ('Visa gada riepas', 'riepas-visagada', 'circle'),
        ('Riepas ar diskiem', 'riepas-ar-diskiem', 'circle'),
        ('Tela diski', 'riepas-tela-diski', 'circle'),
        ('Aluminja diski', 'riepas-al-diski', 'circle'),
        ('Motociklu riepas', 'riepas-moto', 'bicycle'),
        ('Kravas auto riepas', 'riepas-kravas', 'truck'),
    ],
    'auto-piederumi': [
        ('Audio, video tehnika', 'pip-audio', 'speaker'),
        ('GPS navigacija', 'pip-gps', 'geo-alt'),
        ('Drosibas sistemas, signalizacija', 'pip-drosiba', 'shield'),
        ('Autokemeriji, lielie konteineri', 'pip-kempings', 'house'),
        ('Bugsesanas apriko', 'pip-bugse', 'link'),
        ('Tutnings, spoileri', 'pip-tunings', 'lightning'),
        ('Degvielas kannas, rezerves', 'pip-degviela', 'droplet'),
        ('Citi auto piederumi', 'pip-citi', 'bag'),
    ],
    'auto-serviss': [
        ('Tehniska apkope, elja maina', 'serv-apkope', 'wrench'),
        ('Virsbuve, lakosana', 'serv-virsbuve', 'brush'),
        ('Elektronikas diagnostika', 'serv-elektr', 'cpu'),
        ('Riepu montaza, balansesan', 'serv-riepas', 'circle'),
        ('Stiklu nomaina', 'serv-stikli', 'window'),
        ('Auto mazgasana, kimiskais', 'serv-mazgasana', 'droplet'),
        ('Auto kratuve (apzimogosana)', 'serv-kratuve', 'house'),
        ('Cits auto serviss', 'serv-cits', 'tools'),
    ],
    'auto-noma': [
        ('Vieglas automasinas', 'noma-vieglas', 'car-front'),
        ('Apvidus automasinas (SUV)', 'noma-suv', 'car-front'),
        ('Kravas auto noma', 'noma-kravas', 'truck'),
        ('Mikroautobusi noma', 'noma-mikrobus', 'bus-front'),
        ('Motociklu noma', 'noma-moto', 'bicycle'),
        ('Lauksaimn. tehnikas noma', 'noma-lauksaimn', 'tractor'),
    ],
}

total = 0
for parent_slug, children in data.items():
    try:
        parent = Category.objects.get(slug=parent_slug)
    except Category.DoesNotExist:
        print(f'KLUDDA: "{parent_slug}" nav atrasta!')
        continue

    for name, slug, icon in children:
        obj, created = Category.objects.get_or_create(
            slug=slug,
            defaults={'name': name, 'icon': icon, 'parent': parent}
        )
        if created:
            total += 1
            print(f'  + {parent.name} / {name}')

print(f'\nKopa izveidotas {total} apakskategorijas.')
