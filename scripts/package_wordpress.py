from pathlib import Path
import re,json,shutil,zipfile
R=Path(__file__).resolve().parent.parent
T=R/'wordpress-theme'/'target-one';T.mkdir(parents=True,exist_ok=True)
shutil.copytree(R/'assets',T/'assets',dirs_exist_ok=True)
(T/'style.css').write_text('''/*
Theme Name: Target-One
Description: Target-Oneサービスサイト。ワイヤーフレーム準拠、コラム・事例の更新対応。
Version: 1.0.0
Requires at least: 6.0
Requires PHP: 8.0
Text Domain: target-one
*/\n''')
html=(R/'index.html').read_text();header=html.split('<body>',1)[1].split('<main',1)[0];footer=html.split('</main>',1)[1].split('</body>',1)[0]
(T/'partials').mkdir(exist_ok=True)
(T/'partials/header.html').write_text(header);(T/'partials/footer.html').write_text(footer)
seeds=[]
for file in sorted(R.glob('**/index.html')):
 if 'wordpress-theme' in file.parts or 'dist' in file.parts:continue
 url='/' if file==R/'index.html' else '/'+str(file.parent.relative_to(R))+'/'
 if url in ['/case/','/column/'] or '/category/' in url:continue
 text=file.read_text();title=re.search('<title>(.*?)</title>',text)[1].replace(' | Target-One','');description=re.search('<meta name="description" content="(.*?)">',text)[1]
 main=re.search('<main id="main">(.*?)</main>',text,re.S)[1]
 typ='target_case' if url.startswith('/case/') else 'target_column' if url.startswith('/column/') else 'page'
 seeds.append({'path':url,'title':title,'description':description,'content':'<!-- wp:html -->'+main+'<!-- /wp:html -->','type':typ})
(T/'seed.json').write_text(json.dumps(seeds,ensure_ascii=False))
