"""Shared lower-page UI, used by /guide/ and the generated pages alike."""
from html import escape


def buttons(secondary='資料請求', secondary_url='/request/', white=False):
    variant = 'top-button-white' if white else 'top-button-outline'
    return ('<div class="buttons">'
            '<a class="top-button top-button-orange" href="/contact/">無料相談を申し込む</a>'
            f'<a class="top-button {variant}" href="{escape(secondary_url, quote=True)}">{escape(secondary)}</a>'
            '</div>')


def hero(breadcrumb, eyebrow, title, lead, actions='', media='', guide=False):
    extra = ' guide-hero guide-blue' if guide else ' page-hero'
    copy = ' guide-hero-copy' if guide else ' page-hero-copy'
    title_id = 'guide-title' if guide else 'page-title'
    if not guide:
        title = f'<span class="shared-hero-title-accent">{title}</span>'
    return (f'<section class="shared-hero top-dark{extra}" aria-labelledby="{title_id}">'
            f'<div class="container">{breadcrumb}'
            f'<p class="shared-hero-eyebrow">{eyebrow}</p>'
            f'<div class="shared-hero-copy{copy}"><h1 id="{title_id}">{title}</h1>'
            f'<p class="shared-hero-lead">{lead}</p>{actions}</div>'
            + (f'<div class="shared-hero-media">{media}</div>' if media else '')
            + '</div></section>')


def services():
    items = [
        ('service-url', '<span class="shared-phrase">指定URL</span><span class="shared-phrase">ターゲティング広告とは</span>', '競合サイトの訪問者に広告を届ける仕組み', '/guide/'),
        ('service-delivery', 'サービス紹介', 'URL指定、エリア指定、効果測定など', '/service/'),
        ('service-plan', '料金プラン', '月額18,000円から', '/plan/'),
    ]
    cards = ''.join(
        f'<a class="shared-service-card" href="{url}">'
        f'<img src="/assets/images/guide/{asset}.png" alt="" width="130" height="80" loading="lazy" decoding="async">'
        f'<h3>{title}</h3><p>{description}</p>'
        '<span class="top-link">詳しく見る <span aria-hidden="true">→</span></span></a>'
        for asset, title, description, url in items)
    return ('<section class="section shared-service"><div class="container">'
            '<p class="eyebrow">SERVICE</p><h2>Target-Oneでできること</h2>'
            f'<div class="shared-service-grid">{cards}</div></div></section>')


def contact():
    return ('<section class="section shared-contact top-dark"><div class="container">'
            '<h2>まずは<span class="cta-accent">無料相談</span>から</h2>'
            '<p>商圏・業種に応じた具体的なご提案をお伝えします。<br>お問い合わせには24時間以内に対応します。</p>'
            + buttons()
            + '<p class="shared-contact-address"><span>お電話：<a href="tel:05017802231">050-1780-2231</a></span>'
            '　<span>メール：<a href="mailto:info@target-one.net">info@target-one.net</a></span></p>'
            '</div></section>')


def company():
    return ('<div class="shared-company"><div class="container">'
            '<h2><span class="shared-phrase">Target-Oneを運営する</span><span class="shared-phrase">会社について</span></h2>'
            '<a class="top-link" href="/company/">運営会社を見る <span aria-hidden="true">→</span></a>'
            '</div></div>')
