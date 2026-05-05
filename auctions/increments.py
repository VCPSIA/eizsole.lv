from decimal import Decimal

# (max_cena_ieskaitot, solis)
_TIERS = [
    (Decimal('49.99'),    Decimal('1')),
    (Decimal('99.99'),    Decimal('2')),
    (Decimal('199.99'),   Decimal('5')),
    (Decimal('499.99'),   Decimal('10')),
    (Decimal('999.99'),   Decimal('25')),
    (Decimal('2999.99'),  Decimal('50')),
    (Decimal('6000.00'),  Decimal('100')),
    (Decimal('10000.00'), Decimal('150')),
    (Decimal('50000.00'), Decimal('250')),
]
_DEFAULT = Decimal('500')


def get_increment(price):
    """Atgriež minimālo solījuma soli pēc pašreizējās cenas."""
    price = Decimal(str(price))
    for ceiling, step in _TIERS:
        if price <= ceiling:
            return step
    return _DEFAULT
