"""
Day 3-4 script: Cleaning your raw_articles.csv

WHAT THIS SCRIPT DOES, IN PLAIN ENGLISH:
1. Opens the raw_articles.csv file you created in Day 2.
2. Splits each messy title like "Headline - Source Name" into two
   separate, clean columns.
3. Fixes the date column so it's a proper date Python understands
   (right now it's just a long messy piece of text).
4. Removes any duplicate rows and any rows missing a title.
5. Saves everything into a new file called clean_articles.csv,
   WITHOUT touching or overwriting your original raw_articles.csv.

You don't need to understand every single line perfectly yet —
just run it, look at the printed output, and open clean_articles.csv
afterward to see what changed. Comments starting with # explain
what's happening above them.

Requires: pip install pandas
(you should already have this installed from Day 2)
"""

import pandas as pd

# ---------------------------------------------------------
# STEP 1: Load your raw data
# ---------------------------------------------------------
# pd.read_csv() opens a CSV file and turns it into a "DataFrame" —
# think of a DataFrame as an Excel spreadsheet, but living inside Python.
df = pd.read_csv("raw_articles.csv")

print(f"Loaded {len(df)} rows from raw_articles.csv")
print("Here's a preview of the first 3 rows:\n")
print(df.head(3))
print("\n" + "=" * 60 + "\n")


# ---------------------------------------------------------
# STEP 2: Split "Headline - Source Name" into two clean columns
# ---------------------------------------------------------
# Google News titles often look like:  "Germany faces worker gap - Reuters"
# We want to split that into:
#   headline = "Germany faces worker gap"
#   source_clean = "Reuters"
#
# The way we do this: look for the LAST " - " in the title (some headlines
# themselves contain dashes, so splitting on the last one is safer),
# and cut the text into two pieces there.

def split_title_source(title):
    """Takes one title string, returns (headline, source) as a pair."""
    if " - " in title:
        # rsplit with maxsplit=1 splits from the RIGHT, only once.
        # Example: "A - B - C".rsplit(" - ", 1) -> ["A - B", "C"]
        headline, source = title.rsplit(" - ", 1)
        return headline.strip(), source.strip()
    else:
        # If there's no " - " at all, just keep the whole thing as
        # the headline and mark the source as unknown.
        return title.strip(), "Unknown"


# .apply() runs our function on every single row in the "title" column.
# The result is a list of (headline, source) pairs, which we then
# unpack into two brand-new columns.
split_results = df["title"].apply(split_title_source)
df["headline"] = split_results.apply(lambda pair: pair[0])
df["source_clean"] = split_results.apply(lambda pair: pair[1])

print("Split titles into 'headline' and 'source_clean' columns.")
print(df[["headline", "source_clean"]].head(3))
print("\n" + "=" * 60 + "\n")


# ---------------------------------------------------------
# STEP 3: Fix the date column
# ---------------------------------------------------------
# Right now, "date" is just text, like: "Tue, 12 Aug 2026 09:15:00 GMT"
# Python doesn't know that's a date yet — to Python it's just a sentence!
# pd.to_datetime() converts it into a real date/time value, which lets
# us sort by date, filter by month, make timeline charts, etc. later.

df["date_clean"] = pd.to_datetime(df["date"], errors="coerce")
# errors="coerce" means: if any row's date is broken/unreadable,
# just turn it into a blank (NaT) instead of crashing the whole script.

# How many dates failed to convert? Good to know.
missing_dates = df["date_clean"].isna().sum()
print(f"Converted date column. {missing_dates} row(s) had unreadable dates.")
print("\n" + "=" * 60 + "\n")


# ---------------------------------------------------------
# STEP 4: Remove duplicates and empty rows
# ---------------------------------------------------------
# drop_duplicates(subset="url") removes rows that share the exact same
# article link — these are true duplicates, not just similar stories.
before = len(df)
df = df.drop_duplicates(subset="url")
after_dupes = len(df)

# dropna(subset=["headline"]) removes any row where the headline is
# completely empty/missing — useless for analysis.
df = df.dropna(subset=["headline"])
after_empty = len(df)

print(f"Removed {before - after_dupes} duplicate article(s).")
print(f"Removed {after_dupes - after_empty} row(s) with missing headlines.")
print(f"Rows remaining: {len(df)}")
print("\n" + "=" * 60 + "\n")


# ---------------------------------------------------------
# STEP 5: Keep only the columns we actually need, in a nice order
# ---------------------------------------------------------
final_columns = ["language", "source_clean", "date_clean", "headline",
                  "description", "url"]
df_clean = df[final_columns].rename(columns={
    "source_clean": "source",
    "date_clean": "date",
})

# Sort by date so the file reads chronologically — easiest to skim.
df_clean = df_clean.sort_values("date")


# ---------------------------------------------------------
# STEP 6: Save the result
# ---------------------------------------------------------
df_clean.to_csv("clean_articles.csv", index=False)

print("Saved clean_articles.csv — this is your file for Days 5-6.")
print(f"Final count: {len(df_clean)} articles "
      f"({(df_clean['language'] == 'en').sum()} English, "
      f"{(df_clean['language'] == 'de').sum()} German)")
print("\nOpen clean_articles.csv in Excel now and skim through it —")
print("delete any rows by hand that are clearly off-topic.")
