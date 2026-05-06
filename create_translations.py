"""Izveido .po tulkojumu failus ru, en, de valodām."""
import os

TRANSLATIONS = {
    # Navbar
    "Meklēt sludinājumus...":     {"ru": "Поиск объявлений...",        "en": "Search listings...",         "de": "Anzeigen suchen..."},
    "Izsoles":                     {"ru": "Аукционы",                   "en": "Auctions",                   "de": "Auktionen"},
    "Publicēt":                    {"ru": "Опубликовать",               "en": "Post ad",                    "de": "Anzeige aufgeben"},
    "Paziņojumi":                  {"ru": "Уведомления",                "en": "Notifications",              "de": "Benachrichtigungen"},
    "Mans profils":                {"ru": "Мой профиль",                "en": "My profile",                 "de": "Mein Profil"},
    "Moderācija":                  {"ru": "Модерация",                  "en": "Moderation",                 "de": "Moderation"},
    "Admin panelis":               {"ru": "Панель администратора",      "en": "Admin panel",                "de": "Admin-Panel"},
    "Iziet":                       {"ru": "Выйти",                      "en": "Log out",                    "de": "Abmelden"},
    "Pieteikties":                 {"ru": "Войти",                      "en": "Log in",                     "de": "Anmelden"},
    "Reģistrēties":                {"ru": "Регистрация",                "en": "Register",                   "de": "Registrieren"},
    "Valoda":                      {"ru": "Язык",                       "en": "Language",                   "de": "Sprache"},
    # Footer
    "Platforma":                   {"ru": "Платформа",                  "en": "Platform",                   "de": "Plattform"},
    "Sākumlapa":                   {"ru": "Главная",                    "en": "Home",                       "de": "Startseite"},
    "Konts":                       {"ru": "Аккаунт",                    "en": "Account",                    "de": "Konto"},
    # Cookies
    "Mēs izmantojam sīkdatnes, lai nodrošinātu labāku lietotāja pieredzi. Turpinot lietot vietni, jūs piekrītat":
                                   {"ru": "Мы используем файлы cookie для улучшения работы сайта. Продолжая использовать сайт, вы соглашаетесь с",
                                    "en": "We use cookies to improve user experience. By continuing to use the site, you agree to the",
                                    "de": "Wir verwenden Cookies für eine bessere Nutzererfahrung. Durch die weitere Nutzung stimmen Sie der"},
    "privātuma politikai":         {"ru": "политикой конфиденциальности","en": "privacy policy",            "de": "Datenschutzrichtlinie"},
    "Piekrītu":                    {"ru": "Принять",                    "en": "Accept",                     "de": "Akzeptieren"},
    # Pieteikšanās
    "Lietotājvārds":               {"ru": "Имя пользователя",           "en": "Username",                   "de": "Benutzername"},
    "Parole":                      {"ru": "Пароль",                     "en": "Password",                   "de": "Passwort"},
    "Pieteikties sistēmā":         {"ru": "Войти в систему",            "en": "Sign in",                    "de": "Anmelden"},
    "Nav konta?":                  {"ru": "Нет аккаунта?",              "en": "No account?",                "de": "Kein Konto?"},
    "Reģistrējieties šeit":        {"ru": "Зарегистрируйтесь здесь",    "en": "Register here",              "de": "Hier registrieren"},
    "Aizmirsi paroli?":            {"ru": "Забыли пароль?",             "en": "Forgot password?",           "de": "Passwort vergessen?"},
    # Reģistrācija
    "Izveidot kontu":              {"ru": "Создать аккаунт",            "en": "Create account",             "de": "Konto erstellen"},
    "Privātpersona":               {"ru": "Частное лицо",               "en": "Private person",             "de": "Privatperson"},
    "Uzņēmums":                    {"ru": "Компания",                   "en": "Company",                    "de": "Unternehmen"},
    "Vārds":                       {"ru": "Имя",                        "en": "First name",                 "de": "Vorname"},
    "Uzvārds":                     {"ru": "Фамилия",                    "en": "Last name",                  "de": "Nachname"},
    "E-pasta adrese":              {"ru": "Адрес электронной почты",    "en": "Email address",              "de": "E-Mail-Adresse"},
    "Tālrunis":                    {"ru": "Телефон",                    "en": "Phone",                      "de": "Telefon"},
    "Valsts":                      {"ru": "Страна",                     "en": "Country",                    "de": "Land"},
    "Pilsēta":                     {"ru": "Город",                      "en": "City",                       "de": "Stadt"},
    "Apstiprināt paroli":          {"ru": "Подтвердить пароль",         "en": "Confirm password",           "de": "Passwort bestätigen"},
    # Sludinājumu publicēšana
    "Publicēt sludinājumu":        {"ru": "Опубликовать объявление",    "en": "Post listing",               "de": "Anzeige aufgeben"},
    "Virsraksts":                  {"ru": "Заголовок",                  "en": "Title",                      "de": "Titel"},
    "Apraksts":                    {"ru": "Описание",                   "en": "Description",                "de": "Beschreibung"},
    "Kategorija":                  {"ru": "Категория",                  "en": "Category",                   "de": "Kategorie"},
    "Cena":                        {"ru": "Цена",                       "en": "Price",                      "de": "Preis"},
    "Stāvoklis":                   {"ru": "Состояние",                  "en": "Condition",                  "de": "Zustand"},
    "Jauns":                       {"ru": "Новый",                      "en": "New",                        "de": "Neu"},
    "Lietots":                     {"ru": "Б/у",                        "en": "Used",                       "de": "Gebraucht"},
    "Bojāts":                      {"ru": "Повреждённый",               "en": "Damaged",                    "de": "Beschädigt"},
    "Bildes":                      {"ru": "Фотографии",                 "en": "Photos",                     "de": "Fotos"},
    "Publicēt!":                   {"ru": "Опубликовать!",              "en": "Post!",                      "de": "Veröffentlichen!"},
    "Atrašanās vieta":             {"ru": "Местоположение",             "en": "Location",                   "de": "Standort"},
    # Izsoles
    "Sākumcena":                   {"ru": "Начальная цена",             "en": "Starting price",             "de": "Startpreis"},
    "Pašreizējā cena":             {"ru": "Текущая цена",               "en": "Current price",              "de": "Aktueller Preis"},
    "Solīt":                       {"ru": "Сделать ставку",             "en": "Place bid",                  "de": "Bieten"},
    "Izsole beigusies":            {"ru": "Аукцион завершён",           "en": "Auction ended",              "de": "Auktion beendet"},
    "Pērc tūlīt":                  {"ru": "Купить сейчас",              "en": "Buy now",                    "de": "Sofort kaufen"},
    "Laiks atlicis":               {"ru": "Времени осталось",           "en": "Time left",                  "de": "Verbleibende Zeit"},
    "Uzvarētājs":                  {"ru": "Победитель",                 "en": "Winner",                     "de": "Gewinner"},
    "Solījumu vēsture":            {"ru": "История ставок",             "en": "Bid history",                "de": "Gebotshistorie"},
    # Profils
    "Profils":                     {"ru": "Профиль",                    "en": "Profile",                    "de": "Profil"},
    "Rediģēt profilu":             {"ru": "Редактировать профиль",      "en": "Edit profile",               "de": "Profil bearbeiten"},
    "Mani sludinājumi":            {"ru": "Мои объявления",             "en": "My listings",                "de": "Meine Anzeigen"},
    "Maks":                        {"ru": "Кошелёк",                    "en": "Wallet",                     "de": "Geldbörse"},
    "Atlikums":                    {"ru": "Баланс",                     "en": "Balance",                    "de": "Guthaben"},
    "Papildināt maku":             {"ru": "Пополнить кошелёк",          "en": "Top up wallet",              "de": "Guthaben aufladen"},
    # Vispārīgi pogas
    "Saglabāt":                    {"ru": "Сохранить",                  "en": "Save",                       "de": "Speichern"},
    "Atcelt":                      {"ru": "Отмена",                     "en": "Cancel",                     "de": "Abbrechen"},
    "Dzēst":                       {"ru": "Удалить",                    "en": "Delete",                     "de": "Löschen"},
    "Labot":                       {"ru": "Редактировать",              "en": "Edit",                       "de": "Bearbeiten"},
    "Apstiprināt":                 {"ru": "Подтвердить",                "en": "Confirm",                    "de": "Bestätigen"},
    "Meklēt":                      {"ru": "Поиск",                      "en": "Search",                     "de": "Suchen"},
    "Atpakaļ":                     {"ru": "Назад",                      "en": "Back",                       "de": "Zurück"},
    "Skatīt vairāk":               {"ru": "Показать больше",            "en": "View more",                  "de": "Mehr anzeigen"},
    "Sazināties":                  {"ru": "Связаться",                  "en": "Contact",                    "de": "Kontakt"},
    # Meklēšana
    "Meklēšanas rezultāti":        {"ru": "Результаты поиска",          "en": "Search results",             "de": "Suchergebnisse"},
    "Nav rezultātu":               {"ru": "Результатов не найдено",     "en": "No results found",           "de": "Keine Ergebnisse gefunden"},
    # Kategorijas
    "Visas kategorijas":           {"ru": "Все категории",              "en": "All categories",             "de": "Alle Kategorien"},
    "Transports":                  {"ru": "Транспорт",                  "en": "Transport",                  "de": "Transport"},
    "Nekustamais īpašums":         {"ru": "Недвижимость",               "en": "Real estate",                "de": "Immobilien"},
    "Tehnika":                     {"ru": "Техника",                    "en": "Electronics",                "de": "Elektronik"},
    "Sadzīves preces":             {"ru": "Товары для дома",            "en": "Home goods",                 "de": "Haushaltswaren"},
    "Apģērbs":                     {"ru": "Одежда",                     "en": "Clothing",                   "de": "Kleidung"},
    "Sports":                      {"ru": "Спорт",                      "en": "Sports",                     "de": "Sport"},
    "Dārzniecība":                 {"ru": "Садоводство",                "en": "Gardening",                  "de": "Gartenarbeit"},
    "Bērniem":                     {"ru": "Детское",                    "en": "For children",               "de": "Für Kinder"},
    "Dzīvnieki":                   {"ru": "Животные",                   "en": "Animals",                    "de": "Tiere"},
    "Lauksaimniecība":             {"ru": "Сельское хозяйство",         "en": "Agriculture",                "de": "Landwirtschaft"},
    "Darbs":                       {"ru": "Работа",                     "en": "Jobs",                       "de": "Arbeit"},
    "Celtniecība":                 {"ru": "Строительство",              "en": "Construction",               "de": "Bauwesen"},
    "Pakalpojumi":                 {"ru": "Услуги",                     "en": "Services",                   "de": "Dienstleistungen"},
    "Kolekcionēšana":              {"ru": "Коллекционирование",         "en": "Collectibles",               "de": "Sammlerstücke"},
    # Sākumlapa
    "Lētākā izsoļu un sludinājumu platforma": {"ru": "Самая доступная аукционная платформа", "en": "The most affordable auction platform", "de": "Die günstigste Auktionsplattform"},
    "Skatīt izsoles":              {"ru": "Смотреть аукционы",           "en": "View auctions",              "de": "Auktionen ansehen"},
    "Kategorijas":                 {"ru": "Категории",                   "en": "Categories",                 "de": "Kategorien"},
    "Skatīt visu":                 {"ru": "Посмотреть все",              "en": "View all",                   "de": "Alle anzeigen"},
    "Pēdējās skatītās":            {"ru": "Недавно просмотренные",       "en": "Recently viewed",            "de": "Zuletzt angesehen"},
    "Pēc vienošanās":              {"ru": "По договорённости",           "en": "By agreement",               "de": "Nach Vereinbarung"},
    # Izsoles lapa
    "Aktīvās izsoles":             {"ru": "Активные аукционы",           "en": "Active auctions",            "de": "Aktive Auktionen"},
    "Pašlaik nav aktīvu izsolu":   {"ru": "Сейчас нет активных аукционов", "en": "No active auctions at the moment", "de": "Derzeit keine aktiven Auktionen"},
    "Esi pirmais, kas publicē izsoli!": {"ru": "Будьте первым, кто создаст аукцион!", "en": "Be the first to post an auction!", "de": "Seien Sie der Erste mit einer Auktion!"},
    "Publicēt izsoli":             {"ru": "Опубликовать аукцион",        "en": "Post auction",               "de": "Auktion erstellen"},
    # Izsoles detaļas
    "Sākums":                      {"ru": "Главная",                     "en": "Home",                       "de": "Startseite"},
    "Izsoles":                     {"ru": "Аукционы",                    "en": "Auctions",                   "de": "Auktionen"},
    "Pārdevējs":                   {"ru": "Продавец",                    "en": "Seller",                     "de": "Verkäufer"},
    "Sazināties ar pārdevēju":     {"ru": "Связаться с продавцом",       "en": "Contact seller",             "de": "Verkäufer kontaktieren"},
    "Pieteikties, lai solītu":     {"ru": "Войдите, чтобы делать ставки", "en": "Sign in to bid",            "de": "Anmelden zum Bieten"},
    "Solīt!":                      {"ru": "Сделать ставку!",              "en": "Place bid!",                 "de": "Bieten!"},
    "Vēl nav solījumu — esi pirmais!": {"ru": "Ставок пока нет — будьте первым!", "en": "No bids yet — be the first!", "de": "Noch keine Gebote — seien Sie der Erste!"},
    "Rezerves cena sasniegta":     {"ru": "Резервная цена достигнута",   "en": "Reserve price met",          "de": "Mindestpreis erreicht"},
    "Rezerves cena nav sasniegta": {"ru": "Резервная цена не достигнута", "en": "Reserve price not met",     "de": "Mindestpreis nicht erreicht"},
    # Kategoriju lapa
    "Šajā kategorijā vēl nav sludinājumu.": {"ru": "В этой категории пока нет объявлений.", "en": "No listings in this category yet.", "de": "Noch keine Anzeigen in dieser Kategorie."},
    "Meklēšanas filtri":           {"ru": "Фильтры поиска",              "en": "Search filters",             "de": "Suchfilter"},
    "Notīrīt":                     {"ru": "Очистить",                    "en": "Clear",                      "de": "Zurücksetzen"},
    "Nepareizs lietotājvārds vai parole.": {"ru": "Неверное имя пользователя или пароль.", "en": "Incorrect username or password.", "de": "Falscher Benutzername oder Passwort."},
    "Pieteikties sistēmā":         {"ru": "Войти в систему",             "en": "Sign in",                    "de": "Anmelden"},
    "Reģistrēties":                {"ru": "Регистрация",                 "en": "Register",                   "de": "Registrieren"},
    "Jau ir konts?":               {"ru": "Уже есть аккаунт?",          "en": "Already have an account?",   "de": "Bereits ein Konto?"},
    "Konta veids":                 {"ru": "Тип аккаунта",                "en": "Account type",               "de": "Kontotyp"},
    "Privātpersona":               {"ru": "Частное лицо",                "en": "Private person",             "de": "Privatperson"},
    "Uzņēmums":                    {"ru": "Компания",                    "en": "Company",                    "de": "Unternehmen"},
    # Ziņojumi / kļūdas
    "Lūdzu aizpildiet visus laukus.": {"ru": "Пожалуйста, заполните все поля.", "en": "Please fill in all fields.", "de": "Bitte füllen Sie alle Felder aus."},
    "Reģistrācija veiksmīga!":     {"ru": "Регистрация прошла успешно!", "en": "Registration successful!", "de": "Registrierung erfolgreich!"},
    "Sludinājums publicēts.":      {"ru": "Объявление опубликовано.",   "en": "Listing published.",         "de": "Anzeige veröffentlicht."},
}

PO_HEADER = '''\
# {lang} translations for eizsole.lv
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Language: {code}\\n"

'''

LANG_NAMES = {
    'ru': 'Russian',
    'en': 'English',
    'de': 'German',
}

for code in ['ru', 'en', 'de']:
    path = f'locale/{code}/LC_MESSAGES/django.po'
    lines = [PO_HEADER.format(lang=LANG_NAMES[code], code=code)]
    for lv_str, translations in TRANSLATIONS.items():
        translated = translations.get(code, '')
        lines.append(f'msgid "{lv_str}"\n')
        lines.append(f'msgstr "{translated}"\n\n')
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f'Uzrakstīts: {path} ({len(TRANSLATIONS)} virknes)')

print('\nGatavs! Tagad jāpārkompilē: compilemessages')
