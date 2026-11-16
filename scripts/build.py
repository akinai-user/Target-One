from pathlib import Path
import json,re,html,copy
R=Path(__file__).resolve().parent.parent
site_config=json.loads((R/'content/site-config.json').read_text())
pages=json.loads((R/'content/pages.json').read_text());pages=[p for p in pages if 'B案' not in p['name']]
esc=lambda s:html.escape(str(s),quote=True)
industries=['歯科・クリニック','ジム・フィットネス','エステ・整体','飲食店','不動産・住宅','教育・スクール']
slugs=['dental','gym','salon','restaurant','real-estate','school']
# Expand the supplied sample layout for all six industry examples, retaining sample labels.
base=next(p for p in pages if p['number']==22)
for i in range(1,6):
 p=copy.deepcopy(base);p['path']='/case/'+slugs[i]+'/'
 replacements={'歯科・クリニック':industries[i],'歯科医院':['','ジム','サロン','食堂','不動産','スクール'][i],'競合医院':'競合サービス','診療案内':'サービス案内','自院':'自社','医療法人〇〇':'','月20件':['','月30件','月25件','月40件','月15件','月30件'][i],'新規予約':['','体験予約','初回予約','予約','内見予約','体験予約'][i],'医療広告ガイドラインに沿った':'業種に合わせた'}
 for a,b in replacements.items():p=json.loads(json.dumps(p,ensure_ascii=False).replace(a,b))
 p['name']=industries[i]+'の導入事例（サンプル）';pages.append(p)
# Complete the column and glossary destinations represented by list cards.
col=next(p for p in pages if p['number']==27)
colitems=next(s for s in col['sections'] if s['name']=='一覧')['items']
colpaths=['/column/sample/','/how-to-choose/','/column/remarketing/','/column/cpc/','/column/dental/','/column/quality/']
for i,dest in enumerate(colpaths[2:],2):
 title=colitems[i]['text'].split('：')[0]
 targets=['/comparison/remarketing/','/comparison/listing/','/industry/dental/','/features/analytics/']
 source=copy.deepcopy(next(p for p in pages if p['path']==targets[i-2]))
 source.update(path=dest,name=title,title=title,description=title+'。Target-Oneのコラムです。',number=28)
 source['sections'][0]['items']=[{'type':'テキスト','text':'COLUMN'},{'type':'見出し','text':title},{'type':'テキスト','text':'ワイヤーフレームの仮記事をもとにした編集用サンプルです。'}]
 pages.append(source)
gloss=next(p for p in pages if p['number']==29)
gitems=next(s for s in gloss['sections'] if s['name']=='一覧')['items'];gpaths=['/glossary/sample/','/glossary/remarketing/','/glossary/gdn/','/glossary/cvr/','/glossary/cpa/','/glossary/comparison-stage/']
for i,dest in enumerate(gpaths[1:],1):
 title,desc=gitems[i]['text'].split('：',1)
 pages.append({'number':30,'path':dest,'name':title,'title':title+'とは','description':desc,'sections':[{'name':'ページタイトル（共通）','items':[{'type':'テキスト','text':'GLOSSARY'},{'type':'見出し','text':title+'とは'},{'type':'テキスト','text':desc}]},{'name':'詳しい説明','items':[{'type':'見出し','text':title+'の活用'},{'type':'テキスト','text':desc},{'type':'カード','text':'指定URLターゲティング広告とは：関連する仕組みを読む →'},{'type':'カード','text':'効果測定・レポート：指標の活用方法を読む →'}]}]})
lookup={p['name']:p['path'] for p in pages}
lookup.update({'指定URLターゲティング広告について':'/guide/','指定URLターゲティング広告とは':'/guide/','競合ターゲティング広告の選び方':'/how-to-choose/','リマーケティングとの違い':'/comparison/remarketing/','Target-One（指定URLターゲティング広告）':'/service/'})
def linkfor(t):
 for k in sorted(lookup,key=len,reverse=True):
  if k in t:return lookup[k]
 if '資料' in t:return '/request/'
 if '相談' in t:return '/contact/'
 return '/service/'
