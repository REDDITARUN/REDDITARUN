import feedparser
import requests
import re

README_FILE = "README.md"
MAX_POSTS = 5

feeds = [
    "https://teendifferent.substack.com/feed",
    "https://medium.com/feed/@teendifferent"
]

def fetch_feed(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    return feedparser.parse(response.content)

posts = []

for feed_url in feeds:
    feed = fetch_feed(feed_url)
    for entry in feed.entries[:MAX_POSTS]:
        posts.append((entry.published_parsed, entry.title, entry.link))

# Sort newest first
posts.sort(reverse=True)

# Take top MAX_POSTS
posts = posts[:MAX_POSTS]

formatted_posts = ""
for _, title, link in posts:
    formatted_posts += f"- [{title}]({link})\n"

with open(README_FILE, "r", encoding="utf-8") as f:
    content = f.read()

new_content = re.sub(
    r"<!-- BLOG-POST-LIST:START -->.*<!-- BLOG-POST-LIST:END -->",
    f"<!-- BLOG-POST-LIST:START -->\n{formatted_posts}<!-- BLOG-POST-LIST:END -->",
    content,
    flags=re.DOTALL
)

with open(README_FILE, "w", encoding="utf-8") as f:
    f.write(new_content)
