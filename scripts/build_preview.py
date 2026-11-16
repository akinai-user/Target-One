"""Export only client-facing static files; never publish the repository root."""

import argparse
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parent.parent
EXCLUDED = {'.git', 'node_modules', 'wordpress-theme', 'reference'}


def build(output, base_path, site_url):
    output = output.resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError('Output must be outside the source repository.')
    if output.exists() and any(output.iterdir()):
        raise ValueError('Output directory must be empty.')
    output.mkdir(parents=True, exist_ok=True)
    base_path = '/' + base_path.strip('/') + '/' if base_path.strip('/') else '/'
    site_url = site_url.rstrip('/') + '/'
    pages = [p for p in ROOT.rglob('index.html')
             if not EXCLUDED.intersection(p.relative_to(ROOT).parts)]
    for page in pages:
        source = page.read_text()
        if page != ROOT / 'index.html':
            main = re.search(r'<main\b[^>]*>(.*?)</main>', source, re.S)
            if not main or re.sub(r'<[^>]+>', '', main[1]).strip() != 'これから作成予定です。':
                raise ValueError(f'Non-placeholder page: {page}')
        source = re.sub(r'((?:href|src|action)=["\x27])/(?!/)',
                        lambda match: match[1] + base_path, source)
        source = source.replace('https://target-one.net/', site_url)
        destination = output / page.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(source)
    shutil.copytree(ROOT / 'assets', output / 'assets')
    # Contact forms are disabled. PHP, content JSON, reference files and ZIPs are not exported.
    (output / '.nojekyll').touch()
    (output / 'robots.txt').write_text('User-agent: *\nDisallow: /\n')
    (output / '404.html').write_text((output / 'service/index.html').read_text())
    print(f'Exported {len(pages)} pages to {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--base-path', default='/Target-One-preview/')
    parser.add_argument('--site-url', default='https://akinai-user.github.io/Target-One-preview/')
    args = parser.parse_args()
    build(args.output, args.base_path, args.site_url)