def a(t,u=None,cls='text-link'):return f'<a class="{cls}" href="{u or linkfor(t)}">{esc(t)}</a>'
def buttons():return '<div class="buttons">'+a('無料相談を申し込む →','/contact/','button orange')+a('資料請求 ↓','/request/','button outline')+'</div>'
logo='<a class="logo" href="/" aria-label="Target-One トップ"><strong>Target<span>-</span>One</strong><small>指定URLターゲティング広告</small></a>'
groups=[('サービス',[2,3,4,5,6,7,8,9,10,11,12,13]),('活用方法・事例',[14,15,16,17,18,19,20,21]),('料金・導入・サポート',[23,24,25,26]),('お役立ち情報',[27,29,31,32]),('お問い合わせ・会社情報',[33,34,35,36,37,38,39])]
original={p['number']:p for p in pages[:39]}
def navgroup(label,nums):
 return '<details class="nav-group"><summary>'+label+'</summary><div class="dropdown">'+''.join(a(original[n]['name'].split('（A案')[0],original[n]['path'],'nav-link') for n in nums)+'</div></details>'
header='<a class="skip" href="#main">本文へ移動</a><div class="topline">比較の瞬間に、選ばれる理由を。</div><header class="header"><div class="header-inner">'+logo+'<button class="menu-toggle" aria-expanded="false" aria-controls="navigation">メニュー <span>☰</span></button><nav id="navigation" aria-label="メインナビゲーション">'+navgroup('サービス',[2,3,4,5,6,7,8,9,10,11,12,13])+navgroup('活用方法・事例',[14,15,16,17,18,19,20,21])+a('料金プラン','/plan/','nav-direct')+navgroup('導入・サポート',[24,25,26])+navgroup('お役立ち情報',[27,29,31,32])+'</nav><div class="header-cta">'+a('資料請求','/request/','button outline')+a('無料相談を申し込む','/contact/','button orange')+'</div></div></header>'
footer='<footer><div class="container footer-grid"><div>'+logo+'<p>比較の瞬間に、<br>選ばれる理由を。</p><p class="small">Target-Oneは、株式会社AKINAIの<br>プロジェクト「ヨコドリ」が提供するサービスです。</p></div>'+''.join('<div><h2>'+label+'</h2>'+''.join(a(original[n]['name'].split('（A案')[0],original[n]['path'],'footer-link') for n in nums)+'</div>' for label,nums in groups)+'</div><div class="container copyright">© 2026 AKINAI Inc. All Rights Reserved.</div></footer><div class="mobile-cta">'+a('資料請求','/request/','button outline')+a('無料相談を申し込む','/contact/','button orange')+'</div>'
def table(t):
 rows=[x.strip().split('｜') for x in t.split(' ／ ')];out='<div class="table-scroll" tabindex="0" role="region" aria-label="比較・詳細表"><table><thead><tr>'
 out+=''.join('<th scope="col">'+esc(c or '項目')+'</th>' for c in rows[0]);out+='</tr></thead><tbody>'
 for row in rows[1:]:out+='<tr>'+''.join(('<th scope="row">' if i==0 else '<td>')+esc(c)+('</th>' if i==0 else '</td>') for i,c in enumerate(row))+'</tr>'
 return out+'</tbody></table></div>'
def stats(t):
 out='<div class="stats">'
 for part in re.split('[／/]',t):
  m=re.match(r'(.*?)（(.*?)）',part.strip())
  if m:out+='<div class="stat"><strong>'+esc(m[1])+'</strong><span>'+esc(m[2])+'</span></div>'
 return out+'</div><p class="note">※ワイヤーフレーム記載の参考値です。集計条件・根拠は公開前に確認予定です。</p>'
def pic(n,alt='サービスの画面イメージ'):
 return f'<figure><img src="/assets/images/{n}.webp" alt="{esc(alt)}" width="1200" height="675" loading="lazy"><figcaption>※掲載画像はイメージです。</figcaption></figure>'
