import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("/home/claude/ev_project/data/ev_charging_range_data.csv")

# ---------- Summary stats ----------
summary = {
    "total_sessions": len(df),
    "avg_charging_duration_min": round(df.charging_duration_min.mean(), 1),
    "avg_energy_added_kwh": round(df.energy_added_kwh.mean(), 2),
    "avg_distance_driven_km": round(df.distance_driven_km.mean(), 1),
    "avg_range_efficiency_km_per_kwh": round(df.range_efficiency_km_per_kwh.mean(), 2),
    "avg_cost_inr": round(df.cost_inr.mean(), 2),
}
print("SUMMARY:", summary)

print("\nSessions by station type:\n", df.station_type.value_counts())
print("\nSessions by vehicle model:\n", df.vehicle_model.value_counts())
print("\nAvg duration by charger type:\n", df.groupby("charger_type").charging_duration_min.mean().round(1))
print("\nAvg range efficiency by model:\n", df.groupby("vehicle_model").range_efficiency_km_per_kwh.mean().round(2).sort_values(ascending=False))

plt.style.use("seaborn-v0_8-whitegrid")
out = "/home/claude/ev_project/charts"

# 1. Charging duration by charger type
fig, ax = plt.subplots(figsize=(7, 4.5))
df.groupby("charger_type").charging_duration_min.mean().sort_values().plot(kind="barh", ax=ax, color="#2E86AB")
ax.set_title("Avg Charging Duration by Charger Type")
ax.set_xlabel("Minutes")
plt.tight_layout()
plt.savefig(f"{out}/1_duration_by_charger_type.png", dpi=140)
plt.close()

# 2. Distance driven vs estimated range (scatter)
fig, ax = plt.subplots(figsize=(7, 4.5))
sample = df.sample(600, random_state=1)
ax.scatter(sample.estimated_range_km, sample.distance_driven_km, alpha=0.4, s=18, color="#E76F51")
ax.plot([0, 700], [0, 700], "k--", linewidth=1, label="1:1 reference")
ax.set_xlabel("Estimated Range (km)")
ax.set_ylabel("Distance Driven (km)")
ax.set_title("Estimated Range vs Actual Distance Driven")
ax.legend()
plt.tight_layout()
plt.savefig(f"{out}/2_range_vs_distance.png", dpi=140)
plt.close()

# 3. Sessions by hour of day
fig, ax = plt.subplots(figsize=(7, 4.5))
df.hour_of_day.value_counts().sort_index().plot(kind="bar", ax=ax, color="#2A9D8F")
ax.set_title("Charging Sessions by Hour of Day")
ax.set_xlabel("Hour")
ax.set_ylabel("Sessions")
plt.tight_layout()
plt.savefig(f"{out}/3_sessions_by_hour.png", dpi=140)
plt.close()

# 4. Range efficiency by vehicle model
fig, ax = plt.subplots(figsize=(7, 4.5))
df.groupby("vehicle_model").range_efficiency_km_per_kwh.mean().sort_values().plot(kind="barh", ax=ax, color="#F4A261")
ax.set_title("Avg Range Efficiency (km/kWh) by Model")
ax.set_xlabel("km per kWh")
plt.tight_layout()
plt.savefig(f"{out}/4_efficiency_by_model.png", dpi=140)
plt.close()

# 5. Cost by station type
fig, ax = plt.subplots(figsize=(7, 4.5))
df.groupby("station_type").cost_inr.mean().sort_values().plot(kind="barh", ax=ax, color="#264653")
ax.set_title("Avg Cost per Session by Station Type (INR)")
ax.set_xlabel("INR")
plt.tight_layout()
plt.savefig(f"{out}/5_cost_by_station.png", dpi=140)
plt.close()

# 6. Temperature effect on range efficiency
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.scatter(df.temperature_c, df.range_efficiency_km_per_kwh, alpha=0.15, s=10, color="#6A4C93")
ax.set_xlabel("Temperature (°C)")
ax.set_ylabel("Range Efficiency (km/kWh)")
ax.set_title("Temperature vs Range Efficiency")
plt.tight_layout()
plt.savefig(f"{out}/6_temp_vs_efficiency.png", dpi=140)
plt.close()

print("\nCharts saved to", out)
