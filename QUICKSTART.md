# 🚀 Gramlytics - Quick Start Guide

## Setup (First Time)

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Pipeline

### S1-01: Ingest Billboard Top 10
```bash
source venv/bin/activate
python scripts/ingest_billboard.py
```

**Output**: `data/raw/billboard_top10_<date>.csv`

### S1-02: Grammy Historical Data
*Coming next*

### S1-03: Prepare Training Data
*Coming next*

### S1-04: Train Model
*Coming next*

### S1-05: Run Streamlit App
*Coming next*
```bash
streamlit run app/main.py
```

## Project Structure

```
Gramlytics/
├── data/
│   ├── raw/              # Raw data from ingestion
│   ├── interim/          # Intermediate processing
│   └── processed/        # Final training data
├── model/                # Saved model artifacts
├── app/                  # Streamlit UI
├── scripts/              # Data pipeline scripts
├── requirements.txt      # Python dependencies
└── PROJECT_TRACKER.md    # Comprehensive tracking doc
```

## Key Documents

- **PROJECT_TRACKER.md** - Complete project reference
- **sprintplan.md** - Sprint 1 detailed plan
- **PRD.md** - Product requirements
- **datamodel.md** - Data schema
- **backlog.md** - Full task list

## Current Status

✅ Project structure created  
✅ Requirements.txt defined  
✅ S1-01: Billboard ingestion script ready  
⬜ S1-02: Grammy historical data  
⬜ S1-03: Feature engineering  
⬜ S1-04: Model training  
⬜ S1-05: Streamlit UI  
⬜ S1-06: Explanation logic  