def dashboard():
 return '''<div class="dashboard" aria-label="配信レポートの参考画面"><div class="dash-head"><span><i></i> 配信レポート</span><small>DEMO / イメージ</small></div><div class="dash-stats"><div><small>有効訪問数</small><b>1,284</b><em>↗ 18.2%</em></div><div><small>平均滞在時間</small><b>2:41</b><em>↗ 12.4%</em></div><div><small>予約・問い合わせ</small><b>63</b><em>↗ 24.1%</em></div></div><div class="chart"><svg viewBox="0 0 540 170" role="img" aria-label="訪問数の推移のイメージ"><defs><linearGradient id="chartFill" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#2475f7" stop-opacity=".25"/><stop offset="1" stop-color="#2475f7" stop-opacity="0"/></linearGradient></defs><path d="M0 148L50 140L100 144L150 115L200 108L250 87L300 82L350 62L400 55L450 33L500 25L540 6V170H0Z" fill="url(#chartFill)"/><path class="chart-line" d="M0 148L50 140L100 144L150 115L200 108L250 87L300 82L350 62L400 55L450 33L500 25L540 6" fill="none" stroke="#2676f8" stroke-width="3"/></svg><div><span>配信開始</span><span>現在</span></div></div><div class="dash-row"><span>競合A 料金ページ</span><b>CVR 4.2%</b></div><div class="dash-row"><span>比較サイト B</span><b>CVR 3.1%</b></div><div class="dash-row"><span>口コミサイト C</span><b>CVR 2.6%</b></div></div>'''
def field(label,name,typ='text',required=True,wide=False):
 return '<label class="field '+('wide' if wide else '')+'"><span>'+esc(label)+(' <b class="required">必須</b>' if required else ' <small>任意</small>')+f'</span><input type="{typ}" name="{name}" '+('required ' if required else '')+('autocomplete="email" ' if typ=='email' else '')+'></label>'
def choice(label,name,options,multi=False):
 return '<fieldset class="wide"><legend>'+label+' <b class="required">必須</b></legend><div class="choices">'+''.join(f'<label><input type="{"checkbox" if multi else "radio"}" name="{name}{"[]" if multi else ""}" value="{esc(o)}" '+('required' if not multi else '')+'>'+esc(o)+'</label>' for o in options)+'</div></fieldset>'
def form(short=False):
 out='<form class="contact-form" action="/api/contact.php" method="post" data-contact><input type="hidden" name="form_type" value="'+('資料請求' if short else '無料相談')+'"><input type="hidden" name="token"><div class="honey" aria-hidden="true"><label>Website<input name="website_check" tabindex="-1" autocomplete="off"></label></div><div class="form-grid">'
 if not short:out+=choice('お問い合わせ内容','consultation',['無料オンライン相談希望','無料電話相談希望'])
 out+=field('会社／法人／団体名','company')+field('お名前（代表者様名）','name')
 if not short:out+=field('HP','url','url',True,True)
 out+=field('メールアドレス','email','email')+field('電話番号','phone','tel',not short)
 if short:out+=field('役職','position','text',False)
 out+=choice('業種','industry',industries+['その他'],True)
 if not short:
  out+=choice('配信エリアの設定','area',['店舗半径','エリア限定','相談したい'])+choice('WEB広告の実施','advertising',['あり','なし'])
  out+='<label class="field wide"><span>ご質問・ご要望・お困りごと <small>任意</small></span><textarea name="message" rows="4"></textarea></label><div class="wide form-subtitle"><h3>無料相談のご希望日時</h3><p>本日から3営業日以降の平日をご選択ください。第1〜第3希望は必須、第4〜第5希望は任意です。<br>オンライン相談：30〜45分／電話相談：10〜15分</p></div>'
  for i in range(1,6):
   out+=field(f'第{i}希望 ご相談日',f'date{i}','date',i<4)
   out+=f'<label class="field"><span>ご相談時間'+(' <b class="required">必須</b>' if i<4 else ' <small>任意</small>')+f'</span><select name="time{i}" '+('required' if i<4 else '')+'><option value="">選択してください</option>'+''.join('<option>'+t+'</option>' for t in ['10:00','11:00','13:00','14:00','15:00','16:00','17:00'])+'</select></label>'
 else:out+='<label class="field"><span>Target-Oneを知ったきっかけ</span><select name="source"><option value="">選択してください</option><option>検索エンジン</option><option>AI検索</option><option>ご紹介</option><option>その他</option></select></label>'
 out+='</div><label class="consent"><input type="checkbox" name="consent" value="1" required><span><a href="/privacy/" target="_blank" rel="noopener">プライバシーポリシー</a>・<a href="/tokushoho/" target="_blank" rel="noopener">特記事項</a>に同意する <b class="required">必須</b></span></label><p class="form-error" role="alert"></p><button class="button orange submit" type="submit">送信内容を確認する →</button><p class="note">この制作プレビューでは送信先設定前のため実際の送信は行いません。</p></form>'
 return out

