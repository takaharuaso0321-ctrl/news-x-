# x_client.py
import os, httpx, requests
from requests_oauthlib import OAuth1

X_API_BASE = "https://api.x.com/2"  # 互換で https://api.twitter.com/2 でもOK

class XClient:
    def __init__(self):
        # OAuth1.0a（ユーザーコンテキスト）
        self.api_key = os.getenv("X_API_KEY")
        self.api_secret = os.getenv("X_API_SECRET")
        self.access_token = os.getenv("X_OAUTH1_ACCESS_TOKEN")
        self.access_secret = os.getenv("X_OAUTH1_ACCESS_TOKEN_SECRET")

        if not all([self.api_key, self.api_secret, self.access_token, self.access_secret]):
            raise RuntimeError("OAuth1.0a credentials not set (X_API_KEY / X_API_SECRET / X_OAUTH1_ACCESS_TOKEN / X_OAUTH1_ACCESS_TOKEN_SECRET)")

        self.auth = OAuth1(self.api_key, self.api_secret, self.access_token, self.access_secret)

    def post_text(self, text: str):
        url = f"{X_API_BASE}/tweets"
        r = requests.post(url, auth=self.auth, json={"text": text}, timeout=30)
        if r.status_code >= 300:
            raise RuntimeError(f"X error {r.status_code}: {r.text}")
        return r.json()

