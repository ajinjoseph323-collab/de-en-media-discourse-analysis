"""
Day 2 script (v2) — Google News RSS version.
No API key needed, no daily limit. Gives much better English-language
coverage than NewsAPI's free tier for this kind of niche topic.

Requires: pip install feedparser pandas
"""

import feedparser
import pandas as pd
from urllib.parse import quote


def google_news_search(query, language, country, ceid, max_results=40):
    """
    Search Google News RSS for a query in a given language/country edition.
    language: 'en' or 'de' (used for our own labeling)
    hl / gl / ceid: Google's own locale codes for the edition to search
    """
    encoded_query = quote(query)
    url = (
        f"https://news.google.com/rss/search?q={encoded_query}"
        f"&hl={ceid.split(':')[1]}-{country}&gl={country}&ceid={ceid}"
    )

    feed = feedparser.parse(url)

    rows = []
    for entry in feed.entries[:max_results]:
        # Google News RSS often formats titles as "Headline - Source Name"
        title = entry.title
        source_name = getattr(entry, "source", {}).get("title", "Unknown")

        rows.append({
            "language": language,
            "source": source_name,
            "date": entry.get("published", ""),
            "title": title,
            "description": entry.get("summary", ""),
            "url": entry.link,
        })
    return rows


# 1. English search (US edition of Google News)
english_rows = google_news_search(
    query="skilled worker shortage Germany",
    language="en",
    country="US",
    ceid="US:en",
)

# 2. German search (Germany edition of Google News)
german_rows = google_news_search(
    query="Fachkräftemangel",
    language="de",
    country="DE",
    ceid="DE:de",
)

print(f"Collected {len(english_rows)} English articles.")
print(f"Collected {len(german_rows)} German articles.")

# 3. Combine into one table
df = pd.DataFrame(english_rows + german_rows)

# 4. Drop duplicate articles (same URL) and empty titles
df = df.drop_duplicates(subset="url")
df = df.dropna(subset=["title"])

print(f"\nFinal dataset size after cleanup: {len(df)} articles")
print(df["language"].value_counts())

# 5. Save to CSV — this is your Day 3-4 starting point
df.to_csv("raw_articles.csv", index=False)
print("\nSaved to raw_articles.csv")
