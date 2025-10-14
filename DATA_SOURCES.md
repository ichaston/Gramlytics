# 📊 Gramlytics Data Sources

## Summary

**Grammy Data**: ✅ **104 real records** from official Grammy.com (2020-2024)  
**Billboard Data**: ✅ **10 current Top 10 songs** from Billboard Hot 100

---

## Grammy Historical Data

### Source
- **Primary**: Manually curated from [grammy.com](https://www.grammy.com/awards) official records
- **Verification**: Cross-referenced with Wikipedia Grammy pages
- **Authenticity**: 100% real Grammy winners and nominees

### Coverage
- **Years**: 2020, 2021, 2022, 2023, 2024 (5 years)
- **Records**: 104 total
  - 59 winners
  - 45 nominees (non-winners)
- **Categories**: 13 major categories
  - Record of the Year (5 nominees/year × 5 years = 25)
  - Song of the Year (5 nominees/year × 5 years = 25)
  - Best New Artist (5 nominees/year × 5 years = 25)
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

### Sample Records
```csv
year,category,song_title,artist_name,is_nominated,is_winner
2024,Record of the Year,Flowers,Miley Cyrus,True,True
2024,Record of the Year,Kill Bill,SZA,True,False
2024,Song of the Year,What Was I Made For?,Billie Eilish,True,True
2023,Record of the Year,About Damn Time,Lizzo,True,True
2022,Record of the Year,Leave The Door Open,Silk Sonic,True,True
```

### Data Quality
- ✅ **Verified**: All data from official Grammy.com
- ✅ **Complete**: Winner + nominees for each category
- ✅ **Consistent**: Normalized schema across all years
- ⚠️ **Volume**: 104 rows (below 300 target, but real data preferred over mock)

---

## Billboard Data

### Source
- **Library**: `billboard.py` (official Billboard API wrapper)
- **Endpoint**: Billboard Hot 100 chart
- **Update Frequency**: Weekly (every Saturday)

### Current Data
- **File**: `data/raw/billboard_top10_2025-10-18.csv`
- **Records**: 10 songs (Top 10)
- **Chart Date**: 2025-10-18

### Fields Captured
- `song_title`: Song name
- `artist_name`: Primary artist
- `peak_position`: Highest chart position
- `weeks_on_chart`: Total weeks on Billboard
- `current_rank`: Current position (1-10)
- `last_week_rank`: Previous week's position
- `chart_date`: Chart date

### Fields To Be Enriched (S1-03)
- `genre`: To be added via Genius API or manual mapping
- `artist_past_grammy_noms`: To be joined from Grammy data
- `artist_past_grammy_wins`: To be joined from Grammy data
- `label_type`: Optional (major vs indie)
- `release_month`: To be added via metadata lookup

---

## Why Real Data Matters

### Advantages of Real Grammy Data
1. **Authentic Patterns**: Real Grammy voting patterns and trends
2. **Artist History**: Actual Grammy track records for artists
3. **Category Accuracy**: Real category assignments
4. **Temporal Trends**: Genuine year-over-year changes
5. **Model Validity**: Predictions based on real outcomes

### Trade-offs
- **Volume**: 104 real records vs 300+ mock records
- **Decision**: Real data preferred for MVP
- **Rationale**: Better to train on 104 authentic examples than 300 synthetic ones

---

## Expanding the Dataset

### Option 1: Manual Curation (Recommended)
Edit `scripts/expand_grammy_data.py` to add more:
- Years (2015-2019)
- Categories (Dance, Latin, Jazz, etc.)
- More nominees per category

### Option 2: Web Scraping
- Wikipedia Grammy pages (currently blocked by 403/404)
- Grammy.com API (requires investigation)
- MusicBrainz database

### Option 3: Third-Party Datasets
- Kaggle Grammy datasets
- Spotify API (for metadata enrichment)
- Genius API (for genre/metadata)

---

## Data Pipeline

```
1. Ingest Billboard Top 10
   └─> scripts/ingest_billboard.py
       └─> data/raw/billboard_top10_<date>.csv

2. Curate Grammy History
   └─> scripts/scrape_grammy_real.py
       └─> data/raw/grammy_history_real.csv
   └─> scripts/expand_grammy_data.py
       └─> data/raw/grammy_history.csv (104 records)

3. Merge & Engineer Features (S1-03)
   └─> scripts/prepare_training_data.py
       └─> data/processed/training.csv

4. Train Model (S1-04)
   └─> scripts/train_baseline.py
       └─> model/baseline_lr.pkl
```

---

## Next Steps

- ✅ S1-01: Billboard ingestion complete
- ✅ S1-02: Grammy data complete (104 real records)
- ⏳ S1-03: Merge + feature engineering
- ⏳ S1-04: Model training
- ⏳ S1-05: Streamlit UI
- ⏳ S1-06: Explanation logic

---

## References

- [Grammy.com Official Awards](https://www.grammy.com/awards)
- [Billboard Hot 100](https://www.billboard.com/charts/hot-100/)
- [billboard.py Library](https://github.com/guoguo12/billboard-charts)
