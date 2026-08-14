"""
Day 7-8 script: Multilingual sentiment scoring.

Scores every headline (in its ORIGINAL language) on a 1-5 star scale
using ONE model that understands both English and German. Using the
same model for both languages matters: it means any sentiment
difference we find is a real framing difference, not just an artifact
of using two different tools.

First run will download the model (~700MB) — this only happens once,
future runs reuse the cached copy and start instantly.

Requires: pip install transformers torch pandas matplotlib
Run this in the same folder as your clean_articles.csv.
"""

import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline

# ---------------------------------------------------------
# STEP 1: Load your cleaned data
# ---------------------------------------------------------
df = pd.read_csv("clean_articles.csv")
print(f"Loaded {len(df)} rows.\n")


# ---------------------------------------------------------
# STEP 2: Load the multilingual sentiment model
# ---------------------------------------------------------
# This may take a minute or two the very first time — it's downloading
# the model. After that, it loads from your local cache almost instantly.
print("Loading sentiment model (first run downloads it, please wait)...")
sentiment_model = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment",
)
print("Model loaded.\n")


# ---------------------------------------------------------
# STEP 3: Score every headline
# ---------------------------------------------------------
def score_headline(text):
    """
    Runs one headline through the model.
    Returns (stars, centered_score, confidence).

    The model outputs a label like '4 stars' with a confidence score.
    We convert stars (1-5) into a -1 to +1 scale, where:
      1 star  -> -1.0  (very negative)
      3 stars ->  0.0  (neutral)
      5 stars -> +1.0  (very positive)
    This makes it easy to average and compare across languages.
    """
    result = sentiment_model(text[:512])[0]  # [:512] = safety limit on text length
    stars = int(result["label"][0])          # e.g. "4 stars" -> 4
    confidence = result["score"]
    centered_score = (stars - 3) / 2
    return stars, centered_score, confidence


stars_list = []
score_list = []
confidence_list = []

for i, row in df.iterrows():
    stars, score, confidence = score_headline(row["headline"])
    stars_list.append(stars)
    score_list.append(score)
    confidence_list.append(confidence)
    if (i + 1) % 10 == 0 or (i + 1) == len(df):
        print(f"Scored {i + 1}/{len(df)} headlines...")

df["sentiment_stars"] = stars_list
df["sentiment_score"] = score_list
df["sentiment_confidence"] = confidence_list


# ---------------------------------------------------------
# STEP 4: Compare average sentiment by language
# ---------------------------------------------------------
avg_by_language = df.groupby("language")["sentiment_score"].mean()

print("\n" + "=" * 50)
print("AVERAGE SENTIMENT SCORE BY LANGUAGE  (-1 = negative, +1 = positive)")
print("=" * 50)
for lang, avg_score in avg_by_language.items():
    label = "English" if lang == "en" else "German"
    print(f"  {label:<10} {avg_score:+.3f}")


# ---------------------------------------------------------
# STEP 5: Save results
# ---------------------------------------------------------
df.to_csv("sentiment_results.csv", index=False, encoding="utf-8-sig")
print("\nSaved full per-article results to sentiment_results.csv")

fig, ax = plt.subplots(figsize=(6, 5))
labels = ["English" if l == "en" else "German" for l in avg_by_language.index]
colors = ["#4472C4" if l == "en" else "#C00000" for l in avg_by_language.index]
ax.bar(labels, avg_by_language.values, color=colors)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_ylabel("Average sentiment score (-1 to +1)")
ax.set_title("Average Headline Sentiment by Language")
plt.tight_layout()
plt.savefig("sentiment_by_language.png", dpi=150)
print("Saved chart to sentiment_by_language.png")

print("\nDone! Open sentiment_results.csv and sentiment_by_language.png to review.")
