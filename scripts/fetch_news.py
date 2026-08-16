"""
매일 자동으로 실행되어 뉴스를 가져오는 스크립트입니다.
(This runs automatically once a day via GitHub Actions —
no need to run it yourself.)

It fetches real headlines from ABC News Australia (local) and
BBC World News (world), and saves them to news.json, which the
dashboard reads directly — no API key, no live browser fetch,
no login required.
"""
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

LOCAL_FEED = "https://www.abc.net.au/news/feed/51120/rss.xml"   # ABC News Australia — Just In
WORLD_FEED = "https://feeds.bbci.co.uk/news/world/rss.xml"       # BBC World News


def fetch_titles(url, count=3):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = resp.read()
    root = ET.fromstring(data)
    titles = []
    for item in root.iter("item"):
        title_el = item.find("title")
        if title_el is not None and title_el.text:
            titles.append(title_el.text.strip())
        if len(titles) >= count:
            break
    return titles


def main():
    try:
        local = fetch_titles(LOCAL_FEED, 3)
    except Exception:
        local = []
    try:
        world = fetch_titles(WORLD_FEED, 3)
    except Exception:
        world = []

    sydney_time = datetime.now(timezone(timedelta(hours=10))).strftime("%Y-%m-%d %H:%M")
    data = {"updated": sydney_time, "local": local, "world": world}

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Saved news.json:", data)


if __name__ == "__main__":
    main()
