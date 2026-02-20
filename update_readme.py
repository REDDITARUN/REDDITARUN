import feedparser
import requests
import re
from datetime import datetime

README_FILE = "README.md"
SUBSTACK_FEED = "https://rsshub.app/substack/teendifferent"
MAX_POSTS = 5

def fetch_feed(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return feedparser.parse(response.content)

feed = fetch_feed(SUBSTACK_FEED)

posts = []

for entry in feed.entries[:MAX_POSTS]:
    published = entry.get("published_parsed")
    if published:
        date = datetime(*published[:6]).strftime("%b %d, %Y")
    else:
        date = ""
    posts.append(f"- [{entry.title}]({entry.link}) ({date})")

formatted_posts = "\n".join(posts)

with open(README_FILE, "r", encoding="utf-8") as f:
    content = f.read()

new_content = re.sub(
    r"<!-- BLOG-POST-LIST:START -->.*<!-- BLOG-POST-LIST:END -->",
    f"<!-- BLOG-POST-LIST:START -->\n{formatted_posts}\n<!-- BLOG-POST-LIST:END -->",
    content,
    flags=re.DOTALL
)

with open(README_FILE, "w", encoding="utf-8") as f:
    f.write(new_content)