def cards(items,p):
 out='<div class="cards cols-'+str(4 if len(items)==4 else 3)+'">'
 for i,item in enumerate(items):
  text=item['text'];bits=text.split('：',1);title=bits[0];desc=bits[1] if len(bits)>1 else ''
  dest=linkfor(title);category=''
  if p['path']=='/case/':dest='/case/sample/' if i==0 else '/case/'+slugs[i]+'/';category=industries[i]
  elif p['path']=='/column/' or '/column/category/' in p['path']:
   ci=next((j for j,x in enumerate(colitems) if x['text']==text),i);dest=colpaths[ci];category=['基礎知識','基礎知識','競合対策','Web広告運用','業種別集客','Web広告運用'][ci]
  elif p['path']=='/glossary/':dest=gpaths[i];category=['さ行','ら行','英数字','英数字','英数字','は行'][i]
  elif any(x in title for x in industries):dest='/industry/'+slugs[next(j for j,x in enumerate(industries) if x in title)]+'/'
  islink=bool(category or '→' in text or '子ページ' in p.get('_section','') or p['number']==1 or '関連' in p.get('_section',''))
  tag='a' if islink else 'article'
  out+=f'<{tag} class="card" '+(f'href="{dest}" ' if islink else '')+f'data-category="{esc(category)}">'
  if p['path']=='/column/' or '/column/category/' in p['path']:out+=pic('M06' if i%2==0 else 'M05','コラムのイメージ')
  if p['path']=='/case/':out+='<div class="case-art"><span>'+['＋','◉','✧','♨','⌂','✎'][i]+'</span><small>CASE STUDY / SAMPLE</small></div>'
  out+='<span class="card-index">'+(esc(category) if category else f'{i+1:02}')+'</span><h3>'+esc(title)+'</h3>'
  if desc:out+='<p>'+esc(desc.replace(' ／ 活用方法を見る →','').replace(' ／ 詳しく見る →',''))+'</p>'
  if islink:out+='<span class="card-arrow">詳しく見る <b>↗</b></span>'
  out+=f'</{tag}>'
 return out+'</div>'

