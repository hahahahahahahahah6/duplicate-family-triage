#!/usr/bin/env python3
"""Generate deterministic image fixtures next to this script."""
import os
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parent / 'fixtures'
for folder in ('originals', 'copies', 'exports'):
    (root / folder).mkdir(parents=True, exist_ok=True)
image = Image.new('RGB', (320, 192))
image.putdata([(int(x * 255 / 319), int(y * 255 / 191), (x + y) % 256)
               for y in range(192) for x in range(320)])
original = root / 'originals' / 'scene.jpg'
image.save(original, quality=95)
(root / 'copies' / 'scene_copy.jpg').write_bytes(original.read_bytes())
image.resize((160, 96), Image.Resampling.LANCZOS).save(root / 'exports' / 'scene_export.jpg', quality=95)
different = Image.new('RGB', (320, 192))
different.putdata([(255 if x < 160 else 0,) * 3 for y in range(192) for x in range(320)])
different.save(root / 'different.jpg', quality=95)
(root / 'corrupt.jpg').write_bytes(b'not a jpeg\n')
(root / 'notes.txt').write_text('This file must be ignored.\n', encoding='utf-8')
for path in root.rglob('*'):
    if path.is_file():
        os.utime(path, ns=(1600000000000000000, 1600000000000000000))
print(f'Fixtures written to {root}')
