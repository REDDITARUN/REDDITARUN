import requests
import re
from datetime import datetime

README_FILE = "README.md"
SUBSTACK_API = "https://teendifferent.substack.com/api/v1/archive"
MAX_POSTS = 5

response = requests.get(SUBSTACK_API)
response.raise_for_status()
data = response.json()

posts = []

for post in data[:MAX_POSTS]:
    title = post["title"]
    slug = post["slug"]
    date = datetime.fromisoformat(post["post_date"]).strftime("%b %d, %Y")
    link = f"https://teendifferent.substack.com/p/{slug}"
    posts.append(f"- [{title}]({link}) ({date})")

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
