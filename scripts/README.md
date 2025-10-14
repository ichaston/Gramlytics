# Scripts Directory

This directory contains data ingestion, processing, and training scripts for Gramlytics.

## Scripts

### `ingest_billboard.py` (S1-01)
Fetches current Billboard Hot 100 Top 10 and saves to `data/raw/`.

**Usage:**
```bash
python scripts/ingest_billboard.py
```

**Output:**
- `data/raw/billboard_top10_<date>.csv`

**Fields:**
- `song_title`, `artist_name`, `peak_position`, `weeks_on_chart`
- `current_rank`, `last_week_rank`, `chart_date`
- Placeholder fields: `genre`, `artist_past_grammy_noms`, `artist_past_grammy_wins`, `label_type`, `release_month`

---

### `scrape_grammy_history.py` (S1-02)
*Coming next* - Compiles Grammy nominees/winners from past 3-5 years.

---

### `prepare_training_data.py` (S1-03)
*Coming next* - Merges Billboard + Grammy data, engineers features.

---

## Setup

Install dependencies first:
```bash
pip install -r requirements.txt
```
