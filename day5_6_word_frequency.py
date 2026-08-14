"""
Day 5-6 script: Word frequency and framing comparison.

Compares which words dominate ENGLISH headlines vs. GERMAN headlines
about the same topic (skilled worker shortage). This is the core of
your discourse analysis — different word choices = different framing.

IMPORTANT: we analyze the ORIGINAL-language text (German headlines in
German, English headlines in English) — NOT the translated headline_en
column. Framing lives in the actual words each press chose, so
translating first would blur exactly what we're trying to compare.
The headline_en column is just there for YOUR reading comprehension.

Requires: pip install nltk matplotlib pandas
Run this in the same folder as your clean_articles.csv.
"""

import re
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

# ---------------------------------------------------------
# STEP 0: Make sure nltk's stopword lists are downloaded
# ---------------------------------------------------------
# This only actually downloads the first time you run it —
# after that it's cached locally and this line does nothing.
nltk.download("stopwords", quiet=True)

english_stopwords = set(stopwords.words("english"))
german_stopwords = set(stopwords.words("german"))

# Extra words to ignore ON TOP of the standard stopword lists —
# these are words that would dominate simply because they're part
# of our SEARCH QUERY, not because they're interesting framing choices.
# Feel free to add more here as you notice uninteresting words creeping
# into your top-15 list.
extra_stopwords_en = {"germany", "german", "shortage", "workers", "worker"}
extra_stopwords_de = {"fachkräftemangel", "arbeitskräftemangel", "deutschland",
                       "deutschlands"}


# ---------------------------------------------------------
# STEP 1: Load your cleaned data
# ---------------------------------------------------------
df = pd.read_csv("clean_articles.csv")
print(f"Loaded {len(df)} rows.\n")


# ---------------------------------------------------------
# STEP 2: Tokenize — turn each headline into a list of clean words
# ---------------------------------------------------------
def tokenize(text, stopword_set):
    """
    Takes one headline string, returns a list of meaningful lowercase words.
    - re.findall(...) pulls out only letter sequences (including German
      umlauts/ß), ignoring punctuation, numbers, and symbols.
    - We lowercase everything so 'Germany' and 'germany' count as the same word.
    - We then throw away anything in the stopword set (filler words).
    """
    words = re.findall(r"[a-zA-ZäöüÄÖÜß]+", text.lower())
    return [w for w in words if w not in stopword_set and len(w) > 2]


# Build one big list of words for each language
english_words = []
german_words = []

for _, row in df.iterrows():
    if row["language"] == "en":
        combined_stopwords = english_stopwords | extra_stopwords_en
        english_words.extend(tokenize(row["headline"], combined_stopwords))
    else:
        combined_stopwords = german_stopwords | extra_stopwords_de
        german_words.extend(tokenize(row["headline"], combined_stopwords))

print(f"Collected {len(english_words)} English words and "
      f"{len(german_words)} German words after removing stopwords.\n")


# ---------------------------------------------------------
# STEP 3: Count frequency per language
# ---------------------------------------------------------
english_counts = Counter(english_words)
german_counts = Counter(german_words)

top_english = english_counts.most_common(15)
top_german = german_counts.most_common(15)

print("=" * 50)
print("TOP 15 ENGLISH WORDS")
print("=" * 50)
for word, count in top_english:
    print(f"  {word:<20} {count}")

print("\n" + "=" * 50)
print("TOP 15 GERMAN WORDS")
print("=" * 50)
for word, count in top_german:
    print(f"  {word:<20} {count}")


# ---------------------------------------------------------
# STEP 4: Save full frequency tables to CSV
# ---------------------------------------------------------
freq_rows = []
for word, count in english_counts.most_common():
    freq_rows.append({"language": "en", "word": word, "count": count})
for word, count in german_counts.most_common():
    freq_rows.append({"language": "de", "word": word, "count": count})

freq_df = pd.DataFrame(freq_rows)
freq_df.to_csv("word_frequencies.csv", index=False, encoding="utf-8-sig")
print("\nSaved full frequency table to word_frequencies.csv")


# ---------------------------------------------------------
# STEP 5: Quick side-by-side bar chart of top 10 words each
# ---------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

en_words_top10, en_counts_top10 = zip(*english_counts.most_common(10))
axes[0].barh(en_words_top10[::-1], en_counts_top10[::-1], color="#4472C4")
axes[0].set_title("Top 10 English Words")

de_words_top10, de_counts_top10 = zip(*german_counts.most_common(10))
axes[1].barh(de_words_top10[::-1], de_counts_top10[::-1], color="#C00000")
axes[1].set_title("Top 10 German Words")

plt.tight_layout()
plt.savefig("word_frequency_chart.png", dpi=150)
print("Saved chart to word_frequency_chart.png")
print("\nDone! Open word_frequencies.csv and word_frequency_chart.png to review.")
