# Target-One サービスサイト

## GitHub Pages公開

- 公開URL：https://akinai-user.github.io/Target-One/
- `main` へのプッシュで `.github/workflows/pages.yml` が現在の全59ページを自動公開します。
- GitHubのリポジトリ設定で、PagesのSourceは「GitHub Actions」を使用します。
- `develop` で修正・確認し、`main` へのマージ後にGitHub Pagesへ公開します。
- `Target-One-preview` への配置・同期は行いません。

`python3 scripts/build_github_pages.py --output dist` で公開ファイルを書き出せます。
`/Target-One/` に合わせて内部リンク・画像・CSS・JS・サイトマップのURLを変換します。
公開ファイルには静的HTML・アセットのみを含め、PHP・参考資料・WordPress版・納品ZIPは含めません。
リポジトリ自体は公開のため、これらのソースとGit履歴はGitHub上で閲覧できます。
GitHub PagesではPHPが動かないため、問い合わせ・資料請求フォームは送信停止のままです。

共有Excelの39ページをベースに作成した、HTML・CSS・JavaScript中心のサイトです。TOPはこのフォルダ直下の `index.html`、下層ページは各ディレクトリの `index.html` です。お問い合わせはA案を採用しています。

事例詳細6業種・コラム詳細・用語詳細・コラムカテゴリ4ページ・サンクスページを補完し、静的版は全59ページです。ページ一覧は `PAGE-LIST.md` をご覧ください。

## 確認方法

このフォルダで以下を実行し、 http://localhost:8080/ をブラウザーで開いてください。

```sh
python3 -m http.server 8080
```

ルート相対URLを採用しているため、HTMLファイルの直接ダブルクリックではなく、HTTPサーバー経由で確認します。Nodeやnpmのインストール、ビルドは不要です。

## 納品ファイル

- `target-one-static.zip`：Xサーバーの公開ルートに配置する静的版。API以外はHTML/CSS/JSです。
- `target-one-wordpress-theme.zip`：社内で記事・事例を更新するためのWordPressテーマ。
- `content/pages.json`：元ワイヤーのページ別コンテンツ。見出し・説明文・各セクションの編集元。
- `scripts/build.py`：静的HTMLとサイトマップの再生成スクリプト（Python標準ライブラリのみ）。

## 静的版をXサーバーに配置する

1. `target-one-static.zip` を展開し、中身を `target-one.net` の `public_html` に配置します。既存サイトがある場合はバックアップを取り、検証用環境で先にご確認ください。
2. 常時SSLを有効にします。canonical・OGP・サイトマップは `https://target-one.net/` を前提にしています。
3. `api/config.php` の `recipient` と `from` に、利用するメールアドレスを設定します。`from` はXサーバーで送信可能な自社ドメインのメールアドレスをご指定ください。
4. 受付開始時にPHP側の `enabled` と `assets/js/config.js` の `formEnabled` を、両方 `true` に変更します。
5. テスト送信し、担当者宛のメール到達を確認します。資料請求も担当者への通知で、PDFの自動送付は行いません。

フォームはHTML標準の入力チェック、確認ダイアログ、PHPでの再検証、CSRFトークン、セッション内の送信間隔制限、ハニーポットを実装しています。送信成功時のみサンクスページへ進みます。初期状態は受付停止で、確認画面までは操作可能です。reCAPTCHAは未接続です。

希望日は日本時間で3営業日以降、土日祝を除く日を選択できます。祝日データは2026〜2030年分です。祝日法改正や2031年以降に合わせて `api/holidays.json` と `assets/js/config.js` の配列を更新してください。

## WordPressで社内更新する場合

静的版とWordPress版は、同じ公開ルートに重ねず、どちらかを選んで使用します。WordPress版でもHTML/CSS/JSのデザインを利用します。

