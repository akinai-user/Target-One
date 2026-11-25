"""Export the static website for GitHub Pages without server or source files."""

import argparse
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parent.parent
EXCLUDED = {'.git', 'node_modules', 'wordpress-theme', 'reference', 'dist'}


def build(output, base_path, site_url):
    output = output.resolve()
    if output == ROOT or output in ROOT.parents:
        raise ValueError('Output must not be the source repository or its parent.')
    if output.exists() and any(output.iterdir()):
        raise ValueError('Output directory must be empty.')
    pages = [p for p in ROOT.rglob('index.html')
             if not EXCLUDED.intersection(p.relative_to(ROOT).parts)
             and output not in p.parents]
    config = (ROOT / 'assets/js/config.js').read_text()
    if not re.search(r'formEnabled:\s*false', config):
        raise ValueError('PHP contact forms must be disabled on GitHub Pages.')
    output.mkdir(parents=True, exist_ok=True)
    base_path = '/' + base_path.strip('/') + '/' if base_path.strip('/') else '/'
    site_url = site_url.rstrip('/') + '/'
    for page in pages:
        source = page.read_text()
        source = re.sub(r'((?:href|src|action)=["\x27])/(?!/)',
                        lambda match: match[1] + base_path, source)
        source = source.replace('https://target-one.net/', site_url)
        destination = output / page.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(source)
    shutil.copytree(ROOT / 'assets', output / 'assets')
    for script in (output / 'assets/js').glob('*.js'):
        script.write_text(re.sub(r'(["\x27])/(?!/)',
                                lambda match: match[1] + base_path,
                                script.read_text()))
    (output / '.nojekyll').touch()
    (output / 'sitemap.xml').write_text(
        (ROOT / 'sitemap.xml').read_text().replace('https://target-one.net/', site_url))
    (output / 'robots.txt').write_text(
        'User-agent: *\nAllow: /\n'
        f'Disallow: {base_path}contact/thanks/\n'
        f'Disallow: {base_path}request/thanks/\nSitemap: {site_url}sitemap.xml\n')
    (output / '404.html').write_text(
        '<!doctype html><html lang="ja"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>ページが見つかりません | Target-One</title>'
        '<h1>ページが見つかりません</h1>'
        f'<p><a href="{base_path}">トップページへ戻る</a></p></html>')
    print(f'Exported {len(pages)} pages to {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--base-path', default='/Target-One/')
    parser.add_argument('--site-url', default='https://akinai-user.github.io/Target-One/')
    args = parser.parse_args()
    build(args.output, args.base_path, args.site_url)
