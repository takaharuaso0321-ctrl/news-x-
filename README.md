# 📰 News to X Bot

ニュース記事を自動で取得し、要約して **X（旧Twitter）** に投稿するシンプルな自動化ツールです。

---

## ✨ 機能

- `sources.yaml` に登録した **RSS/Atom フィード** からニュースを取得
- 記事本文をスクレイピング（取得できない場合は見出し＋説明を要約対象にフォールバック）
- **OpenAI API** を利用して、日本語で **X 向け要約（280字以内／出典URL付き）** を生成
- **X API (v2 `POST /2/tweets`)** を利用して自動投稿
- 投稿済み記事は **SQLite データベース** に記録して重複投稿を防止

---

## 🚀 セットアップ（ローカル）

1. 依存パッケージをインストール
   ```bash
   pip install -r requirements.txt
   ```

2. 環境変数を設定  
   `.env` ファイルを作成し、以下の値を設定します（`config.example.env` をコピーすると便利です）。

   - `OPENAI_API_KEY`
   - `X_API_KEY`, `X_API_SECRET`
   - `X_OAUTH1_ACCESS_TOKEN`, `X_OAUTH1_ACCESS_TOKEN_SECRET`

   > **注意**: X 側で `tweet.write` 権限が必要です。

3. ニュースソースを編集（任意）  
   `sources.yaml` に RSS/Atom フィード URL を追加できます。
   ```yaml
   feeds:
     - https://news.yahoo.co.jp/rss/topics/top-picks.xml
     - https://rss.asahi.com/rss/asahi/newsheadlines.rdf
     - https://www3.nhk.or.jp/rss/news/cat0.xml
     - https://www.theverge.com/rss/index.xml
     - https://feeds.bbci.co.uk/news/world/rss.xml
   ```

4. 実行
   ```bash
   python app.py
   ```

---

## 📦 主な依存ライブラリ

- [httpx](https://www.python-httpx.org/) – HTTP クライアント
- [feedparser](https://pypi.org/project/feedparser/) – RSS/Atom フィード解析
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) + [lxml](https://lxml.de/) – HTML パース
- [python-dotenv](https://pypi.org/project/python-dotenv/) – 環境変数管理
- [sqlite-utils](https://sqlite-utils.datasette.io/) – SQLite 操作
- [requests-oauthlib](https://requests-oauthlib.readthedocs.io/) – OAuth 認証
- [openai](https://pypi.org/project/openai/) – 要約生成

---

## 🛠️ 拡張ポイント

- **フィード追加**: `sources.yaml` を編集
- **要約スタイル変更**: `summarizer.py` 内のプロンプトを調整
- **投稿先変更**: `x_client.py` を修正すれば Mastodon など他サービスにも応用可能
- **スケジューリング**: cron や GitHub Actions で定期実行すれば完全自動化

---

## ⚠️ 注意

- X API を利用するためには **開発者アカウントと適切なアクセスレベル**（特に `tweet.write`）が必要です。
- 公開記事の本文をスクレイピングするため、利用先のメディアの利用規約に従ってください。