1. Xサーバー上のドメイン直下にWordPressを用意します。まずは検索エンジンへの表示を抑止した検証環境で作業してください。
2. 管理画面の「外観 → テーマ → 新規追加 → テーマのアップロード」から `target-one-wordpress-theme.zip` をアップロードして有効化します。PHP 8.0以上を使用してください。
3. 初回の有効化時に、ワイヤーに対応する固定ページ・サンプル事例・サンプルコラムを読み込みます。既存の同一URLページは上書きしません。テーマはドメイン直下での運用を前提とします。
4. 管理画面の「コラム」「導入事例」から新規追加・更新できます。タイトル・本文・抜粋・アイキャッチ・カテゴリ（事例は業種）・著者・SEOタイトル・descriptionを設定できます。新規記事はWordPressの標準エディタで編集できます。
5. 初期の固定ページとサンプル詳細は、ワイヤーの構成を保つ「カスタムHTML」ブロックです。本文HTMLを編集できます。公開前に仮文言・サンプルデータを差し替えてください。
6. 公開ルートに静的版の `api` ディレクトリを配置し、送信設定を行います。テーマ内 `assets/js/config.js` も設定してください。
7. 投稿更新時のXMLサイトマップはWordPress標準の `/wp-sitemap.xml` を使用します。静的版の `sitemap.xml` を併用する必要はありません。

WordPress版はテーマ内でOrganization・Article・BreadcrumbList・FAQPageの構造化データを生成します。SEOプラグインを追加する場合は、canonical・OGP・構造化データが二重出力されないよう出力設定を調整してください。

## 計測・Search Console

- `assets/js/config.js` の `gtmId` に実際のGTMコンテナIDを設定します。GTMを使わない場合は `ga4Id` を設定できます。両方設定した場合はGTMのみを読み込み、二重計測を避けます。
- 問い合わせ成功時は、個人情報を含めず `lead_complete` イベントと `lead_type` をdataLayerに送ります。GTM側のタグ・コンバージョン定義は実アカウントで設定してください。
- Search ConsoleはDNS認証またはHTMLメタ認証で所有権を確認してください。静的版では `content/site-config.json` の `searchConsoleVerification` に確認コード（content値）を入れて `python3 scripts/build.py` を実行します。WordPress版は「外観 → カスタマイズ → Target-One設定」に設定欄があります。
- GA4/GTM・Search ConsoleのIDやアカウント情報は未共有のため、実アカウントへの接続は未実施です。

## コンテンツの更新と再生成

```sh
python3 scripts/build.py
python3 scripts/check.py
```

`content/pages.json` を編集すると、title・description・h1・本文・表・FAQを再生成できます。コラム／事例を日常的に管理画面から更新する場合は、WordPress版を選んでください。

共通スタイルは `assets/css/style.css`、共通操作は `assets/js/main.js` です。 下層ページの共通デザインは `assets/css/pages.css`、共通アニメーションは `assets/css/top-motion.css` と `assets/js/top-motion.js` です。`/guide/` の本文は `content/guide-main.html`、専用スタイルは `assets/css/guide.css` で管理し、生成時にも維持します。ボタン・リンク・濃紺の背景はTOPの共通クラスを使用します。ソース編集後の再梱包は `python3 scripts/package_delivery.py` で行えます。静的HTMLに直接加えた修正は、再生成時に上書きされるため、継続編集はJSONと生成スクリプト側へ反映してください。

## 確認済み・未確認事項

- 59ページについて、内部リンク・画像・CSS/JS参照・ページ内アンカー・h1が1つであること・title/description・JSON-LD構文を検査済み。
- JavaScriptとPHPの構文を確認済み。受付停止時のPHP応答を確認済み。
- ブラウザー接続が利用できず、Chromeへのコンピューター操作も許可されなかったため、実ブラウザーでのPC/SP表示・操作検証、Core Web Vitals測定は未実施。
- WordPressは未設置のため、テーマの有効化・記事更新・実メール到達は未検証。
- ロゴの原本・営業資料PDFはZIPに含まれていませんでした。ロゴはテキスト組み、画面・表紙・地図・メンバー素材は共有されたイメージ画像を使用しています。
- 実績数値・事例・記事・会社情報・規約の仮表記は原資料に沿って保持しています。追加した事例もサンプルです。利用規約の確定本文、実在する事例、制作事例、PDFの実データは公開前に差し替える必要があります。
- 本文や料金表・比較表はHTMLで記載し、スライド画像で置き換えていません。素材はWebP化・遅延読み込み、動きを減らす設定にも対応しています。

参考サイトは構成の確認のみに使用し、デザイン・文章は流用していません。

## Prettierによる整形

PHP・XML用プラグインを含めて設定済みです。

```sh
npm ci
npm run format
npm run format:check
```

静的ページを再生成した場合も `npm run format` を実行してください。画像・ZIP・Excelなどのバイナリ、Prettier非対応のPython・プレーンテキストは整形対象外です。
