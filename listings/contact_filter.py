import re

_PHONE = re.compile(r'(\+?[0-9][\s\-\.\(\)]?){7,}')
_EMAIL = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')
_URL   = re.compile(r'(https?://|www\.|\b\w+\.(com|lv|eu|net|org|info|biz|io|co)\b)', re.I)


def contains_contact_info(text: str) -> str | None:
    if _EMAIL.search(text):
        return 'e-pasta adrese'
    if _PHONE.search(text):
        return 'telefona numurs'
    if _URL.search(text):
        return 'mājas lapas adrese'
    return None
