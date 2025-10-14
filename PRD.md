# 🏆 Gramlytics – Product Requirements Document (PRD)

## 📌 Project Overview
**Gramlytics** is an AI-powered music analytics tool designed to predict which Billboard-charting songs and artists are most likely to receive Grammy nominations or wins. By analyzing real-time chart performance, artist metadata, and historical Grammy trends, Gramlytics bridges the gap between commercial success and critical recognition.

---

## 🎯 Objectives
- Continuously track and ingest weekly Billboard Hot 100 data (or Top 10 for MVP).
- Analyze song and artist performance metrics to determine nomination or win probability.
- Provide explainable predictions with key factors influencing the outcome.
- Offer an interactive interface for exploring Grammy forecasts and trends.

---

## 🧩 Key Features

| Feature | Description |
|--------|-------------|
| 📈 **Live Billboard Ingestion** | Pull and update weekly Billboard chart data automatically. |
| 🧠 **AI Nomination Predictor** | Predicts the likelihood of Grammy nominations and wins based on historical patterns and song performance. |
| 🏅 **Category Classifier** | Suggests likely Grammy categories (e.g., Best Pop Solo Performance, Best Rap Song). |
| 📊 **Prediction Dashboard** | Displays real-time probabilities, trends, and artist performance scores. |
| 🔍 **Song/Artist Lookup** | Users can search any artist or song to view nomination potential. |
| 📝 **Explainable Results** | Includes a short explanation of why a song may or may not be nominated. |

---

## 👤 Target Users
- Record labels and A&R teams tracking potential award contenders.
- Music marketers and playlist curators predicting cultural impact.
- Data and ML enthusiasts exploring entertainment analytics.
- Fans curious about which hits might make it to the Grammy stage.

---

## 🧰 Tech Stack

| Layer | Tool |
|-------|------|
| Backend | Python, Flask or FastAPI |
| Data Ingestion | `billboard.py`, web scraping, Genius API |
| ML/AI | Scikit-learn, XGBoost, Pandas (optional: GPT for explainability) |
| Frontend | Streamlit, React, or Flask templates |
| Hosting | GitHub Pages, Streamlit Cloud, or AWS EC2 |

---

## 📊 Data Sources
| Source | Usage |
|--------|-------|
| Billboard Hot 100 API | Weekly chart data |
| Grammy historical data | Past nominees and winners for training |
| Genius API | Genre, songwriter, and metadata enrichment |
| YouTube/Twitter (optional) | Sentiment and engagement analysis |

---

## 🤖 Prediction Model (MVP Approach)

**Input Features:**
- Peak chart position
- Weeks on chart
- Genre and subgenre
- Artist’s Grammy nomination history
- Label type (major vs indie)
- Release date proximity to Grammy cutoff
- Collaborations and songwriter profiles

**Output:**
- Nomination Probability (%)
- Win Probability (%)
- Likely Grammy Category
- Explanation of reasoning

---

## ✅ MVP Deliverables
- [ ] Automated retrieval of Billboard Top 10 songs.
- [ ] Machine learning model predicting nomination probability.
- [ ] Web-based dashboard showing current predictions.
- [ ] Search functionality for specific songs or artists.
- [ ] Short explanation for each prediction.

---

## 🚀 Stretch Goals
- Sentiment analysis on fan reactions and media coverage.
- Lyric and language complexity analysis.
- Timeline visualization of chart history vs. Grammy outcomes.
- Artist comparison tool for head-to-head predictions.

---

## 📂 Suggested Repository Structure