def render_section(s,p,idx):
 name=s['name'];items=s['items'];p['_section']=name
 if 'もっと見る' in name:return '<div class="container more-wrap"><button class="button outline more-button">もっと見る ↓</button><p class="note more-note" hidden>現在掲載中のコンテンツは以上です。</p></div>'
 if '絞り込み' in name:
  extra=('<div class="container category-links">カテゴリページ：'+''.join(a(c,'/column/category/'+slug+'/','category-link') for c,slug in zip(['基礎知識','競合対策','Web広告運用','業種別集客'],['basics','competition','advertising','industry']))+'</div>') if p['path']=='/column/' else ''
  return '<div class="container filters" aria-label="カテゴリで絞り込み">'+''.join('<button class="filter '+('active' if i==0 else '')+'" data-filter="'+esc(x['text'])+'" aria-pressed="'+str(i==0).lower()+'">'+esc(x['text'])+'</button>' for i,x in enumerate(items))+'</div>'+extra
 if 'フォーム' in name and p['number'] in [1,31,33,34]:
  if p['number'] in [31,33]:
   textitems=[x for x in items if x['type'] not in ['入力欄','CTA 文言'] and '□' not in x['text'] and x['text']!='必要事項を入力してください']
   return '<section class="section"><div class="container document-layout"><div>'+render_items(textitems,p)+'</div><div><h2>必要事項を入力してください</h2>'+form(True)+'</div></div></section>'
  return '<section class="section '+('navy contact-section' if p['number']==1 else '')+'"><div class="container">'+render_items([x for x in items if x['type'] in ['見出し'] or x['text']=='CONTACT' or x['text'].startswith('商圏')],p)+form()+'</div></section>'
 dark=p['number']==1 and idx in [2,8]
 pale=(p['number']==1 and idx in [4,10]) or (p['number']!=1 and idx%2==0)
 if p['number']==1 and idx==6:return '<div class="slogan"><div>比べている、その瞬間に。 <span>／ 競合訪問者に届く ／ 比較検討層ターゲティング →</span></div></div>'
 if p['number']==1 and idx==2:
  return '<section class="statement navy"><div class="container">'+''.join('<p class="'+('accent' if i==3 else '')+'">'+esc(x['text'].replace('（強調）',''))+'</p>' for i,x in enumerate(items))+'</div></section>'
 cls='section '+('navy ' if dark else 'pale ' if pale else '')
 if '最終CTA' in name:cls+=' final-cta'
 if p['number']==1 and idx==3:
  left=render_items(items[:4],p);right='<ol class="solution-steps">'+''.join('<li><span>0'+str(i+1)+'</span>'+esc(x['text'][2:])+'</li>' for i,x in enumerate(items[4:]))+'</ol>'
  return '<section class="section"><div class="container split">'+f'<div>{left}</div><div>{right}</div></div></section>'
 return '<section class="'+cls+'" id="section-'+str(idx)+'"><div class="container '+('reading' if p['number'] in [13,28,37,38] else '')+'">'+render_items(items,p)+'</div></section>'

def render_items(items,p):
 out='';pending=[]
 def flush():
  nonlocal out,pending
  if pending:out+=cards(pending,p);pending=[]
 for i,x in enumerate(items):
  t=x['text'];typ=x['type']
  if typ=='カード':pending.append(x);continue
  flush()
  if typ in ['見出し','メインコピー']:out+='<h2>'+esc(t)+'</h2>'
  elif typ=='表':out+=table(t)
  elif typ=='実績情報':out+=stats(t)
  elif typ.startswith('Q&A'):
   q,_,answer=t.partition('\nA.');out+='<details class="faq"><summary><span>Q</span>'+esc(q.replace('Q.','').strip())+'</summary><div><b>A</b><p>'+esc(answer.strip())+'</p></div></details>'
  elif typ=='素材イメージ':
   m=re.search('M\d+',t)
   if m:out+=pic(m[0],t.split('→')[0].strip())
  elif typ=='CTA 文言':out+=a(t,'#section-2' if '↓' in t else None,'button '+('orange' if '相談' in t else 'outline'))
  elif typ in ['入力欄','未定']:out+='<p class="notice">'+esc(t)+'</p>' if typ=='未定' else ''
  elif re.fullmatch('[A-Z &]+',t):out+='<p class="eyebrow">'+esc(t)+'</p>'
  elif '→' in t or '［あわせて読みたい］' in t:out+=a(t)
  elif t.startswith('執筆：'):out+='<p class="byline">執筆：Target-One編集部（仮） ／ 監修者：確認中<br>公開日：2026年10月14日 ／ 更新日：2026年10月14日</p>'
  elif t.startswith('目次 '):
   heads=[x['text'] for s in p['sections'] if s['name']=='本文' for x in s['items'] if x['type']=='見出し']
   out+='<nav class="toc" aria-label="記事の目次"><h2>目次</h2>'+''.join('<a href="#heading-'+str(j)+'">'+esc(h)+'</a>' for j,h in enumerate(heads))+'</nav>'
  elif '導入の流れ ／' in t:out+='<div class="inline-links">'+a('導入の流れ')+a('サポート体制')+a('料金プラン')+'</div>'
  elif t.startswith('パンくず'):continue
  else:out+='<p class="'+('note' if t.startswith('※') else 'check' if t.startswith('✓') else '')+'">'+esc(t)+'</p>'
 flush();return out

