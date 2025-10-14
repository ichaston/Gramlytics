# 🎶 Gramlytics

**Gramlytics** is an AI-powered music analytics tool that predicts which Billboard-charting songs and artists are most likely to receive Grammy nominations or wins.  
By combining real-time Billboard chart data with historical Grammy outcomes, Gramlytics uncovers the relationship between commercial success and critical acclaim.

---

## 📌 Overview

Gramlytics helps:
- Forecast Grammy nominations based on Billboard performance
- Highlight the most promising artists week by week
- Understand *why* certain songs may (or may not) get nominated

---

## 🚀 Live Features (MVP)

- 🔍 Billboard Hot 100 chart data (all 100 songs)
- 🧠 ML model predicting Grammy nomination probability
- 🎨 Album art for each song
- 🔎 Song lookup and search
- 📊 Interactive Streamlit dashboard with explanations

---

## 🏃 Quick Start

### Run the App

```bash
cd /../Gramlytics
source venv/bin/activate
streamlit run app/main.py
```

The app will open automatically at **http://localhost:8501**

### First Time Setup

```bash
# 1. Navigate to project
cd /../Gramlytics

# 2. Create virtual environment (if not exists)
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
streamlit run app/main.py
```

### Update Data (Optional)

```bash
# Refresh Billboard Hot 100
python scripts/ingest_billboard.py

# Regenerate training data
python scripts/prepare_training_data.py

# Retrain model
python scripts/train_baseline.py

# Run app with updated data
streamlit run app/main.py
```

---

## 📂 Project Docs

| File | Description |
|------|-------------|
| [`PRD.md`](./PRD.md) | Product Requirements Document |
| [`DATAMODEL.md`](./DATAMODEL.md) | Full input/output schema and training format |
| [`BACKLOG.md`](./BACKLOG.md) | Task tracking and feature planning |
| [`SPRINTPLAN.md`](./SPRINTPLAN.md) | Week-by-week development schedule |

---

## 🧠 Tech Stack

- `Python`, `Pandas`, `scikit-learn` or `XGBoost`
- `billboard.py` for live chart scraping
- `Wikipedia` or `grammy.com` for award history
- `Flask` or `Streamlit` for UI

---

## 📄 License

MIT License

---

## 👤 Author

Built with ✨ at a 2025 Hackathon.
