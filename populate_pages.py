import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'platforma.settings'
django.setup()

from blog.models import StaticPage

privacy = """<p><em>Spēkā no 2025. gada 1. janvāra</em></p>

<h2>1. Pārzinis</h2>
<p>Personas datu pārzinis ir eizsole.lv (turpmāk — "Platforma"). Jautājumu gadījumā rakstiet uz <a href="mailto:info@eizsole.lv">info@eizsole.lv</a>.</p>

<h2>2. Kādi dati tiek vākti</h2>
<ul>
<li>Reģistrācijas dati: vārds, uzvārds vai uzņēmuma nosaukums, e-pasta adrese, tālruņa numurs, valsts, pilsēta.</li>
<li>Sludinājumu un izsoles dati: apraksti, attēli, cenas, kontaktinformācija.</li>
<li>Lietošanas dati: IP adrese, pārlūkprogramma, apmeklētās lapas (sīkdatnes).</li>
<li>Maksājumu dati: maka transakcijas (nav glabāta karte).</li>
</ul>

<h2>3. Kāpēc dati tiek apstrādāti</h2>
<ul>
<li>Konta izveide un autentifikācija.</li>
<li>Sludinājumu un izsoļu publicēšana un vadīšana.</li>
<li>Paziņojumu sūtīšana (e-pasts, SMS).</li>
<li>Krāpšanas novēršana un drošība.</li>
<li>Likumisko saistību izpilde.</li>
</ul>

<h2>4. Sīkdatnes</h2>
<p>Platforma izmanto nepieciešamās sīkdatnes sesijas uzturēšanai un analītikas sīkdatnes apmeklējumu statistikai. Jūs varat atteikties no analītikas sīkdatnēm, noklikšķinot "Noraidīt" cookie josliņā vai pārlūkprogrammas iestatījumos.</p>

<h2>5. Datu glabāšana</h2>
<p>Personas dati tiek glabāti tik ilgi, kamēr ir aktīvs konts. Pēc konta dzēšanas dati tiek dzēsti 30 dienu laikā, izņemot gadījumus, kad likums paredz ilgāku glabāšanu.</p>

<h2>6. Jūsu tiesības</h2>
<ul>
<li>Tiesības piekļūt saviem datiem.</li>
<li>Tiesības labot neprecīzus datus (profila iestatījumi).</li>
<li>Tiesības dzēst kontu un ar to saistītos datus.</li>
<li>Tiesības iebilst pret apstrādi.</li>
<li>Tiesības iesniegt sūdzību Datu valsts inspekcijai (<a href="https://www.dvi.gov.lv" target="_blank" rel="noopener">dvi.gov.lv</a>).</li>
</ul>

<h2>7. Izmaiņas politikā</h2>
<p>Par būtiskām izmaiņām privātuma politikā informēsim pa e-pastu vai ar paziņojumu platformā.</p>"""

terms = """<p><em>Spēkā no 2025. gada 1. janvāra</em></p>

<h2>1. Vispārīgie noteikumi</h2>
<p>Lietojot eizsole.lv, jūs piekrītat šiem noteikumiem. Platforma nodrošina tirgus vietu sludinājumu publicēšanai un izsoļu rīkošanai. Platforma nav darījuma puse starp pircēju un pārdevēju.</p>

<h2>2. Reģistrācija</h2>
<ul>
<li>Reģistrācijai nepieciešams derīgs e-pasts un tālrunis.</li>
<li>Lietotājam jābūt vismaz 18 gadus vecam.</li>
<li>Viens lietotājs var reģistrēt vienu kontu.</li>
<li>Lietotājs ir atbildīgs par konta drošību.</li>
</ul>

<h2>3. Sludinājumi un izsoles</h2>
<ul>
<li>Aizliegts publicēt nelikumīgas, bīstamas vai maldinošas preces.</li>
<li>Attēliem jāattēlo faktiskā prece.</li>
<li>Izsoles solījums ir saistošs — uzvarētājam jāsamaksā.</li>
<li>Platforma patur tiesības dzēst jebkuru sludinājumu bez brīdinājuma.</li>
</ul>

<h2>4. Maksājumi</h2>
<p>Maksa par sludinājumu publicēšanu un TOP funkcijām ir norādīta platformā. Visa nauda tiek iekasēta caur drošu maksājumu sistēmu. Atmaksa iespējama tikai tehnisku kļūdu gadījumā.</p>

<h2>5. Atbildības ierobežojumi</h2>
<p>Platforma neuzņemas atbildību par darījumiem starp lietotājiem, preces kvalitāti, piegādes laiku vai citiem darījuma aspektiem. Lietotāji paši ir atbildīgi par darījuma drošību.</p>

<h2>6. Pārkāpumi</h2>
<p>Noteikumu pārkāpuma gadījumā konts var tikt apturēts vai dzēsts. Nopietnu pārkāpumu gadījumā informācija var tikt nodota tiesībsargājošajām iestādēm.</p>

<h2>7. Kontakti</h2>
<p>Jautājumu gadījumā: <a href="mailto:info@eizsole.lv">info@eizsole.lv</a></p>"""

