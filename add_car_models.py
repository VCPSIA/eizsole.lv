import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platforma.settings')
django.setup()

from listings.models import Category

models_by_brand = {
    'am-audi': [
        'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8',
        'Q2', 'Q3', 'Q4 e-tron', 'Q5', 'Q7', 'Q8',
        'TT', 'R8', 'e-tron', 'RS sērija', 'S sērija', 'Citi modeļi',
    ],
    'am-bmw': [
        '1. sērija', '2. sērija', '3. sērija', '4. sērija', '5. sērija',
        '6. sērija', '7. sērija', '8. sērija',
        'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7',
        'Z3', 'Z4', 'M sērija', 'i sērija (i3, i4, iX)', 'Citi modeļi',
    ],
    'am-chevrolet': [
        'Aveo', 'Captiva', 'Cruze', 'Epica', 'Equinox', 'Lacetti',
        'Malibu', 'Niva', 'Orlando', 'Spark', 'Suburban', 'Tahoe',
        'Trax', 'Citi modeļi',
    ],
    'am-chrysler': [
        'Chrysler 300C', 'Chrysler PT Cruiser', 'Chrysler Sebring',
        'Chrysler Voyager', 'Dodge Charger', 'Dodge Challenger',
        'Dodge Durango', 'Dodge Journey', 'Dodge RAM', 'Citi modeļi',
    ],
    'am-citroen': [
        'Berlingo', 'C1', 'C2', 'C3', 'C3 Aircross', 'C4', 'C4 Cactus',
        'C5', 'C5 Aircross', 'C6', 'C8', 'DS3', 'DS4', 'DS5',
        'Jumper', 'Jumpy', 'Picasso / Grand Picasso', 'Saxo',
        'Xsara', 'Xsara Picasso', 'Citi modeļi',
    ],
    'am-dacia': [
        'Duster', 'Jogger', 'Logan', 'Lodgy', 'Sandero',
        'Dokker', 'Spring', 'Citi modeļi',
    ],
    'am-fiat': [
        '500', '500X', 'Barchetta', 'Brava / Bravo', 'Doblo',
        'Grande Punto', 'Idea', 'Multipla', 'Panda', 'Punto',
        'Sedici', 'Stilo', 'Tipo', 'Ulysse', 'Citi modeļi',
    ],
    'am-ford': [
        'B-Max', 'C-Max', 'EcoSport', 'Edge', 'Escort', 'Explorer',
        'Fiesta', 'Focus', 'Galaxy', 'Ka', 'Kuga', 'Mondeo',
        'Mustang', 'Puma', 'Ranger', 'S-Max', 'Transit',
        'Transit Connect', 'Citi modeļi',
    ],
    'am-honda': [
        'Accord', 'Civic', 'CR-V', 'CR-Z', 'FR-V', 'HR-V',
        'Jazz', 'Legend', 'NSX', 'Pilot', 'Stream',
        'e (elektro)', 'Citi modeļi',
    ],
    'am-hyundai': [
        'Accent', 'Coupe', 'Elantra', 'Getz', 'i10', 'i20',
        'i30', 'i40', 'IONIQ', 'ix20', 'ix35', 'Kona',
        'Santa Fe', 'Sonata', 'Terracan', 'Tucson', 'Citi modeļi',
    ],
    'am-jaguar': [
        'E-Pace', 'E-Type', 'F-Pace', 'F-Type', 'I-Pace',
        'S-Type', 'X-Type', 'XE', 'XF', 'XJ', 'XK', 'Citi modeļi',
    ],
    'am-jeep': [
        'Cherokee', 'Commander', 'Compass', 'Grand Cherokee',
        'Patriot', 'Renegade', 'Wrangler', 'Citi modeļi',
    ],
    'am-kia': [
        'Carens', 'Carnival', 'Ceed', 'Cerato', 'EV6',
        'Magentis', 'Niro', 'Optima', 'Picanto', 'Rio',
        'Sorento', 'Soul', 'Sportage', 'Stinger',
        'Stonic', 'Citi modeļi',
    ],
    'am-landrover': [
        'Defender', 'Discovery', 'Discovery Sport',
        'Freelander', 'Range Rover', 'Range Rover Evoque',
        'Range Rover Sport', 'Range Rover Velar', 'Citi modeļi',
    ],
    'am-lexus': [
        'CT', 'ES', 'GS', 'GX', 'IS', 'LC', 'LS',
        'LX', 'NX', 'RC', 'RX', 'UX', 'Citi modeļi',
    ],
    'am-mazda': [
        'Mazda2', 'Mazda3', 'Mazda5', 'Mazda6',
        'CX-3', 'CX-30', 'CX-5', 'CX-7', 'CX-9',
        'MX-5', 'MX-30', 'RX-8', 'Tribute', 'Citi modeļi',
    ],
    'am-mercedes': [
        'A klase', 'B klase', 'C klase', 'CLA', 'CLS',
        'E klase', 'EQC', 'G klase', 'GL / GLS',
        'GLA', 'GLB', 'GLC', 'GLE', 'GLK',
        'ML', 'S klase', 'SL', 'SLK / SLC',
        'Sprinter', 'V klase / Viano', 'Vito', 'Citi modeļi',
    ],
    'am-mitsubishi': [
        'ASX', 'Carisma', 'Colt', 'Eclipse', 'Eclipse Cross',
        'Galant', 'Grandis', 'L200', 'Lancer', 'Outlander',
        'Pajero', 'Space Star', 'Citi modeļi',
    ],
    'am-nissan': [
        '350Z / 370Z', 'Almera', 'Juke', 'Leaf',
        'Micra', 'Murano', 'Navara', 'Note', 'Pathfinder',
        'Patrol', 'Primera', 'Pulsar', 'Qashqai',
        'Teana', 'Tiida', 'X-Trail', 'Citi modeļi',
    ],
    'am-opel': [
        'Adam', 'Agila', 'Antara', 'Astra', 'Combo',
        'Corsa', 'Crossland', 'Frontera', 'Grandland',
        'Insignia', 'Meriva', 'Mokka', 'Movano',
        'Omega', 'Signum', 'Vectra', 'Vivaro',
        'Zafira', 'Citi modeļi',
    ],
    'am-peugeot': [
        '106', '107', '206', '207', '208',
        '306', '307', '308', '407', '408', '508',
        '2008', '3008', '4008', '5008',
        'Bipper', 'Boxer', 'Expert', 'Partner', 'RCZ', 'Citi modeļi',
    ],
    'am-porsche': [
        '911', 'Boxster', 'Cayenne', 'Cayman',
        'Macan', 'Panamera', 'Taycan', 'Citi modeļi',
    ],
    'am-renault': [
        'Captur', 'Clio', 'Duster', 'Espace', 'Fluence',
        'Grand Scenic', 'Kadjar', 'Kangoo', 'Koleos',
        'Laguna', 'Master', 'Megane', 'Modus', 'Scenic',
        'Symbol', 'Trafic', 'Twingo', 'Zoe', 'Citi modeļi',
    ],
    'am-seat': [
        'Alhambra', 'Altea', 'Arona', 'Ateca',
        'Cordoba', 'Exeo', 'Ibiza', 'Leon',
        'Mii', 'Tarraco', 'Toledo', 'Citi modeļi',
    ],
    'am-skoda': [
        'Citigo', 'Enyaq', 'Fabia', 'Kamiq',
        'Karoq', 'Kodiaq', 'Octavia', 'Rapid',
        'Roomster', 'Scala', 'Superb', 'Yeti', 'Citi modeļi',
    ],
    'am-subaru': [
        'BRZ', 'Forester', 'Impreza', 'Legacy',
        'Outback', 'Tribeca', 'XV', 'Citi modeļi',
    ],
    'am-suzuki': [
        'Alto', 'Baleno', 'Grand Vitara', 'Ignis',
        'Jimny', 'Kizashi', 'Liana', 'S-Cross',
        'Splash', 'Swift', 'SX4', 'Vitara',
        'Wagon R+', 'Citi modeļi',
    ],
    'am-tesla': [
        'Model 3', 'Model S', 'Model X', 'Model Y',
        'Cybertruck', 'Roadster', 'Citi modeļi',
    ],
    'am-toyota': [
        'Auris', 'Avensis', 'Aygo', 'bZ4X', 'C-HR',
        'Camry', 'Corolla', 'FJ Cruiser', 'Hilux',
        'Land Cruiser', 'Prius', 'Proace', 'RAV4',
        'Sequoia', 'Urban Cruiser', 'Verso', 'Yaris', 'Citi modeļi',
    ],
    'am-volkswagen': [
        'Amarok', 'Arteon', 'Beetle', 'Caddy', 'CC',
        'Crafter', 'Eos', 'Fox', 'Golf', 'ID.3',
        'ID.4', 'Jetta', 'Passat', 'Phaeton', 'Polo',
        'Scirocco', 'Sharan', 'Tiguan', 'Tiguan Allspace',
        'Touareg', 'Touran', 'Transporter', 'Up', 'Citi modeļi',
    ],
    'am-volvo': [
        'C30', 'C40', 'C70', 'EX30', 'EX90',
        'S40', 'S60', 'S80', 'S90',
        'V40', 'V50', 'V60', 'V70', 'V90',
        'XC40', 'XC60', 'XC70', 'XC90', 'Citi modeļi',
    ],
}

total = 0
for brand_slug, model_names in models_by_brand.items():
    try:
        brand = Category.objects.get(slug=brand_slug)
    except Category.DoesNotExist:
        print(f'KLUDDA: "{brand_slug}" nav atrasta!')
        continue

    for name in model_names:
        slug = brand_slug + '-' + name.lower().replace(' ', '-').replace('.', '').replace('/', '-').replace('(', '').replace(')', '')
        slug = slug[:50]
        obj, created = Category.objects.get_or_create(
            slug=slug,
            defaults={'name': name, 'icon': 'car-front', 'parent': brand}
        )
        if created:
            total += 1

    print(f'  {brand.name}: {brand.children.count()} modeli')

print(f'\nKopa izveidoti {total} automašīnu modeļi.')