def subhero(p):
 items=p['sections'][0]['items'];en=next((x['text'] for x in items if re.fullmatch('[A-Z &]+',x['text'])),'TARGET-ONE')
 intro=next((x['text'] for x in reversed(items) if x['type']=='テキスト' and not x['text'].startswith('パンくず') and not re.fullmatch('[A-Z &]+',x['text'])),'')
 crumbs=[('/', 'TOP')];parts=p['path'].strip('/').split('/')
 if len(parts)>1:
  parent=next((x for x in pages if x['path']=='/'+parts[0]+'/'),None)
  if parent:crumbs.append((parent['path'],parent['name']))
 bread='<nav class="breadcrumb" aria-label="パンくずリスト">'+''.join(a(n,u,'')+'<span>›</span>' for u,n in crumbs)+'<span aria-current="page">'+esc(p['name'].split('（A案')[0])+'</span></nav>'
 return '<section class="page-hero"><div class="container">'+bread+'<p class="eyebrow">'+en+'</p><h1>'+esc(p['title'])+'</h1><p class="lead">'+esc(intro)+'</p>'+''.join(a(x['text'],'#section-2' if '↓' in x['text'] else None,'button '+('orange' if '相談' in x['text'] else 'outline')) for x in items if x['type']=='CTA 文言')+'</div></section>'

def common():
 return '<section class="section pale"><div class="container"><p class="eyebrow">SERVICE</p><h2>Target-Oneでできること</h2><div class="cards">'+''.join('<a class="card" href="'+u+'"><span class="card-index">'+n+'</span><h3>'+t+'</h3><p>'+d+'</p><span class="card-arrow">詳しく見る →</span></a>' for n,t,d,u in [('01','指定URLターゲティング広告とは','競合サイトの訪問者に広告を届ける仕組み','/guide/'),('02','サービス紹介','URL指定、エリア指定、効果測定など','/service/'),('03','料金プラン','月額18,000円から、事業に合うプランを。','/plan/')])+'</div></div></section>'
def cta():return '<section class="section navy final-cta"><div class="container"><p class="eyebrow">CONTACT</p><h2>まずは無料相談から</h2><p>商圏・業種に応じた具体的なご提案をお伝えします。<br>お問い合わせには24時間以内に対応します。</p>'+buttons()+'<p class="small">お電話：<a href="tel:05017802231">050-1780-2231</a>　メール：<a href="mailto:info@target-one.net">info@target-one.net</a></p></div></section>'
def home(p):
 hero='<section class="hero navy"><div class="container hero-layout"><div><p class="hero-tag">指定URLターゲティング広告</p><h1>“<span>競合他社を比較検討中</span>”の<br>お客様を、あなたの会社へ。</h1><p class="hero-lead">競合サイトを見ている「今まさに比較している人」だけに広告を届けます。<br>エリアや属性で絞り込み、訪問の質まで計測して改善します。</p>'+buttons()+stats('300+（アカウントの運用実績）／87%（継続率）／最短3営業日（で配信開始）')+'</div>'+dashboard()+'</div></section>'
 return hero+''.join(render_section(s,p,i) for i,s in enumerate(p['sections']) if i>0)

