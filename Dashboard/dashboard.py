import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_DIR / "Data" / "Banglore_road_saftey.xlsx"
RESULT_FILE = PROJECT_DIR / "road_safety_analysis_results.xlsx"
CHART_DIR = PROJECT_DIR / "charts"

CHART_DIR.mkdir(exist_ok=True)


# ============================================================
# LOAD ANALYSIS RESULTS
# ============================================================

yearly = pd.read_excel(RESULT_FILE, sheet_name="Yearly Analysis")
station = pd.read_excel(RESULT_FILE, sheet_name="Station Analysis")
zone = pd.read_excel(RESULT_FILE, sheet_name="Zone Analysis")
violation = pd.read_excel(RESULT_FILE, sheet_name="Violation Categories")
offence = pd.read_excel(RESULT_FILE, sheet_name="Offence Analysis")


# ============================================================
# TOTALS
# ============================================================

total_crashes = yearly["total_crashes"].sum()
total_fatal = yearly["fatal_crashes"].sum()
total_killed = yearly["killed"].sum()
total_non_fatal = yearly["non_fatal_crashes"].sum()


print("\n" + "=" * 60)
print("          BANGALORE ROAD SAFETY DASHBOARD")
print("=" * 60)

print(f"\nTotal Crashes       : {total_crashes:,.0f}")
print(f"Total Fatal Crashes: {total_fatal:,.0f}")
print(f"Total People Killed: {total_killed:,.0f}")
print(f"Total Non-Fatal    : {total_non_fatal:,.0f}")


# ============================================================
# 1. CRASHES BY YEAR
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    yearly["year"],
    yearly["total_crashes"],
    marker="o",
    linewidth=2
)

plt.title("Bangalore Road Crashes by Year")
plt.xlabel("Year")
plt.ylabel("Total Crashes")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    CHART_DIR / "dashboard_crashes_by_year.png",
    dpi=300
)

plt.close()


# ============================================================
# 2. DEATHS BY YEAR
# ============================================================

plt.figure(figsize=(12, 6))

plt.bar(
    yearly["year"],
    yearly["killed"]
)

plt.title("People Killed in Road Crashes by Year")
plt.xlabel("Year")
plt.ylabel("People Killed")
plt.xticks(yearly["year"], rotation=45)
plt.tight_layout()

plt.savefig(
    CHART_DIR / "dashboard_deaths_by_year.png",
    dpi=300
)

plt.close()


# ============================================================
# 3. ZONE-WISE CRASHES
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    zone["zone"],
    zone["total_crashes"]
)

plt.title("Zone-wise Road Crashes")
plt.xlabel("Zone")
plt.ylabel("Total Crashes")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "dashboard_zone_crashes.png",
    dpi=300
)

plt.close()


# ============================================================
# 4. TOP 10 CRASH STATIONS
# ============================================================

top_stations = station.head(10).sort_values(
    "total_crashes"
)

plt.figure(figsize=(12, 7))

plt.barh(
    top_stations["station"],
    top_stations["total_crashes"]
)

plt.title("Top 10 Stations by Total Crashes")
plt.xlabel("Total Crashes")
plt.ylabel("Police Station")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "dashboard_top_crash_stations.png",
    dpi=300
)

plt.close()


# ============================================================
# 5. TOP 10 DEATH STATIONS
# ============================================================

top_deaths = station.sort_values(
    "killed",
    ascending=False
).head(10).sort_values("killed")

plt.figure(figsize=(12, 7))

plt.barh(
    top_deaths["station"],
    top_deaths["killed"]
)

plt.title("Top 10 Stations by People Killed")
plt.xlabel("People Killed")
plt.ylabel("Police Station")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "dashboard_top_death_stations.png",
    dpi=300
)

plt.close()


# ============================================================
# 6. VIOLATION CATEGORIES
# ============================================================

top_violations = violation.head(10)

plt.figure(figsize=(12, 7))

plt.barh(
    top_violations["category"],
    top_violations["total_cases"]
)

plt.title("Top Violation Categories")
plt.xlabel("Total Cases")
plt.ylabel("Category")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "dashboard_violation_categories.png",
    dpi=300
)

plt.close()


# ============================================================
# 7. TOP OFFENCES
# ============================================================

top_offences = offence.head(10).sort_values(
    "total_cases"
)

plt.figure(figsize=(12, 7))

plt.barh(
    top_offences["offence"],
    top_offences["total_cases"]
)

plt.title("Top 10 Road Safety Offences")
plt.xlabel("Total Cases")
plt.ylabel("Offence")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "dashboard_top_offences.png",
    dpi=300
)

plt.close()


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("DASHBOARD CHARTS GENERATED SUCCESSFULLY!")
print("=" * 60)

print("\nCharts saved in:")
print(CHART_DIR)

print("\nGenerated:")
print("1. dashboard_crashes_by_year.png")
print("2. dashboard_deaths_by_year.png")
print("3. dashboard_zone_crashes.png")
print("4. dashboard_top_crash_stations.png")
print("5. dashboard_top_death_stations.png")
print("6. dashboard_violation_categories.png")
print("7. dashboard_top_offences.png")

print("\nDashboard preparation completed!")