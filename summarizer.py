# summarizer.py  ——— ローカル Llama 3（Ollama）版
import os
import httpx

SYSTEM = (
    "あなたはジャーナリストです。"
    "X（旧Twitter）向けに日本語で要約します。"
    "制約: 280字以内 / 絵文字なし / 出典URLを文末に1つ（URLだけ） / 主語と時制を明確に / "
    "ハッシュタグは重要語に1〜2個のみ。"
)

PROMPT = """

次のテキストをもとに、X向けの投稿文を生成してください。条件は以下の通りです。

- 280字以内にしてください。
- 冒頭にタイトルを書いてください。(plain_textで出力、装飾なし)
- 改行して、その後に内容を簡潔に要約してください。
- 文末には出典URLを1つのみ記載してください(”出典"は書かず、URLだけ　https://〜）
- 驚き・疑問・緊急性の要素を盛り込んでください。

出力は投稿文のみを書いてください。前置きや説明は不要です。


記事タイトル: {title}

URL: {url}

本文（必要なら抜粋で可）:
{body}
"""

DEFAULT_OLLAMA_MODEL = "elyza-llama3-8b"

def summarize_for_x(title: str, url: str, body: str) -> str:
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
    max_chars = int(os.getenv("MAX_POST_CHARS", "280"))

    # Llamaは「システム」「ユーザー」的な区別が弱いので、SYSTEMを前置きする
    prompt = f"{SYSTEM}\n\n" + PROMPT.format(
        title=title.strip(),
        url=url.strip(),
        body=(body or "").strip()[:8000]
    )

    # Ollama generate API（stream=Falseで一括レスポンス）
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 220  # 余裕を見て、後でカット
        }
    }

    try:
        with httpx.Client(timeout=60) as client:
            r = client.post(f"{host}/api/generate", json=payload)
    except Exception as e:
        raise RuntimeError(f"Ollama connection error: {e}")

    if r.status_code >= 300:
        raise RuntimeError(f"Ollama HTTP {r.status_code}: {r.text}")

    data = r.json()
    # 期待キー: {"response": "...", "done": true, ...}
    text = (data or {}).get("response")
    if not text:
        raise RuntimeError(f"Ollama returned no text: {data}")

    text = text.strip()
    if len(text) > max_chars:
        text = text[: max_chars - 1] + "…"
    return text


