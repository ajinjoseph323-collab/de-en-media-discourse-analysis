"""
Adds a 'headline_en' column to clean_articles.csv.

- For English articles, headline_en is just a copy of the original headline.
- For German articles, headline_en is a machine translation, so you can
  read and understand every row even without being fluent in German.

This uses Google Translate under the hood via the deep-translator package
(free, no API key needed for this volume of text).

Requires: pip install deep-translator pandas
Run this in the same folder as your clean_articles.csv.
"""

import time
import pandas as pd
from deep_translator import GoogleTranslator

# ---------------------------------------------------------
# STEP 1: Load your cleaned data
# ---------------------------------------------------------
df = pd.read_csv("clean_articles.csv")
print(f"Loaded {len(df)} rows.")

# Set up the translator once, German -> English
translator = GoogleTranslator(source="de", target="en")


def translate_headline(row):
    """
    For English rows: just return the headline unchanged.
    For German rows: translate it to English.
    If a translation fails for any reason (e.g. a weird character),
    we don't want the whole script to crash — we just fall back to
    the original German text and print a warning.
    """
    if row["language"] == "en":
        return row["headline"]

    try:
        translated = translator.translate(row["headline"])
        return translated
    except Exception as e:
        print(f"  Could not translate: {row['headline'][:50]}...  ({e})")
        return row["headline"]  # fallback: keep original German


# ---------------------------------------------------------
# STEP 2: Translate row by row
# ---------------------------------------------------------
# We loop manually (instead of using .apply directly) so we can print
# progress and add a tiny pause between requests — this avoids
# overloading the free translation service.

translations = []
total = len(df)

for i, row in df.iterrows():
    translations.append(translate_headline(row))
    if (i + 1) % 10 == 0 or (i + 1) == total:
        print(f"Translated {i + 1}/{total} rows...")
    time.sleep(0.3)  # small pause between requests, be polite to the free service

df["headline_en"] = translations

# ---------------------------------------------------------
# STEP 3: Reorder columns so headline_en sits right next to headline
# ---------------------------------------------------------
column_order = ["language", "source", "date", "headline", "headline_en",
                 "description", "url"]
df = df[column_order]

# ---------------------------------------------------------
# STEP 4: Save — with utf-8-sig so Excel displays everything correctly
# ---------------------------------------------------------
df.to_csv("clean_articles.csv", index=False, encoding="utf-8-sig")

print("\nDone! headline_en column added and saved to clean_articles.csv")
print("Open it in Excel — you should now see every headline in English,")
print("right next to the original.")
