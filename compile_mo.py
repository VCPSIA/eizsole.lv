"""Kompilē .po failus uz .mo bez ārējiem rīkiem."""
import struct


def unescape(s):
    """Konvertē .po escape secības uz īstiem simboliem."""
    return s.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')


def compile_po(po_path, mo_path):
    messages = {}
    msgid = None
    msgstr = None
    reading = None

    with open(po_path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n').rstrip('\r')
            if line.startswith('msgid "'):
                if msgid is not None and msgstr is not None:
                    messages[unescape(msgid)] = unescape(msgstr)
                msgid = line[7:-1]
                msgstr = None
                reading = 'id'
            elif line.startswith('msgstr "'):
                msgstr = line[8:-1]
                reading = 'str'
            elif line.startswith('"') and reading == 'id' and msgid is not None:
                msgid += line[1:-1]
            elif line.startswith('"') and reading == 'str' and msgstr is not None:
                msgstr += line[1:-1]
            elif not line.strip():
                if msgid is not None and msgstr is not None:
                    messages[unescape(msgid)] = unescape(msgstr)
                msgid = None
                msgstr = None
                reading = None

    if msgid is not None and msgstr is not None:
        messages[unescape(msgid)] = unescape(msgstr)

    keys = sorted(messages.keys())
    n = len(keys)

    magic = 0x950412de
    revision = 0
    header_size = 28
    id_arr_off = header_size
    str_arr_off = id_arr_off + n * 8

    id_data = b''
    str_data = b''
    for k in keys:
        id_data += k.encode('utf-8') + b'\x00'
        str_data += messages[k].encode('utf-8') + b'\x00'

    id_start = str_arr_off + n * 8
    str_start = id_start + len(id_data)

    id_arr = b''
    str_arr = b''
    id_pos = id_start
    str_pos = str_start
    for k in keys:
        kid = k.encode('utf-8')
        vstr = messages[k].encode('utf-8')
        id_arr += struct.pack('<II', len(kid), id_pos)
        id_pos += len(kid) + 1
        str_arr += struct.pack('<II', len(vstr), str_pos)
        str_pos += len(vstr) + 1

    header = struct.pack('<IIIIIII', magic, revision, n,
                         id_arr_off, str_arr_off, 0, 0)

    with open(mo_path, 'wb') as f:
        f.write(header + id_arr + str_arr + id_data + str_data)

    print(f'OK {mo_path} ({n} tulkojumi)')


for lang in ['ru', 'en', 'de']:
    po = f'locale/{lang}/LC_MESSAGES/django.po'
    mo = f'locale/{lang}/LC_MESSAGES/django.mo'
    compile_po(po, mo)

print('Gatavs!')
