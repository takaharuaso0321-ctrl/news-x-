# app.py（先頭）
import os, sys
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv(usecwd=True)) # override=False なら上書きしない

# スクリプトのあるディレクトリを基準にする
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)  # ← どこから実行してもプロジェクト直下がCWDになる

# .env を確実に読む
DOTENV_PATH = os.path.join(BASE_DIR, ".env")

os.environ.pop("OLLAMA_MODEL", None)
os.environ["OLLAMA_MODEL"] = "llama3" 

from summarizer import summarize_for_x
from x_client import XClient
import sqlite3


import feedparser, yaml, httpx
from bs4 import BeautifulSoup
from summarizer import summarize_for_x
from x_client import XClient

DB_PATH = os.path.join(os.path.dirname(__file__), "db.sqlite3")

def ensure_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS posted(url TEXT PRIMARY KEY, posted_at INTEGER)")
    con.commit(); con.close()

def already_posted(url):
    con = sqlite3.connect(DB_PATH); cur = con.cursor()
    cur.execute("SELECT 1 FROM posted WHERE url=?", (url,))
    row = cur.fetchone(); con.close()
    return row is not None

def mark_posted(url):
    con = sqlite3.connect(DB_PATH); cur = con.cursor()
    cur.execute("INSERT OR REPLACE INTO posted(url, posted_at) VALUES(?, strftime('%s','now'))", (url,))
    con.commit(); con.close()

def clean_text(html):
    soup = BeautifulSoup(html or "", "lxml")
    for t in soup(["script","style","noscript"]): t.extract()
    return " ".join(soup.get_text(" ").split())

def fetch_article_body(url):
    try:
        with httpx.Client(timeout=20, follow_redirects=True) as client:
            r = client.get(url)
        if r.status_code>=300: return ""
        soup = BeautifulSoup(r.text,"lxml")
        for sel in ["article","div#main","div.article-body","div.entry-content","section.article","main"]:
            node=soup.select_one(sel)
            if node and len(node.get_text())>200:
                return node.get_text(" ")[:12000]
        return clean_text(r.text)[:12000]
    except Exception: return ""

def pick_feed_items():
    with open(os.path.join(os.path.dirname(__file__),"sources.yaml"),encoding="utf-8") as f:
        feeds=yaml.safe_load(f).get("feeds",[])
    items=[]
    for url in feeds:
        try:
            fp=feedparser.parse(url)
            for e in fp.entries[:5]:
                items.append({"title":e.get("title",""),"link":e.get("link",""),"summary":e.get("summary","")})
        except Exception: pass
    return items

def main():
    ensure_db(); client=XClient()
    for it in pick_feed_items():
        url=it["link"]
        if not url or already_posted(url): continue
        body=fetch_article_body(url) or it["summary"]
        try:
            text = summarize_for_x(it["title"], url, body)
        except Exception as e:
            print("Summarize failed:", e)
            continue

        resp=client.post_text(text); print("Posted:",resp)
        mark_posted(url)

        break

if __name__=="__main__": main()
