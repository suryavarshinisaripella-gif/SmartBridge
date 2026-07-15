"""
Generates a synthetic-but-realistic EV Charging & Range Analysis dataset.
Mimics real-world telematics/charging-session data so it can be used for
EDA, Tableau dashboarding, and the Flask app.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

N = 5000  # number of charging sessions

models = [
    ("Tata Nexon EV", 30.2, 312, "Slow"),
    ("MG ZS EV", 50.3, 461, "Fast"),
    ("Hyundai Kona Electric", 39.2, 452, "Fast"),
    ("Tesla Model 3", 60.0, 491, "Ultra-Fast"),
    ("Mahindra XUV400", 39.4, 456, "Fast"),
    ("BYD Atto 3", 60.5, 521, "Fast"),
    ("Kia EV6", 77.4, 708, "Ultra-Fast"),
    ("Nissan Leaf", 40.0, 311, "Slow"),
]
model_names = [m[0] for m in models]
model_map = {m[0]: m for m in models}

stations = ["Home Charger", "Public Fast Station", "Mall Charging Hub",
            "Office Charger", "Highway Supercharger"]
station_charger_type = {
    "Home Charger": "Slow",
    "Public Fast Station": "Fast",
    "Mall Charging Hub": "Fast",
    "Office Charger": "Slow",
    "Highway Supercharger": "Ultra-Fast",
}
charger_power_kw = {"Slow": 7, "Fast": 50, "Ultra-Fast": 120}

cities = ["Hyderabad", "Bengaluru", "Delhi", "Mumbai", "Chennai", "Pune"]

rows = []
start_date = datetime(2024, 1, 1)

for i in range(N):
    model = np.random.choice(model_names, p=[0.22, 0.15, 0.15, 0.08, 0.12, 0.1, 0.06, 0.12])
    _, battery_kwh, rated_range, _ = model_map[model]

    station = np.random.choice(stations, p=[0.35, 0.25, 0.15, 0.15, 0.10])
    charger_type = station_charger_type[station]
    power_kw = charger_power_kw[charger_type]

    start_soc = np.clip(np.random.normal(30, 15), 2, 70)
    target_soc = np.clip(start_soc + np.random.normal(55, 15), start_soc + 10, 100)
    energy_added_kwh = battery_kwh * (target_soc - start_soc) / 100

    # charging efficiency loss
    efficiency = np.random.uniform(0.85, 0.95)
    duration_hr = energy_added_kwh / (power_kw * efficiency)
    duration_min = round(duration_hr * 60, 1)

    temperature_c = np.round(np.random.normal(28, 7), 1)
    # cold/hot temps reduce charging efficiency & range slightly
    temp_penalty = 0
    if temperature_c < 10 or temperature_c > 40:
        temp_penalty = np.random.uniform(0.05, 0.15)

    estimated_range_km = round(rated_range * (target_soc / 100) * (1 - temp_penalty), 1)
    distance_driven_km = round(np.random.uniform(20, min(estimated_range_km, rated_range)), 1)

    cost_per_kwh = 8 if charger_type == "Slow" else (12 if charger_type == "Fast" else 18)  # INR
    cost = round(energy_added_kwh * cost_per_kwh, 2)

    day_offset = np.random.randint(0, 545)
    ts = start_date + timedelta(days=int(day_offset), hours=int(np.random.randint(0, 24)))

    rows.append({
        "session_id": f"EVS{i+1:05d}",
        "vehicle_model": model,
        "battery_capacity_kwh": battery_kwh,
        "rated_range_km": rated_range,
        "city": np.random.choice(cities),
        "station_type": station,
        "charger_type": charger_type,
        "charger_power_kw": power_kw,
        "start_soc_percent": round(start_soc, 1),
        "end_soc_percent": round(target_soc, 1),
        "energy_added_kwh": round(energy_added_kwh, 2),
        "charging_duration_min": duration_min,
        "temperature_c": temperature_c,
        "estimated_range_km": estimated_range_km,
        "distance_driven_km": distance_driven_km,
        "cost_inr": cost,
        "session_datetime": ts,
    })

df = pd.DataFrame(rows)
df["hour_of_day"] = df["session_datetime"].dt.hour
df["day_of_week"] = df["session_datetime"].dt.day_name()
df["month"] = df["session_datetime"].dt.month_name()
df["range_efficiency_km_per_kwh"] = round(df["distance_driven_km"] / df["energy_added_kwh"], 2)

df.to_csv("/home/claude/ev_project/data/ev_charging_range_data.csv", index=False)
print(df.shape)
print(df.head(3).to_string())
