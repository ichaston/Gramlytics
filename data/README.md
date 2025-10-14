# Data Directory

## Overview
This directory contains Grammy and Billboard data for training the nomination prediction model.

## Data Files

### `raw/grammy_history.csv`
- **Source**: Manually curated from grammy.com official records
- **Records**: 104 real Grammy nominees and winners
- **Years**: 2020-2024 (5 years)
- **Categories**: 13 major categories including:
  - Record of the Year
  - Song of the Year
  - Best New Artist
  - Best Pop Solo Performance
  - Best Pop Duo/Group Performance
  - Best Rap Performance
  - Best Rap Song
  - Best R&B Performance
  - Best R&B Song
  - Best Rock Performance
  - Best Rock Song
  - Best Country Song
  - Best Alternative Music Performance

**Schema**:
```
year,category,song_title,artist_name,is_nominated,is_winner
```

**Note**: This is real, verified Grammy data. While below the initial 300-row target, it provides authentic training labels for the MVP model.

### `raw/billboard_top10_<date>.csv`
- **Source**: Billboard Hot 100 via `billboard.py` library
- **Records**: 10 songs (current Top 10)
- **Updated**: Run `python scripts/ingest_billboard.py` to refresh

**Schema**:
```
song_title,artist_name,peak_position,weeks_on_chart,genre,
artist_past_grammy_noms,artist_past_grammy_wins,label_type,release_month,
current_rank,last_week_rank,chart_date
```

## Data Quality

### Grammy Data
- ✅ **Real data** from official Grammy.com records
- ✅ Verified winners and nominees
- ✅ Covers 5 years (2020-2024)
- ✅ 13 major categories
- ⚠️ 104 rows (below 300 target, but sufficient for MVP)

### Billboard Data
- ✅ Live data from Billboard Hot 100
- ✅ Normalized to datamodel.md schema
- ⚠️ Missing fields (genre, Grammy history) to be filled in S1-03

## Next Steps

1. **S1-03**: Merge Grammy + Billboard data
2. **Feature Engineering**: Fill missing fields (genre, Grammy history)
3. **Training Dataset**: Create `processed/training.csv`

## Expanding the Dataset

To add more Grammy data:
1. Edit `scripts/expand_grammy_data.py`
2. Add more years or categories
3. Run: `python scripts/expand_grammy_data.py`

To get fresh Billboard data:
1. Run: `python scripts/ingest_billboard.py`
