"""Page layouts derived from the supplied wireframe and the completed TOP."""

import html
import json
import re
import components


FONT_HEAD = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400..900&amp;display=swap">
<link rel="stylesheet" href="/assets/css/top.css">
<link rel="stylesheet" href="/assets/css/pages.css">
<link rel="stylesheet" href="/assets/css/top-motion.css">
<link rel="stylesheet" href="/assets/css/sub-components.css">
<script src="/assets/js/top-motion.js" defer></script>'''


class PageDesign:
    def __init__(self, root):
        self.root = root
        self.top = (root / 'index.html').read_text()
        self.layouts = json.loads((root / 'content/wire-layout.json').read_text())['pages']
        self.dimensions = {}
        for image in re.findall(r'<img\b[^>]*>', self.top, re.S):
            attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', image))
            self.dimensions[attrs['src']] = (attrs['width'], attrs['height'])
        for number in range(1, 13):
            sizes = [(960, 600)] * 4 + [(1200, 630)] * 2 + [(1200, 675)] * 2 + [(600, 800)] * 2 + [(1200, 560), (1200, 420)]
            self.dimensions[f'/assets/images/M{number:02}.webp'] = sizes[number - 1]
        for number in range(1, 6):
            self.dimensions[f'/assets/images/pages/member-{number}.webp'] = (200, 240)

    @staticmethod
    def esc(text):
        return html.escape(str(text), quote=True)

    def image(self, source, alt='', cls='', eager=False):
        width, height = self.dimensions[source]
        loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
        return f'<img src="{source}" alt="{self.esc(alt)}" width="{width}" height="{height}" class="{cls}" {loading} decoding="async">'

    def picture(self, number, alt='サービス画面のイメージ'):
        return '<figure>' + self.image(f'/assets/images/{number}.webp', alt) + '<figcaption>※掲載画像はイメージです。</figcaption></figure>'

    def chrome(self):
        header = re.search(r'<header\b.*?</header>', self.top, re.S)[0]
        footer = re.search(r'<footer\b.*?</footer>', self.top, re.S)[0]
        mobile = re.search(r'<div class="mobile-cta">.*?</div>', self.top, re.S)[0]
        return ('<a class="skip" href="#main">本文へ移動</a>' + header.replace('href="#contact"', 'href="/contact/"'),
                (footer + mobile).replace('href="#contact"', 'href="/contact/"'))

    def layout(self, page, name):
        return next((section['layout'] for section in self.layouts.get(str(page['number']), []) if section['name'] == name), '')

    @staticmethod
    def unify_body(source):
        """Use TOP components without changing content, links or page structure."""
        def shared_classes(match):
            classes = match[1].split()
            if 'card' in classes and 'sub-card' not in classes:
                classes.append('sub-card')
            if 'button' in classes:
                variant = 'top-button-orange' if 'orange' in classes else 'top-button-outline'
                classes = [c for c in classes if c not in ('button', 'orange', 'outline')]
                classes += ['top-button', variant]
            if 'text-link' in classes:
                classes = ['top-link' if c == 'text-link' else c for c in classes]
            if 'card-arrow' in classes and 'top-link' not in classes:
                classes.append('top-link')
            if 'wire-final-cta' in classes and 'shared-invitation' not in classes:
                classes.append('shared-invitation')
            if ('solution-section' in classes or ('final-cta' in classes and 'navy' in classes)) and 'top-dark' not in classes:
                classes.append('top-dark')
            return 'class="' + ' '.join(classes) + '"'

        source = re.sub(r'class="([^"]*)"', shared_classes, source)

        def card_heading(match):
            card = match[0]
            if 'card-heading' in card or 'class="card-icon"' not in card:
                return card
            return re.sub(
                r'(<img\b[^>]*class="card-icon"[^>]*>\s*(?:<span class="card-index">.*?</span>\s*)?<h3>.*?</h3>)',
                r'<div class="card-heading">\1</div>', card, count=1, flags=re.S,
            )

        source = re.sub(r'<(a|article)\b[^>]*class="card sub-card"[^>]*>.*?</\1\s*>', card_heading, source, flags=re.S)

        def consultation_heading(match):
            section = match[0]
            return re.sub(r'(<h2>)まずは無料相談から(</h2>)',
                          r'\1まずは<span class="cta-accent">無料相談</span>から\2', section)

        return re.sub(r'<section\b[^>]*class="section navy final-cta top-dark"[^>]*>.*?</section>',
                      consultation_heading, source, flags=re.S)

    @staticmethod
    def kind(page):
        number = page['number']
        if number in (13, 28):
            return 'article'
        if number in (37, 38, 39):
            return 'legal'
        if number in (21, 27, 29, 32):
            return 'listing'
        if number == 22:
            return 'case-detail'
        if number == 30:
            return 'term'
        if number in (31, 33, 34):
            return 'form'
        return 'service'

    @staticmethod
    def business(page):
        match = re.match(r'/(?:industry|case)/(dental|gym|salon|restaurant|real-estate|school)/', page['path'])
        return match[1] if match else 'dental' if page['number'] == 22 else None

    def hero(self, page, old_hero):
        media = None
        if page['number'] == 23:
            media = '<div class="price-hero-card"><span>月額・配信費込み</span><p>18,000<span>円〜</span></p><small>税抜 ／ ライトプラン</small></div>'
        contents = re.search(r'<div class="container">(.*)</div></section>', old_hero, re.S)[1]
        breadcrumb, contents = re.match(r'(<nav class="breadcrumb".*?</nav>)(.*)', contents, re.S).groups()
        eyebrow = re.search(r'<p class="eyebrow">(.*?)</p>', contents, re.S)[1]
        title = re.search(r'<h1>(.*?)</h1>', contents, re.S)[1]
        lead = re.search(r'<p class="lead">(.*?)</p>', contents, re.S)[1]
        actions = re.findall(r'<a\b[^>]*class="button[^>]*>.*?</a>', contents, re.S)
        actions = '<div class="buttons">' + ''.join(actions) + '</div>' if actions else ''
        return components.hero(breadcrumb, eyebrow, title, lead, actions, media or '')

    def guide(self):
        config = json.loads((self.root / 'content/guide-hero.json').read_text())
        source = (self.root / 'content/guide-main.html').read_text()
        blocks = {
            'hero': components.hero(**config, actions=components.buttons('詳しく見る ↓', '#section-2', white=True), guide=True),
            'services': components.services(), 'contact': components.contact(), 'company': components.company(),
        }
        for name, block in blocks.items():
            source = source.replace(f'<!-- component:{name} -->', block)
        return re.search(r'<main\b[^>]*>(.*?)</main>', source, re.S)[1]

    def card_image(self, page, title, index):
        section = page.get('_section', '')
        if page['path'] == '/glossary/':
            return ''
        businesses = ['dental', 'gym', 'salon', 'restaurant', 'real-estate', 'school']
        if page['path'] == '/industry/' or page['path'] == '/case/':
            return self.image(f'/assets/images/top/{businesses[index % 6]}.webp', '業種別の活用イメージ', 'card-photo')
        if page['path'] == '/column/' or '/column/category/' in page['path']:
            return self.image('/assets/images/M05.webp' if index % 2 else '/assets/images/M06.webp', 'コラムのイメージ', 'card-photo')
        if '関連する事例' in section:
            slug = next((slug for word, slug in zip(['歯科', 'ジム', 'サロン', '食堂', '不動産', 'スクール'], businesses) if word in title), businesses[(index + 1) % 6])
            return self.image(f'/assets/images/top/{slug}.webp', '導入事例のイメージ', 'card-photo')
        if 'ステップ' in section or '無料相談の流れ' in section:
            icons = ['support-consult', 'support-plan', 'support-start', 'method-analytics']
            if page['number'] == 3:
                icons = ['method-url', 'method-audience', 'solution-delivery', 'method-analytics']
            return self.image('/assets/images/top/' + icons[index % len(icons)] + '.webp', '', 'card-icon')
        words = [('URL', 'method-url'), ('エリア', 'method-area'), ('属性', 'method-area'), ('配信', 'solution-delivery'), ('GDN', 'solution-delivery'), ('YouTube', 'solution-delivery'), ('レポート', 'method-analytics'), ('測定', 'method-analytics'), ('ダッシュボード', 'method-analytics'), ('制作', 'method-audience')]
        asset = next((asset for word, asset in words if word in title), None)
        return self.image('/assets/images/top/' + asset + '.webp', '', 'card-icon') if asset else ''

    def decorate_cards(self, cards, page):
        section = page.get('_section', '')
        layout = self.layout(page, section)
        columns = re.search(r'カード：.*?PC (\d)列', layout, re.S)
        if columns:
            cards = re.sub(r'cols-\d', 'cols-' + columns[1], cards, count=1)
        if 'ステップ' in section or '無料相談の流れ' in section:
            cards = cards.replace('class="cards ', 'class="cards step-cards ', 1)
        if page['path'] == '/glossary/':
            cards = cards.replace('class="cards ', 'class="cards term-cards ', 1)
        if page['path'] == '/case/':
            cards = re.sub(r'<div class="case-art">.*?</div>', '', cards, flags=re.S)
        index = 0

        def add_image(match):
            nonlocal index
            block = match[0]
            title = re.search(r'<h3>(.*?)</h3>', block, re.S)
            title = html.unescape(title[1]) if title else ''
            visual = self.card_image(page, title, index)
            if visual:
                block = re.sub(r'<figure>.*?</figure>', '', block, flags=re.S)
                block = re.sub(r'(<(?:a|article)\b[^>]*>)', lambda start: start[1] + visual, block, count=1)
            if 'ステップ' in section or '無料相談の流れ' in section:
                block = re.sub(r'(<h3>)(?:STEP\.?\s*)?\d+[\s　.]*', r'\1', block)
            # Related sample cases should lead to their corresponding case detail.
            if '関連する事例' in section:
                for word, slug in [('ジム', 'gym'), ('サロン', 'salon'), ('食堂', 'restaurant'), ('不動産', 'real-estate'), ('スクール', 'school'), ('歯科', 'sample')]:
                    if word in title:
                        block = re.sub(r'href="[^"]+"', f'href="/case/{slug}/"', block, count=1)
                        break
            index += 1
            return block

        return re.sub(r'<(a|article)\b[^>]*class="card"[^>]*>.*?</\1>', add_image, cards, flags=re.S)

    def section(self, section, page, index, render_items, render_form):
        name = section['name']
        items = section['items']
        page['_section'] = name
        classes = ['section', 'wire-section']
        if name.startswith('解決策') or name == '理念':
            classes += ['navy', 'solution-section']
        elif '最終CTA' in name:
            classes += ['final-cta', 'wire-final-cta']
        elif index % 2 == 0:
            classes += ['pale']
        if name.startswith('ステップ') or '無料相談の流れ' in name:
            classes += ['steps-section']
        if name.startswith('よくある質問'):
            classes += ['faq-section']
        if '本文' in name or name in ('目次', 'まとめ', 'アイキャッチ・記事情報'):
            classes += ['reading-section']
        body = render_items(items, page)
        layout = 'container'
        if '使用イメージ' in name:
            classes += ['image-section']
            text = render_items([item for item in items if item['type'] != '素材イメージ'], page)
            pictures = render_items([item for item in items if item['type'] == '素材イメージ'], page)
            body = '<div class="image-section-copy">' + text + '</div><div class="image-section-media">' + pictures + '</div>'
            layout += ' image-layout'
        if name == '会社情報の表＋地図':
            heading = next((item['text'] for item in items if item['type'] == '見出し'), '会社情報')
            data = render_items([item for item in items if item['type'] == '表'], page)
            pictures = render_items([item for item in items if item['type'] == '素材イメージ'], page)
            body = '<h2>' + self.esc(heading) + '</h2><div class="company-layout"><div>' + data + '</div><div>' + pictures + '</div></div>'
        if name == 'メンバー':
            roles = ['代表取締役', '運用責任者', '広告運用', 'クリエイティブ', 'カスタマーサクセス']
            body = '<h2>メンバー</h2><div class="member-grid">' + ''.join('<figure>' + self.image(f'/assets/images/pages/member-{i + 1}.webp', 'メンバー写真の仮イメージ') + '<figcaption><strong>〇〇 〇〇</strong><span>' + role + '</span></figcaption></figure>' for i, role in enumerate(roles)) + '</div>'
        if name == '沿革':
            body = '<h2>沿革</h2><dl class="history-list">'
            for position, item in enumerate(items[1:]):
                body += ('<dt>' if item['type'] == '見出し' else '<dd>') + self.esc(item['text']) + ('</dt>' if item['type'] == '見出し' else '</dd>')
            body += '</dl>'
        if page['number'] == 32 and name == '一覧':
            body = '<div class="news-list">'
            for item in items:
                match = re.match(r'(\d{4}\.\d{2}\.\d{2})\s*［([^］]+)］\s*(.*)', item['text'])
                if match:
                    date, category, title = match.groups()
                    body += f'<article class="card news-item" data-category="{self.esc(category)}"><time datetime="{date.replace(".", "-")}">{date}</time><span class="news-category">{category}</span><h2>{self.esc(title)}</h2></article>'
            body += '</div>'
        if 'フォーム' in name and page['number'] in (31, 33, 34):
            if page['number'] in (31, 33):
                text_items = [item for item in items if item['type'] not in ('入力欄', 'CTA 文言') and '□' not in item['text'] and item['text'] != '必要事項を入力してください']
                body = '<div class="document-intro">' + render_items(text_items, page) + '</div><div class="document-form"><h2>必要事項を入力してください</h2>' + render_form(True) + '</div>'
                layout += ' document-layout'
            else:
                classes = ['section', 'wire-section', 'top-contact', 'top-dark']
                body = '<h2>無料相談のお申し込み</h2>' + render_form()
        if self.kind(page) in ('article', 'term', 'legal', 'case-detail') and ('reading-section' in classes or name.startswith('規約本文') or 'インタビュー本文' in name):
            layout += ' reading'
        if 'サマリー' in name:
            classes += ['case-summary']
        if name == 'メイン画像・企業名' and page['number'] == 22:
            slug = self.business(page)
            body = '<figure class="case-main-photo">' + self.image(f'/assets/images/top/{slug}.webp', '導入事例の業種イメージ') + '<figcaption>※サンプル事例・写真はイメージです。</figcaption></figure>' + render_items([item for item in items if item['type'] != '素材イメージ'], page)
        return f'<section class="{" ".join(classes)}" id="section-{index}" data-wire-section="{self.esc(name)}"><div class="{layout}">{body}</div></section>'

    def filters(self, section, page, old):
        return old.replace('class="container filters"', f'class="container filters" data-wire-section="{self.esc(section["name"])}" style="--filter-columns:{len(section["items"])}"')

    def table(self, source):
        headers = re.findall(r'<th\b[^>]*>(.*?)</th>', source.split('</thead>')[0], re.S)
        target = next((index for index, title in enumerate(headers) if 'Target-One' in html.unescape(title)), None)
        popular = next((index for index, title in enumerate(headers) if 'スタンダード' in html.unescape(title)), None)
        if popular is not None:
            source = source.replace('<table>', '<table class="plan-table">', 1)

        def row_style(match):
            row = match[0]
            cells = re.findall(r'<(?:th|td)\b[^>]*>(.*?)</(?:th|td)>', row, re.S)
            target_row = bool(cells and 'Target-One' in html.unescape(cells[0]))
            index = 0

            def cell_style(cell):
                nonlocal index
                cls = 'target-cell' if target_row or index == target else 'featured-plan' if index == popular else ''
                index += 1
                return cell[0][:-1] + (f' class="{cls}">' if cls else '>')

            return re.sub(r'<(?:th|td)\b[^>]*>', cell_style, row)

        return re.sub(r'<tr>.*?</tr>', row_style, source, flags=re.S)

    def common(self):
        return components.services()

    def company_link(self):
        return components.company()
