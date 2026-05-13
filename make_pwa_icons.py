"""Ģenerē PWA ikonas priekš eizsole.lv"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join(os.path.dirname(__file__), 'static', 'icons', 'pwa')
os.makedirs(OUT, exist_ok=True)

BG = (230, 57, 70)       # #e63946 — zīmola sarkans
FG = (255, 255, 255)      # balts teksts

def make_icon(size):
    img = Image.new('RGB', (size, size), BG)
    draw = ImageDraw.Draw(img)

    # Balts aplītis centrā
    margin = int(size * 0.12)
    r = size // 2
    draw.ellipse([margin, margin, size - margin, size - margin], fill=(200, 30, 44))

    # Burts "e"
    font_size = int(size * 0.52)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except Exception:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

    text = "e"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1]
    draw.text((x, y), text, fill=FG, font=font)

    path = os.path.join(OUT, f'icon-{size}.png')
    img.save(path, 'PNG')
    print(f'Saglabāts: {path}')

for sz in [72, 96, 128, 144, 152, 192, 384, 512]:
    make_icon(sz)

print('Ikonas gatavos!')
