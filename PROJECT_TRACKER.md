# 📊 Gramlytics – Comprehensive Project Tracker

**Last Updated**: 2025-10-14  
**Sprint**: Sprint 1 (Oct 14-21, 2025)  
**Status**: Planning Complete → Implementation Starting

---

## 🎯 Project Mission
AI-powered music analytics tool predicting Grammy nominations for Billboard-charting songs by analyzing real-time chart performance, artist metadata, and historical Grammy trends.

---

## 📋 Data Schema (from datamodel.md)

### Input Features (9 fields)
| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `song_title` | string | Song title | Billboard |
| `artist_name` | string | Primary artist | Billboard |
| `peak_position` | int | Highest chart position (1=best) | Billboard |
| `weeks_on_chart` | int | Total weeks on Billboard | Billboard |
| `genre` | string | Pop, Rap, R&B, etc. | Genius API / manual |
| `artist_past_grammy_noms` | int | Prior Grammy nominations | Grammy.com |
| `artist_past_grammy_wins` | int | Prior Grammy wins | Grammy.com |
| `label_type` | string | "major" or "indie" (optional) | Manual research |
| `release_month` | string | Release month (e.g., "August") | Billboard / metadata |

### Target Labels
| Field | Type | Description |
|-------|------|-------------|
| `is_nominated` | boolean | Grammy nomination received |
| `predicted_category` | string | Best-fit Grammy category |
| `nomination_probability` | float | Likelihood 0.0–1.0 |

### Sample Record
```json
{
  "song_title": "Paint The Town Red",
  "artist_name": "Doja Cat",
  "peak_position": 1,
  "weeks_on_chart": 19,
  "genre": "Pop",
  "artist_past_grammy_noms": 6,
  "artist_past_grammy_wins": 1,
  "label_type": "major",
  "release_month": "August"
}
```

---

## 🗂️ Repository Structure

```
Gramlytics/
├── data/
│   ├── raw/                    # Raw ingested data
│   │   ├── billboard_top10_<date>.csv
│   │   └── grammy_history.csv
│   ├── interim/                # Intermediate processing
│   └── processed/              # Final training data
│       └── training.csv
├── model/
│   ├── baseline_lr.pkl         # Saved model artifact
│   └── train_baseline.py       # Training script (or in scripts/)
├── app/
│   └── main.py                 # Streamlit UI
├── scripts/
│   ├── ingest_billboard.py     # S1-01
│   ├── scrape_grammy_history.py # S1-02
│   └── prepare_training_data.py # S1-03
├── requirements.txt
├── README-5.md
├── PRD.md
├── datamodel.md
├── backlog.md
├── sprintplan.md
└── PROJECT_TRACKER.md (this file)
```

---

## 🚀 Sprint 1 Scope (Oct 14-21, 2025)

**Goal**: End-to-end thin slice—ingest Top 10, build minimal training dataset, train baseline model, expose predictions in Streamlit UI.

### Stories & Tasks (20 pts total)

#### ✅ S1-01: Billboard Top 10 Ingestion (3 pts) – Day 1-2
- **T1.1**: Research and call `billboard.py` to pull Top 10 (1 pt) ✅
- **T1.2**: Normalize fields to `datamodel.md` (1 pt) ✅
- **T1.3**: Save `data/raw/billboard_top10_<date>.csv` (1 pt) ✅
- **Acceptance**: Script outputs CSV with 10 rows and required columns ✅
- **Status**: ✅ **COMPLETE** (2025-10-14)

#### ✅ S1-02: Historical Grammy CSV (4 pts) – Day 1-2
- **T2.1**: Compile nominees/winners for 3–5 years from Wikipedia/grammy.com (2 pts) ✅
- **T2.2**: Normalize to labels in `datamodel.md` (1 pt) ✅
- **T2.3**: Save `data/raw/grammy_history.csv` (1 pt) ✅
- **Acceptance**: CSV with ≥300 rows across 3–5 years; includes nominees ✅
- **Status**: ✅ **COMPLETE** (2025-10-14) - 350 rows, 5 years, 14 categories

#### ✅ S1-03: Merge + Feature Engineering (3 pts) – Day 3
- **T3.1**: Join on artist/title; derive `is_nominated` (1 pt) ✅
- **T3.2**: Fill minimal features: `peak_position`, `weeks_on_chart`, `genre` (1 pt) ✅
- **T3.3**: Save `data/processed/training.csv` (1 pt) ✅
- **Acceptance**: `training.csv` aligns with `datamodel.md`; null rate < 10% on core features ✅
- **Status**: ✅ **COMPLETE** (2025-10-14) - 111 records (101 labeled, 10 unlabeled)

#### ✅ S1-04: Baseline Model (4 pts) – Day 4
- **T4.1**: Train logistic regression; metrics (AUC/F1) via holdout (2 pts) ✅
- **T4.2**: Persist model to `model/baseline_lr.pkl` (1 pt) ✅
- **T4.3**: CLI or script to load and predict (1 pt) ✅
- **Acceptance**: Model trains without error; metrics printed; `baseline_lr.pkl` saved ✅
- **Status**: ✅ **COMPLETE** (2025-10-14) - Test AUC: 1.000, F1: 1.000

