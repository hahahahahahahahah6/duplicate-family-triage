#!/usr/bin/env python3
"""Read-only image duplicate triage. Near families use transitive connectivity."""
import argparse
import hashlib
import json
import os
from pathlib import Path
from PIL import Image, UnidentifiedImageError

HINTS = ('screenshot', 'export', 'copy', 'edited')


def inspect(root):
    records, skipped = [], []
    count = 0
    extensions = set(Image.registered_extensions())
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not Path(directory, d).is_symlink())
        for name in sorted(files):
            path = Path(directory, name)
            if path.is_symlink():
                continue
            count += 1
            if path.suffix.lower() not in extensions:
                continue
            try:
                stat = path.stat()
                digest = hashlib.sha256()
                with path.open('rb') as stream:
                    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                        digest.update(chunk)
                with Image.open(path) as im:
                    im.load()
                    width, height = im.size
                    gray = im.convert('L').resize((8, 8), Image.Resampling.LANCZOS)
                    values = list(gray.getdata())
                    average = sum(values) / 64
                    ahash = sum((v >= average) << i for i, v in enumerate(values))
                records.append(dict(path=str(path.relative_to(root)), sha256=digest.hexdigest(),
                                    ahash=ahash, orientation=('landscape' if width > height else
                                    'portrait' if height > width else 'square'),
                                    pixels=width * height, size=stat.st_size, mtime_ns=stat.st_mtime_ns,
                                    deprioritized=any(h in name.lower() for h in HINTS)))
            except (OSError, ValueError, UnidentifiedImageError, Image.DecompressionBombError) as exc:
                skipped.append(dict(path=str(path.relative_to(root)), reason=str(exc)))
    return records, skipped, count


def rank(item):
    return (item['deprioritized'], -item['pixels'], -item['size'], item['mtime_ns'],
            len(item['path']), item['path'])


def reason(item, keeper):
    for key, description in [('deprioritized', 'screenshot/export/copy/edited filename hint'),
                             ('pixels', 'smaller pixel count'), ('size', 'smaller file size'),
                             ('mtime_ns', 'later modification time')]:
        if item[key] != keeper[key]:
            return description
    return 'longer path' if len(item['path']) != len(keeper['path']) else 'lexicographic path tiebreak'


def report(root):
    records, skipped, count = inspect(root)
    parents = list(range(len(records)))
    def find(i):
        while parents[i] != i:
            parents[i] = parents[parents[i]]
            i = parents[i]
        return i
    def union(i, j):
        parents[find(j)] = find(i)
    exact = {}
    for i, item in enumerate(records):
        exact.setdefault(item['sha256'], []).append(i)
        for j in range(i):
            other = records[j]
            if item['sha256'] == other['sha256'] or (item['orientation'] == other['orientation']
                    and (item['ahash'] ^ other['ahash']).bit_count() <= 5):
                union(i, j)
    groups = {}
    for i, item in enumerate(records):
        groups.setdefault(find(i), []).append(item)
    families = []
    for number, members in enumerate(sorted(groups.values(), key=lambda g: min(x['path'] for x in g)), 1):
        members.sort(key=rank)
        keeper = members[0]
        families.append(dict(id=f'F{number:04d}', keeper=keeper['path'],
                             members=[dict(path=m['path'], reason=reason(m, keeper),
                                           match='exact' if m['sha256'] == keeper['sha256'] else 'near (connected family)')
                                      for m in members[1:]],
                             bytes_reclaimable=sum(m['size'] for m in members[1:])))
    return dict(message='no files found' if count == 0 else 'dry-run only; no files changed',
                image_count=len(records), family_count=len(families),
                duplicate_family_count=sum(bool(f['members']) for f in families),
                exact_groups=[[records[i]['path'] for i in indices] for indices in exact.values() if len(indices) > 1],
                families=families, skipped=skipped,
                bytes_reclaimable=sum(f['bytes_reclaimable'] for f in families))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    if not args.root.is_dir() or args.root.is_symlink():
        result = dict(message='no files found', families=[], skipped=[dict(path=str(args.root), reason='not a non-symlink directory')])
    else:
        result = report(args.root)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result['message'])
        for group in result.get('exact_groups', []):
            print('Exact SHA-256 group: ' + ', '.join(group))
        for family in result['families']:
            print(f"{family['id']} keeper: {family['keeper']}")
            for member in family['members']:
                print(f"  {member['path']}: {member['reason']}; {member['match']}")
            print(f"  bytes reclaimable: {family['bytes_reclaimable']}")
        print('Skipped:')
        for item in result['skipped']:
            print(f"  {item['path']}: {item['reason']}")
        print(f"Images: {result.get('image_count', 0)}; families: {len(result['families'])}; duplicate families: {result.get('duplicate_family_count', 0)}")


if __name__ == '__main__':
    main()
