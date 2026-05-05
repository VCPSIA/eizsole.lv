import re

# Rupji vārdi latviešu valodā
LV = [
    'mauka', 'maukas', 'maukam', 'mauku',
    'sūds', 'sūda', 'sūdam', 'sūdu', 'suds', 'suda',
    'dirst', 'dira', 'dirsa', 'dirsā', 'dirsu',
    'pička', 'pičkas', 'picka', 'pickas',
    'pizda', 'pizdas',
    'drāzt', 'drāz', 'draz', 'drazt',
    'fuck', 'mudat', 'mudaks', 'mudaka',
    'pakaļa', 'pakala', 'pakaļu',
    'piedirst', 'piedira',
    'piss', 'pise', 'pisties', 'pisties',
    'bļņa', 'blnja',
    'kuce', 'kucene', 'kuces',
    'ķēve', 'keve',
    'hujs', 'huja', 'huj',
    'mīzt', 'mizt', 'mīž',
    'izpīties', 'pīties',
    'bledj', 'bledi', 'bled',
    'stulbenis', 'stulbs',
    'idiots', 'idiot',
    'nekrofīls',
    'pedofīls', 'pedofil',
]

# Rupji vārdi angļu valodā
EN = [
    'fuck', 'fucker', 'fucking', 'fucked', 'fuk', 'fck', 'f.uck', 'f*ck',
    'shit', 'shitting', 'shitty', 'sht',
    'bitch', 'bitches', 'btch',
    'asshole', 'ass hole', 'arsehole',
    'bastard', 'bastards',
    'cunt', 'cunts',
    'dick', 'dicks', 'dik',
    'cock', 'cocks',
    'pussy', 'pussies',
    'whore', 'whores',
    'nigger', 'nigga', 'niggers',
    'faggot', 'fag',
    'retard', 'retards',
    'motherfucker', 'mofo',
    'wanker', 'wank',
    'twat', 'twats',
    'slut', 'sluts',
    'porn', 'porno',
    'penis', 'vagina',
    'rape', 'rapist',
    'pedophile', 'pedophilia',
]

# Rupji vārdi krievu valodā (kirilicā un transliterācijā)
RU = [
    # Kirilicā
    'хуй', 'хуя', 'хуем', 'хуйня', 'хуйло',
    'пизда', 'пизды', 'пиздец', 'пиздить', 'пизданутый',
    'ёбаный', 'ёб', 'еб', 'ёбать', 'ебать', 'ебал', 'ебут',
    'блядь', 'бляди', 'блядина', 'блядство',
    'сука', 'суки', 'сучка',
    'мудак', 'мудаки', 'мудаков',
    'пиздить', 'пиздёж',
    'залупа', 'залупон',
    'ёбнутый', 'ёбнуться',
    'заебал', 'заебись',
    'пиздато', 'охуеть', 'охуенно',
    'ёпта', 'ёптвою',
    'педик', 'педераст', 'педофил',
    'шлюха', 'шлюхи',
    'проститутка', 'проститутки',
    'мразь', 'мрази',
    'ублюдок', 'ублюдки',
    'долбоёб', 'долбоеб',
    'пиздюк', 'пиздюки',
    'нигер', 'нигга',
    # Transliterācijā
    'khuy', 'huy', 'huil', 'hujlo',
    'pizda', 'pizdet', 'pizdeц',
    'yobany', 'yob', 'ebal', 'ebat',
    'blyad', 'blad', 'blyadi',
    'suka', 'suki',
    'mudak', 'mudaki',
    'zalupa',
    'shlyuha', 'prostitutka',
    'pedik', 'pederast', 'pedofil',
    'mraz', 'ublydok',
    'dolboeb', 'dolboyob',
    'pisdyuk',
]

ALL_WORDS = LV + EN + RU


def _build_pattern():
    escaped = [re.escape(w) for w in ALL_WORDS]
    # Garākiem vārdiem (>4 burti) izmanto robežas; īsākiem — precīzu sakritību
    parts = []
    for w, e in zip(ALL_WORDS, escaped):
        if len(w) > 4:
            parts.append(r'\b' + e + r'\b')
        else:
            parts.append(e)
    return re.compile('|'.join(parts), re.IGNORECASE | re.UNICODE)


_PATTERN = _build_pattern()


def contains_profanity(text: str) -> bool:
    return bool(_PATTERN.search(text))


def find_profanity(text: str) -> list:
    return _PATTERN.findall(text)
