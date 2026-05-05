import os
from PIL import Image
import io
from django.conf import settings

MAX_SIZE = (1920, 1080)
QUALITY = 82


def compress_image(image_field):
    """Saspiež attēlu vietā (pārraksta failu, nemaina nosaukumu)."""
    if not image_field or not image_field.name:
        return False
    try:
        full_path = os.path.join(settings.MEDIA_ROOT, image_field.name)
        if not os.path.exists(full_path):
            return False

        with Image.open(full_path) as img:
            img.load()

            if img.mode not in ('RGB', 'RGBA', 'L', 'P'):
                img = img.convert('RGB')

            changed = False
            if img.width > MAX_SIZE[0] or img.height > MAX_SIZE[1]:
                img = img.copy()
                img.thumbnail(MAX_SIZE, Image.LANCZOS)
                changed = True

            ext = os.path.splitext(full_path)[1].lower()
            if ext in ('.jpg', '.jpeg'):
                fmt = 'JPEG'
            elif ext == '.png':
                fmt = 'PNG'
            elif ext == '.webp':
                fmt = 'WEBP'
            else:
                fmt = 'JPEG'
                changed = True

            if img.mode == 'RGBA' and fmt == 'JPEG':
                bg = Image.new('RGB', img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3])
                img = bg

            buf = io.BytesIO()
            save_kw = {'format': fmt}
            if fmt in ('JPEG', 'WEBP'):
                save_kw['quality'] = QUALITY
                save_kw['optimize'] = True

            orig_size = os.path.getsize(full_path)
            img.save(buf, **save_kw)
            new_bytes = buf.getvalue()

            if changed or len(new_bytes) < orig_size:
                with open(full_path, 'wb') as f:
                    f.write(new_bytes)
                return True
    except Exception:
        pass
    return False
