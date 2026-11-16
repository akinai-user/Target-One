from pathlib import Path
import zipfile,json
R=Path(__file__).resolve().parent.parent
exclude={'reference','scripts','content','wordpress-theme','.git','.openai','__pycache__','node_modules'}
with zipfile.ZipFile(R/'target-one-static.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(R.rglob('*')):
  rel=p.relative_to(R)
  if not p.is_file() or any(x in exclude for x in rel.parts) or p.suffix in ['.zip','.py','.md'] or p.name.startswith('.') or p.name in ['package.json','package-lock.json']:continue
  z.write(p,rel)
with zipfile.ZipFile(R/'target-one-wordpress-theme.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted((R/'wordpress-theme/target-one').rglob('*')):
  if p.is_file():z.write(p,p.relative_to(R/'wordpress-theme'))
pages=json.loads((R/'content/page-inventory.json').read_text())
for n,slug in zip(['基礎知識','競合対策','Web広告運用','業種別集客'],['basics','competition','advertising','industry']):pages.append({'path':'/column/category/'+slug+'/','title':n+'のコラム'})
(R/'PAGE-LIST.md').write_text('# ページ一覧（全59ページ）\n\n| URL | ページ |\n|---|---|\n'+''.join('| '+p['path']+' | '+p['title']+' |\n' for p in pages))
print('Packaged static site and WordPress theme.')
