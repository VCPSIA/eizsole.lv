import os, django, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
os.environ['DJANGO_SETTINGS_MODULE'] = 'platforma.settings'
django.setup()

from blog.models import BlogPost

posts = [
    {
        'title': 'Kā pārdot auto Latvijā — pilns ceļvedis 2026',
        'excerpt': 'Uzzini kā ātri un izdevīgi pārdot savu auto Latvijā. Padomi par cenas noteikšanu, fotogrāfijām un sludinājuma rakstīšanu.',
        'content': '''Pārdot auto Latvijā var būt vienkārši, ja zini pareizos soļus. Šajā rakstā uzzināsi visu, kas nepieciešams, lai ātri atrastu pircēju par labu cenu.

**1. Nosakiet pareizu cenu**

Pirms publicēt sludinājumu, izpētiet tirgus cenas. Skatieties, par cik tiek pārdoti līdzīgi auto eizsole.lv, izsolis.lv un citos portālos. Ņemiet vērā:
- Automašīnas gadu un nobraukumu
- Tehnisko stāvokli
- Sezonas pieprasījumu

**2. Sagatavojiet auto pārdošanai**

Pirms fotografēšanas:
- Nomazgājiet auto iekšpusi un ārpusi
- Salabojiet sīkus defektus
- Sagatavojiet visus dokumentus (tehniskā pase, apdrošināšana)

**3. Uzņemiet kvalitatīvas fotogrāfijas**

Fotogrāfijas ir pirmais, ko pircējs redz. Fotografējiet:
- Ārpusi no visām pusēm
- Salonu un torpēdo
- Motoru
- Odometru

**4. Rakstiet skaidru sludinājumu**

Norādiet visus svarīgos datus: gadu, nobraukumu, dzinēju, pārnesumkārbu, defektus. Esiet godīgi — tas palīdz atrast nopietnus pircējus.

**5. Publicējiet eizsole.lv**

eizsole.lv ir bezmaksas platforma auto pārdošanai Latvijā. Jūsu sludinājums būs redzams tūkstošiem pircēju katru dienu.

Sāciet šodien — publicējiet auto sludinājumu bez maksas!''',
        'meta_keywords': 'pārdot auto Latvija, auto pārdošana, auto sludinājumi Latvija, kā pārdot auto, eizsole auto',
    },
    {
        'title': 'Izsoles Latvijā — kā solīt un uzvarēt',
        'excerpt': 'Pilns ceļvedis par internetizsollēm Latvijā. Uzzini kā darbojas izsoles, kā noteikt maksimālo cenu un kā uzvarēt.',
        'content': '''Interneta izsoles Latvijā kļūst arvien populārākas. Šis ceļvedis palīdzēs jums saprast, kā tās darbojas un kā maksimāli izmantot solīšanas priekšrocības.

**Kā darbojas online izsoles?**

Online izsolē pircēji solī augošas cenas līdz izsoles beigu laikam. Uzvar tas, kurš pēdējais piedāvājis augstāko cenu. eizsole.lv platformā katrai izsolei redzama:
- Sākuma cena
- Pašreizējā augstākā cena
- Atlikušais laiks
- Solījumu skaits

**Padomi veiksmīgai solīšanai**

1. **Pētiet pirms solīšanas** — izpētiet preces vērtību tirgū
2. **Nosakiet maksimālo cenu** — pirms sākat solīt, izlemiet, cik maksimāli maksāsiet
3. **Anti-snipe aizsardzija** — eizsole.lv automātiski pagarina izsoli, ja solījums iesniegts pēdējās 60 sekundēs
4. **Sekojiet izsolei** — ieslēdziet paziņojumus, lai nekavējoties uzzinātu par pārsolīšanu

**Kāpēc pirkt izsolē?**

- Bieži vien zemāka cena nekā regulāros sludinājumos
- Liela preču dažādība
- Droša darījumu platforma
- Pircēja aizsardzība

Sāciet solīt jau šodien — skatiet aktīvās izsoles eizsole.lv!''',
        'meta_keywords': 'izsoles Latvija, interneta izsoles, online izsoles, solīšana, eizsole izsoles, pirkt izsolē',
    },
    {
        'title': '10 padomi drošai pirkšanai tiešsaistē Latvijā',
        'excerpt': 'Kā droši pirkt no privātpersonām internetā? 10 praktiski padomi, kas palīdzēs izvairīties no krāpniekiem un veikt drošus darījumus.',
        'content': '''Pirkšana tiešsaistē no privātpersonām var būt izdevīga, bet prasa piesardzību. Lūk, 10 padomi, kas palīdzēs jums veikt drošus darījumus.

**1. Pārbaudiet pārdevēja profilu**

Pirms sazināšanās, apskatiet pārdevēja profilu — cik ilgi reģistrēts, cik sludinājumu, vai ir atsauksmes.

**2. Uzdodiet jautājumus**

Neskaidros gadījumos jautājiet. Godīgs pārdevējs labprāt atbildēs uz visiem jautājumiem.

**3. Pieprasiet papildu fotogrāfijas**

Lūdziet papildfoto no leņķiem, kas nav sludinājumā — tas parāda, ka prece tiešām eksistē.

**4. Tikšanās drošā vietā**

Priekšroku dodiet tikšanās vietām ar novērošanas kamerām — veikalu parkstāvvietās, Rīgā — tirdzniecības centros.

**5. Nemaksājiet avansā**

Izvairieties no priekšapmaksas privātpersonām. Maksājiet tikai pēc preces pārbaudes.

**6. Pārbaudiet preci klātienē**

Pirms maksāšanas rūpīgi pārbaudiet preci. Ja nepieciešams, ņemiet līdzi speciālistu.

**7. Saglabājiet saraksti**

Visu saziņu saglabājiet — SMS, e-pastus, zvanu pierakstus.

**8. Uzticieties instinktiem**

Ja kaut kas šķiet aizdomīgs — atteicieties no darījuma. Labāk zaudēt labu piedāvājumu, nekā kļūt par krāpšanas upuri.

**9. Izmantojiet drošas platformas**

Platformas kā eizsole.lv nodrošina lietotāju verifikāciju un atbalstu strīdus gadījumā.

**10. Ziņojiet par aizdomīgiem sludinājumiem**

Ja pamanāt krāpniecīgu sludinājumu, ziņojiet moderatoriem — palīdziet aizsargāt citus pircējus.

Drošu pirkšanu eizsole.lv!''',
        'meta_keywords': 'droša pirkšana tiešsaistē, sludinājumi padomi, krāpnieki internet, pirkt drošas, eizsole.lv drošums',
    },
    {
        'title': 'Nekustamais īpašums Latvijā — kā atrast labāko piedāvājumu',
        'excerpt': 'Meklē dzīvokli vai māju Latvijā? Uzzini kā atrast labāko nekustamā īpašuma piedāvājumu sludinājumu portālos.',
        'content': '''Nekustamais īpašums Latvijā ir viens no populārākajiem sludinājumu veidiem. Gan pircēji, gan pārdevēji var ievērojami ietaupīt, izmantojot tiešos sludinājumus bez starpnieka.

**Kāpēc meklēt bez starpnieka?**

Darbojoties tieši ar pārdevēju vai pircēju, jūs:
- Ietaupāt 2-5% komisiju
- Tieši sazināties ar īpašnieku
- Ātrāk vienojaties par cenu

**Rīga — populārākie rajoni**

Pērkot dzīvokli Rīgā, izvērtējiet:
- **Centrs** — augstākas cenas, lielāka pieprasījums
- **Purvciems, Imanta** — pieejamākas cenas, labi transports
- **Pļavnieki, Jugla** — zaļš, ģimenēm piemērots
- **Mārupe, Ādaži** — mājas ar dārziem, labas skolas

**Ar ko sākt meklēšanu?**

1. Nosakiet budžetu un prasības
2. Izvēlieties vēlamo rajonu
3. Meklējiet sludinājumus eizsole.lv
4. Sazinieties ar pārdevējiem
5. Apskatiet vairākus variantus

**Ko pārbaudīt pirms pirkšanas?**

- Zemesgrāmatas apliecinājums
- Komunālie parādi
- Mājas tehniskais stāvoklis
- Kaimiņi un kāpņutelpa

Skatiet nekustamā īpašuma sludinājumus eizsole.lv — Latvijas bezmaksas platformā!''',
        'meta_keywords': 'nekustamais īpašums Latvija, dzīvokļi Rīgā, mājas pārdod Latvijā, nekustamais īpašums sludinājumi, eizsole nekustamais',
    },
]

created = 0
for p in posts:
    if not BlogPost.objects.filter(slug__contains='auto-latvija').exists() or p['title'] != posts[0]['title']:
        obj, c = BlogPost.objects.get_or_create(
            title=p['title'],
            defaults={
                'excerpt':       p['excerpt'],
                'content':       p['content'],
                'meta_keywords': p['meta_keywords'],
            }
        )
        if c:
            created += 1
            print(f'Izveidots: {obj.title[:50]} → /blogs/{obj.slug}/')

print(f'\nKopā izveidoti: {created} raksti')
print(f'Esošie: {BlogPost.objects.count()} raksti')
