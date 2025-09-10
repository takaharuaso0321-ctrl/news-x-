
# News → OpenAI Summary → Post to X

シンプルな自動化ツール：
- RSSからニュース見出しを取得
- 本文を取得（取得できないときは要約対象を見出し＋説明にフォールバック）
- OpenAI Responses APIで日本語のX向け要約（原文リンク付き・280字以内）を生成
- X API (v2 `POST /2/tweets`) に投稿

> **注意**: XのAPIキー権限とアクセスレベル（`tweet.write` 含む）が必要です。

## 使い方 (ローカル)

1. 依存関係のインストール
```bash
pip install -r requirements.txt
```

2. 設定ファイル `.env` を作成（`config.example.env` をコピーして値を入れる）

3. フィードの編集（任意）: `sources.yaml` にRSS/AtomのURLを追記

4. 実行
```bash
python app.py
```
