# 📊 Data Model – Gramlytics

This document defines the simplified data schema used by **Gramlytics** to predict Grammy nomination likelihood for Billboard-charting songs.

---

## 🧠 Purpose

This schema powers:
- The ML model that predicts Grammy nomination probability
- The user-facing prediction dashboard
- Lightweight explainability of results

---

## 📥 Input Schema (Simplified Feature Set)

| Field | Type | Description |
|-------|------|-------------|
| `song_title` | `string` | Title of the song |
| `artist_name` | `string` | Name of the primary artist |
| `peak_position` | `int` | Highest Billboard chart position (1 = best) |
| `weeks_on_chart` | `int` | Total number of weeks on Billboard |
| `genre` | `string` | General genre (Pop, Rap, R&B, etc.) |
| `artist_past_grammy_noms` | `int` | Number of prior Grammy nominations |
| `artist_past_grammy_wins` | `int` | Number of prior Grammy wins |
| `label_type` | `string` | `"major"` or `"indie"` (optional for MVP) |
| `release_month` | `string` | Release month of the song (e.g., "August") |

> 🔹 *Only 7–9 columns — fast to collect and model.*

---

## 🏷️ Target Labels

| Field | Type | Description |
|-------|------|-------------|
| `is_nominated` | `boolean` | True if the song received a Grammy nomination |
| `predicted_category` | `string` | Best-fit Grammy category |
| `nomination_probability` | `float` | Likelihood score from 0.0 to 1.0 |

---

## 🧪 Sample Input

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
