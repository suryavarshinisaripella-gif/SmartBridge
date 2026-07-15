# Visualization Tool for Electric Vehicle Charge and Range Analysis

## What's included
- `data/ev_charging_range_data.csv` — 5,000-row EV charging session dataset
  (vehicle model, battery, station type, SOC, duration, range, cost, temperature, etc.)
  Generated with realistic distributions since a live dataset wasn't provided —
  swap it out for your own export any time, same column structure works.
- `charts/` — 6 exploratory analysis charts (PNG) from the Python EDA
- `eda_analysis.py` — the analysis script that produced the charts + summary stats
- `app/` — full Flask web application (routes, templates, DB, CSS)

## Step 1 — Build your Tableau dashboard
1. Open Tableau Public / Desktop, connect to `data/ev_charging_range_data.csv`.
2. Build these sheets (mirrors the Python EDA so you have a story to tell mentors):
   - Avg charging duration by charger_type (bar)
   - distance_driven_km vs estimated_range_km (scatter)
   - Sessions by hour_of_day (bar)
   - Avg range_efficiency_km_per_kwh by vehicle_model (bar)
   - Avg cost_inr by station_type (bar)
   - temperature_c vs range_efficiency_km_per_kwh (scatter)
3. Combine sheets into one **Dashboard**, then build a **Story** walking through
   the insights (charging patterns → range efficiency → cost → temperature effect).
4. Publish to Tableau Public (Server menu → Save to Tableau Public).
5. On your published view: Share → Embed Code → copy the `src` URL.

## Step 2 — Wire it into the Flask app
1. Open `app/templates/dashboard.html`
2. Replace the placeholder iframe `src` with your real Tableau Public embed URL.

## Step 3 — Run the app
```bash
cd app
pip install -r requirements.txt
python app.py
```
Visit http://127.0.0.1:5000 — sign up, log in, and view the dashboard page.

## Step 4 — Submit
- Push this folder to GitHub.
- Record a short demo video (home → signup/login → dashboard with your live Tableau viz).
- Submit the repo link, dashboard link, and video link through your SkillWallet task.

## Key findings from the analysis (for your report/demo narration)
- Ultra-fast chargers average ~13 min per session vs ~223 min for home/slow chargers.
- Range efficiency varies notably by model — compact EVs (e.g. Nexon EV, Kona) trend
  higher km/kWh than larger/performance EVs.
- Extreme temperatures (below 10°C or above 40°C) measurably reduce range efficiency.
- Home charging remains the most common session type, despite the longest duration.
