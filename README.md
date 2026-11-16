# Target-One 先方確認用

- `main`：先方確認用。TOP以外の本文は「これから作成予定です。」と表示します。
- `develop`：全59ページ・WordPressテーマ・参考資料・納品ZIPを保持する作業ブランチ。通常の制作はこのブランチで行います。
- 確認URL：https://akinai-user.github.io/Target-One-preview/

元リポジトリは非公開です。現在のGitHubプランでは非公開リポジトリのPagesを利用できないため、確認用の公開リポジトリ `akinai-user/Target-One-preview` に必要な静的ファイルだけを配置しています。先方確認URLは誰でも閲覧できるURLで、検索除外設定を加えています。

## 確認用ファイルの書き出し

`main` で次を実行してください。出力先はリポジトリ外の空のディレクトリを指定します。

```sh
python3 scripts/build_preview.py --output /tmp/target-one-preview-export
```

出力するのはTOP・準備中ページ・共通アセット・robots.txt・404ページのみです。PHP、参考資料、コンテンツJSON、WordPressテーマ、納品ZIPは公開しません。GitHub PagesのプロジェクトURLに合わせてリンクを補正します。

書き出したファイルを確認用公開リポジトリの `main` にコミット・プッシュするとGitHub Pagesに反映されます。非公開リポジトリからの自動同期は設定していません。

`main` で `scripts/build.py` を実行すると下層の本文が再生成されるため、制作・再生成は `develop` で行ってください。
