#!/usr/bin/env python3
"""Generate a larger deterministic fixture set for the Duplicate Family Triage
dry-run prototype: repeated-import scenario (original + exact copy + resized
export per scene), unique images, corrupt files, and a non-image file.

All files get the same mtime so the keeper ranking is decided by the
documented rule (filename hint, pixels, size), not by timestamps.
"""
import os
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parent / 'fixtures2'
for folder in ('originals', 'copies', 'exports', 'unique'):
    (root / folder).mkdir(parents=True, exist_ok=True)

MTIME_NS = 1600000000000000000


def scene_image(kind, seed, size=(320, 192)):
    w, h = size
    img = Image.new('RGB', size)
    px = []
    for y in range(h):
        for x in range(w):
            if kind == 'gradient':
                px.append((int(x * 255 / max(w - 1, 1)), int(y * 255 / max(h - 1, 1)), (x * 3 + y * 7 + seed * 31) % 256))
            elif kind == 'halves':
                px.append((255, 40, 40) if (x < w // 2) != (seed % 2 == 0) else (40, 40, 255))
            elif kind == 'stripes':
                px.append((255, 255, 255) if ((x // 16) + seed) % 2 == 0 else (0, 0, 0))
            elif kind == 'dots':
                px.append((255, 220, 0) if (x % 32 < 8 and y % 32 < 8) else (20 + seed * 10, 60, 120))
            elif kind == 'checker':
                px.append((200, 200, 200) if ((x // 24) + (y // 24) + seed) % 2 == 0 else (30, 30, 30))
            else:  # 'rings'
                d = abs((x - w // 2) ** 2 + (y - h // 2) ** 2) ** 0.5
                px.append((int(d * 3 + seed * 20) % 256, 100, 180))
    img.putdata(px)
    return img


# 6 original scenes: 4 landscape, 1 portrait, 1 square (exercises orientation groups)
scenes = [
    ('scene_a', 'gradient', (320, 192)),
    ('scene_b', 'halves', (320, 192)),
    ('scene_c', 'stripes', (320, 192)),
    ('scene_d', 'dots', (320, 192)),
    ('scene_e', 'checker', (192, 320)),   # portrait
    ('scene_f', 'rings', (256, 256)),     # square
]
for i, (name, kind, size) in enumerate(scenes):
    img = scene_image(kind, i, size)
    orig = root / 'originals' / f'{name}.jpg'
    img.save(orig, quality=95)
    (root / 'copies' / f'{name}_copy.jpg').write_bytes(orig.read_bytes())
    img.resize((size[0] // 2, size[1] // 2), Image.Resampling.LANCZOS).save(
        root / 'exports' / f'{name}_export.jpg', quality=95)

# 4 unique images with no copies
uniques = [
    ('unique_1', 'gradient', (320, 192), 11),
    ('unique_2', 'halves', (320, 192), 12),
    ('unique_3', 'stripes', (192, 320), 13),
    ('unique_4', 'rings', (256, 256), 14),
]
for name, kind, size, seed in uniques:
    scene_image(kind, seed, size).save(root / 'unique' / f'{name}.jpg', quality=95)

# 2 corrupt files + 1 non-image file
(root / 'corrupt_1.jpg').write_bytes(b'not a jpeg\n')
(root / 'corrupt_2.jpg').write_bytes(b'\xff\xd8\xff\xe0truncated')
(root / 'notes.txt').write_text('This file must be ignored.\n', encoding='utf-8')

for path in root.rglob('*'):
    if path.is_file():
        os.utime(path, ns=(MTIME_NS, MTIME_NS))

n_files = sum(1 for _ in root.rglob('*') if _.is_file())
print(f'Fixtures2 written to {root}: {n_files} files '
      f'(6 originals + 6 exact copies + 6 resized exports + 4 unique images '
      f'+ 2 corrupt + 1 non-image)')