faq = """<h2>Biežāk uzdotie jautājumi</h2>

<h3>Vai eizsole.lv ir bezmaksas?</h3>
<p>Jā, eizsole.lv ir pilnīgi bezmaksas gan pircējiem, gan pārdevējiem. Sludinājumu publicēšana, solīšana un ziņapmaiņa ar pārdevēju ir bez maksas.</p>

<h3>Kā publicēt sludinājumu eizsole.lv?</h3>
<p>Reģistrējieties vai piesakieties kontā → nospiediet "Publicēt" → aizpildiet informāciju → pievienojiet fotogrāfijas → nospiediet "Publicēt". Sludinājums parādīsies pēc moderatora apstiprinājuma.</p>

<h3>Kā darbojas izsoles eizsole.lv?</h3>
<p>Izsole sākas ar minimālo cenu un beidzas noteiktā laikā. Uzvar tas, kurš piedāvājis augstāko cenu. Anti-snipe aizsardzība: ja solījums iesniegts pēdējās 60 sekundēs, izsoles laiks automātiski pagarinās par 3 minūtēm.</p>

<h3>Kā solīt izsolē?</h3>
<p>Atveriet izsoles lapu → piesakieties kontā → ievadiet solīšanas summu (ne mazāku par minimālo soli) → nospiediet "Solīt". Saņemsiet e-pasta paziņojumu, ja jūs pārsolīs.</p>

<h3>Kā sazināties ar pārdevēju?</h3>
<p>Katram sludinājumam ir poga "Sazināties". Nosūtiet ziņu tieši pārdevējam caur eizsole.lv iekšējo ziņapmaiņas sistēmu.</p>

<h3>Cik ilgi darbojas sludinājums?</h3>
<p>Sludinājums darbojas 30 dienas no publicēšanas brīža. Pēc tam to var pagarināt vai atkārtoti publicēt.</p>

<h3>Kādas kategorijas ir pieejamas?</h3>
<p>eizsole.lv piedāvā: Auto un transports, Nekustamais īpašums, Elektronika un tehnika, Mājsaimniecība, Apģērbs, Sports un hobiji, Lauksaimniecība, Celtniecība, Kolekcionēšana un daudz ko citu.</p>

<h3>Kā ziņot par aizdomīgu sludinājumu?</h3>
<p>Katram sludinājumam ir poga "Ziņot". Izvēlieties iemeslu un nosūtiet ziņojumu. Moderatori izskata ziņojumus 24 stundu laikā.</p>

<h3>Vai varu pārdot jebko?</h3>
<p>Nav atļauts pārdot: ieročus, narkotikas, viltotus produktus, dzīvniekus bez dokumentiem un jebko pretrunā Latvijas likumiem.</p>

<h3>Vai eizsole.lv darbojas mobilajā tālrunī?</h3>
<p>Jā! eizsole.lv ir optimizēts mobilajām ierīcēm un instalējams kā lietotne (PWA) bez App Store.</p>"""

data = [
    ('privacy', 'Privātuma politika', privacy),
    ('terms',   'Lietošanas noteikumi', terms),
    ('faq',     'Jautājumi un atbildes', faq),
]

for ptype, title, content in data:
    obj, created = StaticPage.objects.get_or_create(
        page_type=ptype,
        defaults={'title_lv': title, 'content_lv': content, 'is_published': True}
    )
    if not created:
        obj.title_lv = title
        obj.content_lv = content
        obj.save()
        print(f'Atjaunots: {ptype}')
    else:
        print(f'Izveidots: {ptype}')

print('Gatavs!')