def writepage(p,body=None):
 path=p['path'];title=p['title']+' | Target-One';url='https://target-one.net'+path
 body=body if body is not None else home(p) if path=='/' else subhero(p)+''.join(render_section(s,p,i) for i,s in enumerate(p['sections']) if i>0)+common()+(cta() if path!='/contact/' else '')+'<div class="container company-link"><h2>Target-Oneを運営する会社について</h2>'+a('運営会社を見る →','/company/')+'</div>'
 # Create stable heading anchors for article TOCs.
 if p['number'] in [13,28]:
  heads=[x['text'] for s in p['sections'] if s['name']=='本文' for x in s['items'] if x['type']=='見出し']
  for i,h in enumerate(heads):body=body.replace('<h2>'+esc(h)+'</h2>','<h2 id="heading-'+str(i)+'">'+esc(h)+'</h2>')
 schemas=[{'@context':'https://schema.org','@type':'Organization','name':'株式会社AKINAI','url':'https://target-one.net/','telephone':'050-1780-2231'}, {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'TOP','item':'https://target-one.net/'},{'@type':'ListItem','position':2,'name':p['name'],'item':url}]}]
 faqs=[x['text'] for s in p.get('sections',[]) for x in s['items'] if x['type'].startswith('Q&A')]
 if faqs:schemas.append({'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':t.split('\nA.')[0].replace('Q.','').strip(),'acceptedAnswer':{'@type':'Answer','text':t.split('\nA.')[-1].strip()}} for t in faqs]})
 if p['number'] in [13,28]:schemas.append({'@context':'https://schema.org','@type':'Article','headline':p['title'],'datePublished':'2026-10-14T09:00:00+09:00','dateModified':'2026-10-14T09:00:00+09:00','author':{'@type':'Organization','name':'Target-One編集部（仮）'},'publisher':{'@type':'Organization','name':'株式会社AKINAI'},'mainEntityOfPage':url})
 verification=('<meta name="google-site-verification" content="'+esc(site_config.get('searchConsoleVerification',''))+'">') if site_config.get('searchConsoleVerification') else ''
 head=f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(p['description'])}"><link rel="canonical" href="{url}"><meta property="og:type" content="{'article' if p['number'] in [13,28] else 'website'}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(p['description'])}"><meta property="og:url" content="{url}"><meta property="og:site_name" content="Target-One"><meta property="og:locale" content="ja_JP"><meta property="og:image" content="https://target-one.net/assets/images/ogp.webp"><meta name="twitter:card" content="summary_large_image">{verification}<meta name="theme-color" content="#102e5a"><link rel="icon" href="/assets/images/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/css/style.css"><script src="/assets/js/config.js" defer></script><script src="/assets/js/main.js" defer></script><script type="application/ld+json">{json.dumps(schemas,ensure_ascii=False)}</script></head>'''
 doc=head+'<body>'+header+'<main id="main">'+body+'</main>'+footer+'<dialog id="confirm-dialog"><div class="dialog-inner"><button class="dialog-close" aria-label="閉じる">×</button><p class="eyebrow">CONFIRMATION</p><h2>入力内容の確認</h2><p>内容をご確認のうえ、送信してください。</p><dl id="confirm-values"></dl><p class="dialog-error" role="alert"></p><div class="buttons"><button class="button outline edit-form">入力内容を修正</button><button class="button orange send-form">この内容で送信する →</button></div></div></dialog></body></html>'
 dest=R/path.strip('/')/'index.html' if path!='/' else R/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(doc)
for p in pages:writepage(p)
for cat,slug in zip(['基礎知識','競合対策','Web広告運用','業種別集客'],['basics','competition','advertising','industry']):
 p=copy.deepcopy(col);p.update(path='/column/category/'+slug+'/',name=cat,title=cat+'のコラム',description=cat+'に関する集客・広告のコラム一覧。')
 p['sections']=[p['sections'][0],{'name':'一覧','items':[x for x in colitems if cat in x['text']]}];writepage(p)
for path,kind in [('/contact/thanks/','無料相談'),('/request/thanks/','資料請求')]:
 p={'path':path,'title':kind+'を受け付けました','name':'受付完了','description':kind+'の受付完了ページ。','number':0,'sections':[]}
 writepage(p,'<section class="section final-cta"><div class="container reading"><p class="eyebrow">THANK YOU</p><h1>'+kind+'を受け付けました</h1><p>お問い合わせいただき、ありがとうございます。<br>担当者よりご連絡いたします。</p><p>返信が届かない場合は、お電話にてお問い合わせください。</p><a href="tel:05017802231">050-1780-2231</a><div class="buttons">'+a('トップページに戻る','/','button orange')+'</div></div></section>');pages.append(p)
(R/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>https://target-one.net'+p['path']+'</loc></url>' for p in pages if '/thanks/' not in p['path'])+''.join('<url><loc>https://target-one.net/column/category/'+s+'/</loc></url>' for s in ['basics','competition','advertising','industry'])+'</urlset>')
(R/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /contact/thanks/\nDisallow: /request/thanks/\nSitemap: https://target-one.net/sitemap.xml\n')
(R/'content/page-inventory.json').write_text(json.dumps([{'path':p['path'],'title':p['title']} for p in pages],ensure_ascii=False,indent=2))
print('Generated',len(pages)+4,'pages')
