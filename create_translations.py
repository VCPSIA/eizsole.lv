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

    # ── Meklēšanas filtri ──
    "Gads":                        {"ru": "Год",                         "en": "Year",                       "de": "Jahr"},
    "Tilpums":                     {"ru": "Объём",                       "en": "Volume",                     "de": "Volumen"},
    "Dzinēja tips":                {"ru": "Тип двигателя",              "en": "Engine type",                "de": "Motortyp"},
    "Ātrumkārba":                  {"ru": "Коробка передач",            "en": "Transmission",               "de": "Getriebe"},
    "Virsbūves tips":              {"ru": "Тип кузова",                  "en": "Body type",                  "de": "Karosserietyp"},
    "Nobraukums":                  {"ru": "Пробег",                      "en": "Mileage",                    "de": "Kilometerstand"},
    "Darījuma veids":              {"ru": "Тип сделки",                  "en": "Deal type",                  "de": "Angebotsart"},
    "Veids":                       {"ru": "Тип",                         "en": "Type",                       "de": "Typ"},
    "Ražotājs":                    {"ru": "Производитель",               "en": "Manufacturer",               "de": "Hersteller"},
    "Sezona":                      {"ru": "Сезон",                       "en": "Season",                     "de": "Saison"},
    "Platums":                     {"ru": "Ширина",                      "en": "Width",                      "de": "Breite"},
    "Profils":                     {"ru": "Профиль",                     "en": "Profile",                    "de": "Profil"},
    "Rādiuss":                     {"ru": "Радиус",                      "en": "Radius",                     "de": "Radius"},
    "Slodzes indekss":             {"ru": "Индекс нагрузки",             "en": "Load index",                 "de": "Tragfähigkeitsindex"},
    "Ātr. ind.":                   {"ru": "Инд. ск.",                    "en": "Speed idx.",                 "de": "Geschw.-idx."},
    "Visi":                        {"ru": "Все",                         "en": "All",                        "de": "Alle"},
    "Visas":                       {"ru": "Все",                         "en": "All",                        "de": "Alle"},
    "Pārdod":                      {"ru": "Продаёт",                     "en": "Selling",                    "de": "Verkauft"},
    "Pērk":                        {"ru": "Покупает",                    "en": "Buying",                     "de": "Kauft"},
    "Maina":                       {"ru": "Обменивает",                  "en": "Trading",                    "de": "Tauscht"},
    "Sludinājums":                 {"ru": "Объявление",                  "en": "Listing",                    "de": "Anzeige"},
    "Lapā":                        {"ru": "На стр.",                     "en": "Per page",                   "de": "Pro Seite"},
    "kopā":                        {"ru": "всего",                       "en": "total",                      "de": "gesamt"},

    # ── Transports (apakškategorijas) ──
    "Automašīnas":                 {"ru": "Автомобили",                  "en": "Cars",                       "de": "Autos"},
    "Motocikli, motorolleri":      {"ru": "Мотоциклы, мопеды",          "en": "Motorcycles, scooters",      "de": "Motorräder, Roller"},
    "Kravas auto, autobusi":       {"ru": "Грузовики, автобусы",         "en": "Trucks, buses",              "de": "LKW, Busse"},
    "Lauksaimniecības tehnika":    {"ru": "Сельхозтехника",              "en": "Agricultural machinery",     "de": "Landmaschinen"},
    "Ūdens transports":            {"ru": "Водный транспорт",            "en": "Water transport",            "de": "Wasserfahrzeuge"},
    "Rezerves daļas":              {"ru": "Запчасти",                    "en": "Spare parts",                "de": "Ersatzteile"},
    "Riepas, diski":               {"ru": "Шины, диски",                 "en": "Tires, rims",                "de": "Reifen, Felgen"},
    "Auto piederumi":              {"ru": "Автоаксессуары",              "en": "Car accessories",            "de": "Autozubehör"},
    "Auto serviss":                {"ru": "Автосервис",                  "en": "Car service",                "de": "Kfz-Service"},
    "Noma":                        {"ru": "Аренда",                      "en": "Rental",                     "de": "Verleih"},

    # ── Nekustamais īpašums (apakškategorijas) ──
    "Dzīvokļi - pārdod":          {"ru": "Квартиры - продажа",          "en": "Apartments - for sale",      "de": "Wohnungen - Kauf"},
    "Dzīvokļi - īrē":             {"ru": "Квартиры - аренда",           "en": "Apartments - for rent",      "de": "Wohnungen - Miete"},
    "Mājas - pārdod":              {"ru": "Дома - продажа",              "en": "Houses - for sale",          "de": "Häuser - Kauf"},
    "Mājas - īrē":                 {"ru": "Дома - аренда",               "en": "Houses - for rent",          "de": "Häuser - Miete"},
    "Vasarnīcas, dārziņi":        {"ru": "Дачи, садовые участки",       "en": "Summer houses, allotments",  "de": "Ferienhäuser, Gärten"},
    "Zeme":                        {"ru": "Земля",                       "en": "Land",                       "de": "Grundstücke"},
    "Telpas biznesam":             {"ru": "Помещения для бизнеса",       "en": "Business premises",          "de": "Gewerberäume"},
    "Noliktavas, ražotnes":        {"ru": "Склады, производства",        "en": "Warehouses, factories",      "de": "Lagerhallen, Fabriken"},
    "Garāžas, stāvvietas":        {"ru": "Гаражи, парковки",            "en": "Garages, parking",           "de": "Garagen, Parkplätze"},
    "Citi īpašumi":                {"ru": "Другая недвижимость",         "en": "Other properties",           "de": "Andere Immobilien"},
    "Zeme un lauku īpašumi":      {"ru": "Земля и сельская недвижимость", "en": "Land and rural properties", "de": "Ländliche Grundstücke"},

    # ── Tehnika (apakškategorijas) ──
    "Datori, planšetes":           {"ru": "Компьютеры, планшеты",        "en": "Computers, tablets",         "de": "Computer, Tablets"},
    "Telefoni":                    {"ru": "Телефоны",                    "en": "Phones",                     "de": "Telefone"},
    "TV, audio, video":            {"ru": "ТВ, аудио, видео",            "en": "TV, audio, video",           "de": "TV, Audio, Video"},
    "Sadzīves tehnika":            {"ru": "Бытовая техника",             "en": "Home appliances",            "de": "Haushaltsgeräte"},
    "Foto, optika":                {"ru": "Фото, оптика",                "en": "Photo, optics",              "de": "Foto, Optik"},
    "Spēļu konsoles":              {"ru": "Игровые консоли",             "en": "Gaming consoles",            "de": "Spielkonsolen"},
    "Biroja tehnika":              {"ru": "Офисная техника",             "en": "Office equipment",           "de": "Bürotechnik"},
    "Tīkla iekārtas":              {"ru": "Сетевое оборудование",        "en": "Network equipment",          "de": "Netzwerkgeräte"},
    "Programmatūra":               {"ru": "Программное обеспечение",     "en": "Software",                   "de": "Software"},

    # ── Sadzīves preces (apakškategorijas) ──
    "Mēbeles":                     {"ru": "Мебель",                      "en": "Furniture",                  "de": "Möbel"},
    "Virtuves preces":             {"ru": "Кухонные товары",             "en": "Kitchen goods",              "de": "Küchenartikel"},
    "Apgaismojums":                {"ru": "Освещение",                   "en": "Lighting",                   "de": "Beleuchtung"},
    "Mājas tekstils":              {"ru": "Домашний текстиль",           "en": "Home textiles",              "de": "Heimtextilien"},
    "Vannas istaba":               {"ru": "Ванная комната",              "en": "Bathroom",                   "de": "Badezimmer"},
    "Dekorācijas":                 {"ru": "Декорации",                   "en": "Decorations",                "de": "Dekorationen"},
    "Remonta materiāli":           {"ru": "Ремонтные материалы",         "en": "Renovation materials",       "de": "Renovierungsmaterialien"},
    "Instrumenti":                 {"ru": "Инструменты",                 "en": "Tools",                      "de": "Werkzeuge"},
    "Trauki, servīzes":            {"ru": "Посуда, сервизы",             "en": "Dishes, crockery",           "de": "Geschirr, Service"},
    "Citas preces mājai":          {"ru": "Другие товары для дома",      "en": "Other home goods",           "de": "Anderes für zu Hause"},

    # ── Apģērbs (apakškategorijas) ──
    "Sieviešu apģērbs":            {"ru": "Женская одежда",              "en": "Women's clothing",           "de": "Damenbekleidung"},
    "Vīriešu apģērbs":             {"ru": "Мужская одежда",              "en": "Men's clothing",             "de": "Herrenbekleidung"},
    "Bērnu apģērbs":               {"ru": "Детская одежда",              "en": "Children's clothing",        "de": "Kinderbekleidung"},
    "Apavi - sieviešu":            {"ru": "Обувь - женская",             "en": "Shoes - women's",            "de": "Schuhe - Damen"},
    "Apavi - vīriešu":             {"ru": "Обувь - мужская",             "en": "Shoes - men's",              "de": "Schuhe - Herren"},
    "Apavi - bērnu":               {"ru": "Обувь - детская",             "en": "Shoes - children's",         "de": "Schuhe - Kinder"},
    "Somas, mugursomas":           {"ru": "Сумки, рюкзаки",             "en": "Bags, backpacks",            "de": "Taschen, Rucksäcke"},
    "Rotaslietas, pulksteņi":      {"ru": "Украшения, часы",             "en": "Jewelry, watches",           "de": "Schmuck, Uhren"},
    "Sporta apģērbs":              {"ru": "Спортивная одежда",           "en": "Sports clothing",            "de": "Sportbekleidung"},
    "Cepures, šalles, cimdi":     {"ru": "Шапки, шарфы, перчатки",     "en": "Hats, scarves, gloves",      "de": "Mützen, Schals, Handschuhe"},
    "Cits apģērbs":                {"ru": "Другая одежда",               "en": "Other clothing",             "de": "Andere Kleidung"},
    "Apakšveļa":                   {"ru": "Нижнее бельё",               "en": "Underwear",                  "de": "Unterwäsche"},

    # ── Sports (apakškategorijas) ──
    "Velosipēdi":                  {"ru": "Велосипеды",                  "en": "Bicycles",                   "de": "Fahrräder"},
    "Ziemas sports":               {"ru": "Зимний спорт",                "en": "Winter sports",              "de": "Wintersport"},
    "Ūdens sports":                {"ru": "Водный спорт",                "en": "Water sports",               "de": "Wassersport"},
    "Fitnesa inventārs":           {"ru": "Фитнес-оборудование",         "en": "Fitness equipment",          "de": "Fitnessgeräte"},
    "Medības":                     {"ru": "Охота",                       "en": "Hunting",                    "de": "Jagd"},
    "Makšķerēšana":                {"ru": "Рыбалка",                     "en": "Fishing",                    "de": "Angeln"},
    "Tūrisms, kempings":           {"ru": "Туризм, кемпинг",             "en": "Tourism, camping",           "de": "Tourismus, Camping"},
    "Futbols, bumbu spēles":       {"ru": "Футбол, командные игры",      "en": "Football, ball games",       "de": "Fußball, Ballspiele"},
    "Teniss, badmintons":          {"ru": "Теннис, бадминтон",           "en": "Tennis, badminton",          "de": "Tennis, Badminton"},
    "Cits sports":                 {"ru": "Другие виды спорта",          "en": "Other sports",               "de": "Andere Sportarten"},

    # ── Dārzniecība (apakškategorijas) ──
    "Dārza instrumenti":           {"ru": "Садовые инструменты",         "en": "Garden tools",               "de": "Gartengeräte"},
    "Augi, stādi, sēklas":        {"ru": "Растения, рассада, семена",   "en": "Plants, seedlings, seeds",   "de": "Pflanzen, Setzlinge, Samen"},
    "Dārza mēbeles":               {"ru": "Садовая мебель",              "en": "Garden furniture",           "de": "Gartenmöbel"},
    "Siltumnīcas":                 {"ru": "Теплицы",                     "en": "Greenhouses",                "de": "Gewächshäuser"},
    "Laistīšanas sistēmas":        {"ru": "Системы полива",              "en": "Irrigation systems",         "de": "Bewässerungssysteme"},
    "Dārza mājiņas":               {"ru": "Садовые домики",              "en": "Garden sheds",               "de": "Gartenhäuschen"},
    "Mēslojums, augu kopšana":    {"ru": "Удобрения, уход за растениями", "en": "Fertilizers, plant care",  "de": "Dünger, Pflanzenpflege"},
    "Dārza tehnika":               {"ru": "Садовая техника",             "en": "Garden machinery",           "de": "Gartenmaschinen"},

    # ── Bērniem (apakškategorijas) ──
    "Rotaļlietas":                 {"ru": "Игрушки",                     "en": "Toys",                       "de": "Spielzeug"},
    "Ratiņi, autokrēsli":         {"ru": "Коляски, автокресла",         "en": "Prams, car seats",           "de": "Kinderwagen, Autositze"},
    "Bērnu mēbeles":               {"ru": "Детская мебель",              "en": "Children's furniture",       "de": "Kindermöbel"},
    "Bērnu apģērbs (0-2 g.)":     {"ru": "Детская одежда (0-2 г.)",     "en": "Children's clothing (0-2 y.)", "de": "Kinderkleidung (0-2 J.)"},
    "Bērnu apģērbs (3-7 g.)":     {"ru": "Детская одежда (3-7 г.)",     "en": "Children's clothing (3-7 y.)", "de": "Kinderkleidung (3-7 J.)"},
    "Bērnu apģērbs (8+ g.)":      {"ru": "Детская одежда (8+ г.)",      "en": "Children's clothing (8+ y.)", "de": "Kinderkleidung (8+ J.)"},
    "Skolas piederumi":            {"ru": "Школьные принадлежности",     "en": "School supplies",            "de": "Schulbedarf"},
    "Grāmatas, mūzika":            {"ru": "Книги, музыка",               "en": "Books, music",               "de": "Bücher, Musik"},
    "Sporta preces bērniem":       {"ru": "Спорттовары для детей",       "en": "Sports goods for children",  "de": "Sportartikel für Kinder"},
    "Barošana, aprūpe":            {"ru": "Кормление, уход",             "en": "Feeding, care",              "de": "Ernährung, Pflege"},

    # ── Dzīvnieki (apakškategorijas) ──
    "Suņi":                        {"ru": "Собаки",                      "en": "Dogs",                       "de": "Hunde"},
    "Kaķi":                        {"ru": "Кошки",                       "en": "Cats",                       "de": "Katzen"},
    "Putni":                       {"ru": "Птицы",                       "en": "Birds",                      "de": "Vögel"},
    "Zivis, akvāriji":             {"ru": "Рыбы, аквариумы",             "en": "Fish, aquariums",            "de": "Fische, Aquarien"},
    "Grauzēji, truši":             {"ru": "Грызуны, кролики",            "en": "Rodents, rabbits",           "de": "Nagetiere, Kaninchen"},
    "Rāpuļi, eksotiskie":          {"ru": "Рептилии, экзотические",      "en": "Reptiles, exotic",           "de": "Reptilien, Exotische"},
    "Barība":                      {"ru": "Корм",                        "en": "Pet food",                   "de": "Tierfutter"},
    "Piederumi, aksesuāri":        {"ru": "Аксессуары",                  "en": "Accessories",                "de": "Zubehör"},
    "Veterinārija":                {"ru": "Ветеринария",                  "en": "Veterinary",                 "de": "Tierarzt"},
    "Zoopreču veikali":            {"ru": "Зоомагазины",                 "en": "Pet shops",                  "de": "Zoohandlungen"},

    # ── Lauksaimniecība (apakškategorijas) ──
    "Traktori":                    {"ru": "Тракторы",                    "en": "Tractors",                   "de": "Traktoren"},
    "Kombaini":                    {"ru": "Комбайны",                    "en": "Harvesters",                 "de": "Mähdrescher"},
    "Augsnes apstrāde":            {"ru": "Обработка почвы",             "en": "Soil cultivation",           "de": "Bodenbearbeitung"},
    "Lauksaimniecības piekabes":   {"ru": "Сельскохоз. прицепы",         "en": "Agricultural trailers",      "de": "Landwirtsch. Anhänger"},
    "Augu aizsardzība un mēslošana": {"ru": "Защита растений и удобрения", "en": "Crop protection and fertilization", "de": "Pflanzenschutz und Düngung"},
    "Lopkopība":                   {"ru": "Животноводство",              "en": "Animal husbandry",           "de": "Tierhaltung"},
    "Meža tehnika":                {"ru": "Лесная техника",              "en": "Forestry equipment",         "de": "Forstmaschinen"},
    "Apūdeņošana":                 {"ru": "Орошение",                    "en": "Irrigation",                 "de": "Bewässerung"},
    "Graudu un produktu apstrāde": {"ru": "Переработка зерна и продуктов", "en": "Grain and product processing", "de": "Getreide- und Produktverarbeitung"},
    "Lauksaimniecības piederumi":  {"ru": "Сельскохоз. принадлежности",  "en": "Agricultural accessories",   "de": "Landwirtsch. Zubehör"},
    "Lauksaimniecības pakalpojumi": {"ru": "Сельскохоз. услуги",         "en": "Agricultural services",      "de": "Landwirtsch. Dienstleistungen"},

    # ── Darbs (apakškategorijas) ──
    "Pilna laika darbs":           {"ru": "Работа полный день",          "en": "Full-time job",              "de": "Vollzeitarbeit"},
    "Nepilna laika darbs":         {"ru": "Работа неполный день",        "en": "Part-time job",              "de": "Teilzeitarbeit"},
    "Darbs ārzemēs":               {"ru": "Работа за рубежом",           "en": "Jobs abroad",                "de": "Jobs im Ausland"},
    "Meklē darbu":                 {"ru": "Ищу работу",                  "en": "Looking for work",           "de": "Suche Arbeit"},
    "Freelance, attālinātais":     {"ru": "Фриланс, удалённая работа",   "en": "Freelance, remote work",     "de": "Freelance, Fernarbeit"},
    "Prakses vietas":              {"ru": "Стажировки",                   "en": "Internships",                "de": "Praktika"},
    "Uzņēmējdarbība":              {"ru": "Предпринимательство",         "en": "Entrepreneurship",           "de": "Unternehmertum"},
    "Kursi, apmācība":             {"ru": "Курсы, обучение",             "en": "Courses, training",          "de": "Kurse, Schulungen"},

    # ── Celtniecība (apakškategorijas) ──
    "Būvmateriāli":                {"ru": "Строительные материалы",      "en": "Building materials",         "de": "Baumaterialien"},
    "Jumti un fasādes":            {"ru": "Кровля и фасады",             "en": "Roofs and facades",          "de": "Dächer und Fassaden"},
    "Logi un durvis":              {"ru": "Окна и двери",                "en": "Windows and doors",          "de": "Fenster und Türen"},
    "Siltumizolācija un hidroizolācija": {"ru": "Тепло- и гидроизоляция", "en": "Thermal and waterproofing", "de": "Wärme- und Abdichtung"},
    "Betona darbi un mūrēšana":    {"ru": "Бетонные работы и кладка",    "en": "Concrete works and masonry", "de": "Betonarbeiten und Mauerwerk"},
    "Koka konstrukcijas":          {"ru": "Деревянные конструкции",      "en": "Wooden structures",          "de": "Holzkonstruktionen"},
    "Grīdas un sienas apdare":     {"ru": "Полы и отделка стен",         "en": "Floor and wall finishing",   "de": "Boden- und Wandverkleidung"},
    "Santehnika":                  {"ru": "Сантехника",                  "en": "Plumbing",                   "de": "Sanitär"},
    "Apkure un ventilācija":       {"ru": "Отопление и вентиляция",      "en": "Heating and ventilation",    "de": "Heizung und Lüftung"},
    "Elektromateriāli":            {"ru": "Электроматериалы",            "en": "Electrical materials",       "de": "Elektromaterialien"},
    "Celtniecības tehnika un instrumenti": {"ru": "Строит. техника и инструменты", "en": "Construction equipment and tools", "de": "Baumaschinen und Werkzeuge"},
    "Atkritumi un demontāža":      {"ru": "Отходы и демонтаж",           "en": "Waste and demolition",       "de": "Abbruch und Entsorgung"},
    "Celtniecības pakalpojumi":    {"ru": "Строительные услуги",         "en": "Construction services",      "de": "Baudienstleistungen"},

    # ── Pakalpojumi (apakškategorijas) ──
    "Remontdarbi, būvniecība":     {"ru": "Ремонт, строительство",       "en": "Repairs, construction",      "de": "Reparaturen, Bauwesen"},
    "Santehnika, elektrika":       {"ru": "Сантехника, электрика",       "en": "Plumbing, electricity",      "de": "Sanitär, Elektrik"},
    "Tīrīšana":                    {"ru": "Уборка",                      "en": "Cleaning",                   "de": "Reinigung"},
    "Pārvākšanās":                 {"ru": "Переезд",                     "en": "Moving",                     "de": "Umzug"},
    "IT pakalpojumi":              {"ru": "IT услуги",                   "en": "IT services",                "de": "IT-Dienste"},
    "Apmācība, tulkošana":         {"ru": "Обучение, переводы",          "en": "Training, translation",      "de": "Schulung, Übersetzung"},
    "Skaistums, veselība":         {"ru": "Красота, здоровье",           "en": "Beauty, health",             "de": "Schönheit, Gesundheit"},
    "Foto, video, dizains":        {"ru": "Фото, видео, дизайн",         "en": "Photo, video, design",       "de": "Foto, Video, Design"},
    "Juridiskā palīdzība":         {"ru": "Юридическая помощь",          "en": "Legal assistance",           "de": "Rechtsberatung"},
    "Pārējie pakalpojumi":         {"ru": "Прочие услуги",               "en": "Other services",             "de": "Sonstige Dienstleistungen"},

    # ── Kolekcionēšana (apakškategorijas) ──
    "Monētas, naudaszīmes":        {"ru": "Монеты, банкноты",            "en": "Coins, banknotes",           "de": "Münzen, Banknoten"},
    "Pastmarkas, filokartija":     {"ru": "Марки, открытки",             "en": "Stamps, postcards",          "de": "Briefmarken, Postkarten"},
    "Antīkās lietas":              {"ru": "Антиквариат",                 "en": "Antiques",                   "de": "Antiquitäten"},
    "Māksla, gleznas":             {"ru": "Искусство, картины",          "en": "Art, paintings",             "de": "Kunst, Gemälde"},
    "Grāmatas, žurnāli":           {"ru": "Книги, журналы",              "en": "Books, magazines",           "de": "Bücher, Zeitschriften"},
    "Mūzika, lentas, plates":      {"ru": "Музыка, кассеты, пластинки",  "en": "Music, tapes, records",      "de": "Musik, Kassetten, Schallplatten"},
    "Filmas, DVD":                 {"ru": "Фильмы, DVD",                 "en": "Films, DVD",                 "de": "Filme, DVD"},
    "Sporta suvenīri":             {"ru": "Спортивные сувениры",         "en": "Sports memorabilia",         "de": "Sportmemorabilien"},
    "Rotaļlietas, figūriņas":      {"ru": "Игрушки, фигурки",            "en": "Toys, figurines",            "de": "Spielzeug, Figuren"},
    "Militārā vēsture":            {"ru": "Военная история",             "en": "Military history",           "de": "Militärgeschichte"},
    "Medaļas, ordeņi, nozīmītes": {"ru": "Медали, ордена, значки",      "en": "Medals, orders, badges",     "de": "Medaillen, Orden, Abzeichen"},
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
