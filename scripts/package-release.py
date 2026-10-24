#!/usr/bin/env python3
"""Build the two legacy downloads from exact manifest files on any Python host."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

root = Path(__file__).resolve().parent.parent
manifest = json.loads((root / 'kit-manifest.json').read_text(encoding='utf-8'))
dist = root / 'dist'
prepared = []
for package in manifest['packages']:
    source = (root / 'packages' / package['id']).resolve()
    if not source.is_relative_to((root / 'packages').resolve()):
        raise SystemExit('Package source leaves packages directory.')
    archive = package['archive']
    if Path(archive).name != archive or not archive.endswith('.zip'):
        raise SystemExit('Unsafe archive name.')
    contents = []
    for name in package['files']:
        path = (source / name).resolve()
        if not path.is_relative_to(source) or not path.is_file():
            raise SystemExit(f'Invalid manifest file: {name}')
        contents.append((Path(name).as_posix(), path.read_bytes()))
    prepared.append((archive, contents))
dist.mkdir(exist_ok=True)
for archive, contents in prepared:
    output = dist / archive
    with ZipFile(output, 'w', compression=ZIP_DEFLATED) as bundle:
        for name, content in contents:
            info = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = ZIP_DEFLATED
            bundle.writestr(info, content)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix('.zip.sha256').write_text(f'{digest}  {archive}', encoding='ascii')
    print(f'Created {archive} ({len(contents)} manifest files)')
(dist / 'kit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
