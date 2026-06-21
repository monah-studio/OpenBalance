#!/usr/bin/env python3
"""Generate app icon for OpenBalance — used by GitHub Actions build."""
from PIL import Image, ImageDraw
import struct, os

def create_icns(output_path):
    img = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    c = 512
    for r in range(512, 0, -1):
        ratio = r / 512
        col = (int(30 + 30 * (1 - ratio)),
               int(100 + 80 * (1 - ratio)),
               int(200 + 55 * (1 - ratio)), 255)
        draw.ellipse([c - r, c - r, c + r, c + r], fill=col)

    wc = (255, 255, 255, 230)
    draw.rounded_rectangle([200, 350, 824, 700], 60, fill=None, outline=wc, width=30)
    draw.rounded_rectangle([200, 350, 450, 500], 60, fill=wc)
    draw.ellipse([430, 380, 594, 670], fill=None, outline=wc, width=28)
    draw.rectangle([495, 350, 529, 700], fill=wc)
    draw.rectangle([430, 410, 594, 440], fill=wc)
    draw.rectangle([430, 590, 594, 620], fill=wc)

    entries = []
    sizes = [(16, b'icp5'), (32, b'icp6'), (64, b'ic07'),
             (128, b'ic08'), (256, b'ic09'), (512, b'ic10')]
    seen = set()
    for s, o in sizes:
        if o in seen:
            continue
        seen.add(o)
        tmp = f'/tmp/icon_{s}.png'
        img.resize((s, s), Image.LANCZOS).save(tmp, 'PNG')
        with open(tmp, 'rb') as f:
            entries.append((o, f.read()))

    total = 8 + sum(8 + len(d) for _, d in entries)
    data = b'icns' + struct.pack('>I', total)
    for o, d in entries:
        data += o + struct.pack('>I', 8 + len(d)) + d

    with open(output_path, 'wb') as f:
        f.write(data)

if __name__ == '__main__':
    create_icns('OpenBalance.app/Contents/Resources/applet.icns')
    print(f'✓ Icon created: OpenBalance.app/Contents/Resources/applet.icns')
