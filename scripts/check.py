from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,collections
root=Path(__file__).resolve().parent.parent
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.h1=0;self.ids=set();self.jsons=[];self.injson=False;self.temp='';self.hasdesc=False;self.title=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  if tag=='meta' and a.get('name')=='description':self.hasdesc=True
  if 'id'in a:self.ids.add(a['id'])
  for name in ['href','src']:
   if name in a:self.links.append(a[name])
  if tag=='script' and a.get('type')=='application/ld+json':self.injson=True;self.temp=''
 def handle_data(self,d):
  if self.injson:self.temp+=d
 def handle_endtag(self,tag):
  if tag=='script' and self.injson:self.injson=False;self.jsons.append(self.temp)
errors=[];files=list(root.glob('**/index.html'));files=[p for p in files if 'wordpress-theme' not in p.parts and 'dist' not in p.parts and 'node_modules' not in p.parts]
for p in files:
 parser=Parser();parser.feed(p.read_text())
 if parser.h1!=1:errors.append(f'{p.relative_to(root)}: h1={parser.h1}')
 if not(parser.title and parser.hasdesc):errors.append(f'{p}: meta missing')
 for s in parser.jsons:
  try:json.loads(s)
  except Exception as e:errors.append(f'{p}: JSON-LD invalid {e}')
 for link in parser.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  if not u.path:
   if u.fragment and unquote(u.fragment) not in parser.ids:errors.append(f'{p.relative_to(root)}: missing anchor {link}')
   continue
  dest=(root/u.path.lstrip('/')) if u.path.startswith('/') else p.parent/u.path
  if u.path.endswith('/'):dest=dest/'index.html'
  if not dest.exists():errors.append(f'{p.relative_to(root)}: missing {link}')
print(json.dumps({'pages':len(files),'errors':errors},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
