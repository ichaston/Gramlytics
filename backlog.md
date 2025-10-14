# 📋 Gramlytics – Development Backlog

This file tracks planned features, tasks, and ideas for the Gramlytics project. Tasks are categorized by priority and scope: MVP features, stretch goals, and future enhancements.

---

## ✅ MVP Backlog (Core for Demo)

| Priority | Task | Status |
|----------|------|--------|
| 🔴 High | Set up project structure (`/data`, `/model`, `/app`) | ⬜ Not started |
| 🔴 High | Ingest Billboard Top 10 using `billboard.py` | ⬜ Not started |
| 🔴 High | Manually compile historical Grammy data (CSV) | ⬜ Not started |
| 🔴 High | Build simplified training dataset (merge chart + Grammy) | ⬜ Not started |
| 🔴 High | Train baseline model (logistic regression or XGBoost) | ⬜ Not started |
| 🔴 High | Create Flask or Streamlit app to run predictions | ⬜ Not started |
| 🔴 High | Display prediction results with probability + category | ⬜ Not started |
| 🟠 Medium | Add search UI (artist/song lookup) | ⬜ Not started |
| 🟠 Medium | Write explanation logic (basic rule-based) | ⬜ Not started |
| 🟢 Low | Deploy app on Streamlit Cloud or Replit | ⬜ Not started |

---

## 🚀 Stretch Goals (Nice to Have)

| Task | Notes |
|------|-------|
| Add lyrics-based sentiment analysis | Optional: Use Genius API + TextBlob |
| Add social sentiment signals (Twitter/YouTube comments) | Use scraped data or mock values |
| Predict win probability separately from nomination | Secondary model |
| Show Grammy eligibility logic (cutoff date flag) | Based on release_month |
| Compare multiple songs/artists head-to-head | Simple UI selector |
| Category-specific model tuning (e.g., Pop vs Rap vs R&B) | More accurate by genre |

---

## 🧪 Data & Research Tasks

| Task | Notes |
|------|-------|
| Create `grammy_training_data.csv` from past 5 years | Pull from Wikipedia or Grammy.com |
| Map Grammy categories to Billboard genres | Helps with category prediction |
| Analyze distribution of major vs indie label winners | Optional feature for label_type weighting |

---

## ✨ Future Enhancements (Post-Hackathon)

| Task | Notes |
|------|-------|
| Build public-facing API for predictions | REST or GraphQL |
| Add user auth to save predictions or favorites | Firebase/Auth0/etc |
| Turn into a browser extension (Grammy predictor on YouTube/Spotify) | Wild but cool |
| Enable Slack or Discord bot: “Will this win a Grammy?” | Community fun use |
| Support Grammy predictions for albums | Track-level first, album-level next |

---

## 🧱 Changelog

| Date | Update |
|------|--------|
| 2025-10-14 | Initial backlog created with MVP + stretch goals |

---

## 📌 How to Use This File

- Check off tasks (`✅`) as you go.
- Keep MVP section clean and focused for demo day.
- Add new ideas to Stretch or Future Enhancements — but don’t overload MVP.