#### ✅ S1-05: Streamlit UI (4 pts) – Day 5
- **T5.1**: Basic page: table of Top 10 + probabilities + category (2 pts) ✅
- **T5.2**: Search box for artist/song lookup (basic filter) (1 pt) ✅
- **T5.3**: Minimal styling, instructions (1 pt) ✅
- **Acceptance**: `streamlit run app/main.py` shows table with probabilities and category ✅
- **Status**: ✅ **COMPLETE** (2025-10-14) - 3 tabs: Predictions, Search, About

#### ✅ S1-06: Explanation Logic (2 pts) – Day 5
- **T6.1**: Rule snippets (e.g., high weeks_on_chart, top peak_position) (1 pt) ✅
- **T6.2**: Display explanation string per row (1 pt) ✅
- **Acceptance**: Each prediction includes a short explanation string ✅
- **Status**: ✅ **COMPLETE** (2025-10-14) - Integrated into Streamlit UI

---

## 📜 Runbook Commands

```bash
# Setup
pip install -r requirements.txt

# S1-01: Ingest Billboard Top 10
python scripts/ingest_billboard.py

# S1-02: Grammy history (manual or scripted)
python scripts/scrape_grammy_history.py  # or manual CSV creation

# S1-03: Prepare training data
python scripts/prepare_training_data.py

# S1-04: Train baseline model
python scripts/train_baseline.py

# S1-05 & S1-06: Run Streamlit app
streamlit run app/main.py
```

---

## ⚙️ Tech Stack & Dependencies

### Core Dependencies (requirements.txt)
```
billboard.py>=6.0.0
pandas>=2.0.0
scikit-learn>=1.3.0
streamlit>=1.28.0
requests>=2.31.0
```

### Optional (Stretch)
- `textblob` – sentiment analysis
- `beautifulsoup4` – web scraping
- `xgboost` – advanced modeling

---

## 🎯 Definition of Done (Sprint 1)

- [x] Code runs locally with documented commands
- [x] Minimal dataset artifacts versioned under `data/`
- [x] Baseline model trained and saved under `model/`
- [x] App starts locally and returns predictions for current Top 10
- [x] Basic explanation text accompanies each prediction

---

## 🚩 Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Data quality/joins mismatch | Manual mapping rules; fuzzy match fallback |
| Incomplete labels | Start with nominees (binary); expand later |
| Model underperforms | Add XGBoost fallback if time allows |
| API/scraper flakiness | Cache latest CSVs; keep manual CSV as fallback |

---

## 📈 Out of Scope (Sprint 1)

- Social/lyric sentiment analysis
- Category-specific model tuning
- Deployment to cloud
- Win probability (separate from nomination)
- Album-level predictions

---

## 🧪 Backlog Status (from backlog.md)

### MVP Tasks
| Priority | Task | Status |
|----------|------|--------|
| 🔴 High | Set up project structure | ✅ Complete |
| 🔴 High | Ingest Billboard Top 10 | ✅ Complete |
| 🔴 High | Compile Grammy historical data | ✅ Complete |
| 🔴 High | Build training dataset | ✅ Complete |
| 🔴 High | Train baseline model | ✅ Complete |
| 🔴 High | Create Streamlit app | ✅ Complete |
| 🔴 High | Display predictions | ✅ Complete |
| 🟠 Medium | Add search UI | ✅ Complete |
| 🟠 Medium | Write explanation logic | ✅ Complete |
| 🟢 Low | Deploy to Streamlit Cloud | ⬜ Not started |

---

## 📊 Progress Tracking

**Sprint 1 Progress**: 20/20 pts (100%) 🎉

- S1-01: ✅✅✅ (3/3 pts) **COMPLETE**
- S1-02: ✅✅✅✅ (4/4 pts) **COMPLETE**
- S1-03: ✅✅✅ (3/3 pts) **COMPLETE**
- S1-04: ✅✅✅✅ (4/4 pts) **COMPLETE**
- S1-05: ✅✅✅✅ (4/4 pts) **COMPLETE**
- S1-06: ✅✅ (2/2 pts) **COMPLETE**

**Next Action**: Sprint 1 Complete! 🎉 Ready for demo

---

## 🔗 Reference Documents

- **PRD.md**: Product requirements, objectives, features, tech stack
- **datamodel.md**: Input/output schema, sample records
- **backlog.md**: Full task list, stretch goals, future enhancements
- **sprintplan.md**: Sprint 1 detailed plan, schedule, risks
- **README-5.md**: Project overview and quick reference

---

## 📝 Notes

- **Target Users**: Record labels, A&R, marketers, curators, data enthusiasts, fans
- **Data Sources**: Billboard Hot 100, Grammy.com, Wikipedia, Genius API (optional)
- **Model Type**: Logistic regression baseline (XGBoost stretch)
- **UI Framework**: Streamlit (confirmed)
- **Timeline**: 1-week sprint (Oct 14-21, 2025)
- **Demo Milestone**: End of week—UI shows Top 10 with probabilities + explanations
