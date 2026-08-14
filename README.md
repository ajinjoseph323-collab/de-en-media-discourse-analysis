# English vs. German Media Framing of Germany's Skilled-Worker Shortage

A comparative discourse analysis project examining how English-language and
German-language news coverage frame Germany's *Fachkräftemangel*
(skilled-worker shortage).

## Why this project

As a Master's student in Data and Discourse Studies at TU Darmstadt, I built
this project to combine my academic training in discourse analysis with
practical data skills (Python, Excel) — and to have something concrete to
show for it ahead of my mandatory internship search.

## Method

- Collected 80 news headlines (40 English, 40 German) via Google News RSS,
  published within roughly the past month (August 2026)
- Cleaned and deduplicated the dataset using pandas
- Performed word-frequency analysis (Python, NLTK stopword removal) to
  compare vocabulary and framing patterns between the two language groups
- Scored sentiment using a **single multilingual model**
  (`nlptown/bert-base-multilingual-uncased-sentiment`) so scores are
  directly comparable across languages, rather than using two different
  sentiment tools per language
- Visualized results in both Python (matplotlib) and Excel

## Key findings

1. **Different framing.** English-language coverage — largely from Indian
   outlets — frames the shortage as a **recruitment/opportunity story**:
   top words were *skilled, India, labour, Indian, demand*. German-language
   coverage frames it as a **domestic economic paradox**: top words were
   *weniger* (fewer), *warum* (why), *Arbeitsmarkt* (labor market), *trotz*
   (despite), *Stellenabbau* (job cuts).
2. **Different tone.** Average sentiment was more negative in German
   coverage (−0.26) than English coverage (−0.09), consistent with the more
   skeptical, self-questioning framing seen in the word-frequency results.

## Limitations

- Modest sample size (40 headlines per language) — findings describe a
  consistent directional pattern, not a statistically definitive claim
- English sample skews toward Indian outlets rather than general Western
  press, which likely shapes the "opportunity" framing specifically
- Analysis is based on headlines only, not full article text, so
  within-article nuance isn't captured

## Repo contents

| File | Purpose |
|---|---|
| `day2_collect_articles_v2.py` | Collects EN/DE headlines via Google News RSS |
| `day3_4_clean_data.py` | Cleans, deduplicates, and standardizes the raw dataset |
| `add_translation_column.py` | Adds English translations for German headlines |
| `day5_6_word_frequency.py` | Word-frequency analysis and chart |
| `day7_8_sentiment_analysis.py` | Multilingual sentiment scoring and chart |
| `raw_articles.csv` | Original collected dataset |
| `clean_articles.csv` | Cleaned dataset with English translations |
| `word_frequencies.csv` | Full word-frequency results |
| `sentiment_results.csv` | Per-article sentiment scores |
| `discourse_analysis_visuals.xlsx` | Excel-built charts and PivotTable |
| `word_frequency_chart.png`, `sentiment_by_language.png` | Python-generated charts |

## How to run

```bash
pip install requests pandas feedparser deep-translator nltk matplotlib transformers torch
python day2_collect_articles_v2.py
python day3_4_clean_data.py
python add_translation_column.py
python day5_6_word_frequency.py
python day7_8_sentiment_analysis.py
```

## Author

**Ajin Joseph** — M.A. Data and Discourse Studies, TU Darmstadt
[LinkedIn](https://linkedin.com/in/ajinjoseph-de)
