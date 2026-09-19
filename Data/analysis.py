import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(__file__).resolve().parent
CHART_DIR = PROJECT_DIR / "charts"

CHART_DIR.mkdir(exist_ok=True)

EXCEL_FILE = DATA_DIR / "Banglore_road_saftey.xlsx"

print("=" * 70)
print("BENGALURU ROAD SAFETY ANALYSIS")
print("=" * 70)

# ============================================================
# 2. LOAD DATA
# ============================================================

station_df = pd.read_excel(
    EXCEL_FILE,
    sheet_name="Station_Crashes"
)

city_df = pd.read_excel(
    EXCEL_FILE,
    sheet_name="City_Crashes"
)

violations_df = pd.read_excel(
    EXCEL_FILE,
    sheet_name="Violations"
)

print("\nData loaded successfully!")

# ============================================================
# 3. BASIC INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("DATASET INFORMATION")
print("=" * 70)

print("\nStation Crashes:")
print("Rows:", station_df.shape[0])
print("Columns:", station_df.shape[1])

print("\nCity Crashes:")
print("Rows:", city_df.shape[0])
print("Columns:", city_df.shape[1])

print("\nViolations:")
print("Rows:", violations_df.shape[0])
print("Columns:", violations_df.shape[1])

# ============================================================
# 4. DUPLICATE CHECK
# ============================================================

print("\n" + "=" * 70)
print("DUPLICATE CHECK")
print("=" * 70)

print("Station duplicates:", station_df.duplicated().sum())
print("City duplicates:", city_df.duplicated().sum())
print("Violation duplicates:", violations_df.duplicated().sum())

# ============================================================
# 5. DATA CLEANING
# ============================================================

station_clean = station_df.copy()
city_clean = city_df.copy()
violations_clean = violations_df.copy()

# Clean text columns
for column in ["zone", "sub_division", "station", "station_raw"]:
    if column in station_clean.columns:
        station_clean[column] = (
            station_clean[column]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

for column in ["offence", "category"]:
    if column in violations_clean.columns:
        violations_clean[column] = (
            violations_clean[column]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

# Do NOT convert missing numeric values to zero.
# Missing values are kept as NaN.

print("\nData cleaning completed.")

# ============================================================
# 6. YEAR-WISE CITY ANALYSIS
# ============================================================

yearly = city_clean[
    [
        "year",
        "fatal_crashes",
        "killed",
        "non_fatal_crashes",
        "total_crashes",
        "fatality_rate_pct"
    ]
].copy()

yearly = yearly.sort_values("year")

print("\n" + "=" * 70)
print("YEAR-WISE CRASH ANALYSIS")
print("=" * 70)

print(yearly.to_string(index=False))

# ============================================================
# 7. TOTAL STATISTICS
# ============================================================

total_crashes = yearly["total_crashes"].sum()
fatal_crashes = yearly["fatal_crashes"].sum()
total_killed = yearly["killed"].sum()
non_fatal_crashes = yearly["non_fatal_crashes"].sum()

print("\n" + "=" * 70)
print("OVERALL STATISTICS")
print("=" * 70)

print("Total crashes:", int(total_crashes))
print("Fatal crashes:", int(fatal_crashes))
print("People killed:", int(total_killed))
print("Non-fatal crashes:", int(non_fatal_crashes))

# ============================================================
# 8. HIGHEST / LOWEST YEARS
# ============================================================

highest_death_year = yearly.loc[
    yearly["killed"].idxmax()
]

lowest_death_year = yearly.loc[
    yearly["killed"].idxmin()
]

highest_crash_year = yearly.loc[
    yearly["total_crashes"].idxmax()
]

lowest_crash_year = yearly.loc[
    yearly["total_crashes"].idxmin()
]

print("\n" + "=" * 70)
print("HIGHEST / LOWEST YEARS")
print("=" * 70)

print(
    "Highest deaths:",
    int(highest_death_year["year"]),
    "->",
    int(highest_death_year["killed"])
)

print(
    "Lowest deaths:",
    int(lowest_death_year["year"]),
    "->",
    int(lowest_death_year["killed"])
)

print(
    "Highest crashes:",
    int(highest_crash_year["year"]),
    "->",
    int(highest_crash_year["total_crashes"])
)

print(
    "Lowest crashes:",
    int(lowest_crash_year["year"]),
    "->",
    int(lowest_crash_year["total_crashes"])
)

# ============================================================
# 9. STATION-WISE ANALYSIS
# ============================================================

station_summary = (
    station_clean
    .groupby("station", as_index=False)
    .agg(
        total_crashes=("total_crashes", "sum"),
        fatal_crashes=("fatal_crashes", "sum"),
        killed=("killed", "sum"),
        injured=("injured", "sum")
    )
    .sort_values("total_crashes", ascending=False)
)

top_10_stations = station_summary.head(10)

print("\n" + "=" * 70)
print("TOP 10 CRASH STATIONS")
print("=" * 70)

print(top_10_stations.to_string(index=False))

# ============================================================
# 10. ZONE-WISE ANALYSIS
# ============================================================

zone_summary = (
    station_clean
    .groupby("zone", as_index=False)
    .agg(
        total_crashes=("total_crashes", "sum"),
        fatal_crashes=("fatal_crashes", "sum"),
        killed=("killed", "sum"),
        injured=("injured", "sum")
    )
    .sort_values("total_crashes", ascending=False)
)

print("\n" + "=" * 70)
print("ZONE-WISE ANALYSIS")
print("=" * 70)

print(zone_summary.to_string(index=False))

# ============================================================
# 11. VIOLATION ANALYSIS
# ============================================================

violation_summary = (
    violations_clean
    .groupby("category", as_index=False)
    .agg(
        total_cases=("cases", "sum")
    )
    .sort_values("total_cases", ascending=False)
)

print("\n" + "=" * 70)
print("VIOLATION CATEGORY ANALYSIS")
print("=" * 70)

print(violation_summary.to_string(index=False))

# ============================================================
# 12. TOP OFFENCES
# ============================================================

offence_summary = (
    violations_clean
    .groupby("offence", as_index=False)
    .agg(
        total_cases=("cases", "sum")
    )
    .sort_values("total_cases", ascending=False)
)

top_10_offences = offence_summary.head(10)

print("\n" + "=" * 70)
print("TOP 10 OFFENCES")
print("=" * 70)

print(top_10_offences.to_string(index=False))

# ============================================================
# 13. CHART 1 - DEATHS BY YEAR
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    yearly["year"],
    yearly["killed"],
    marker="o"
)

plt.title("Bengaluru Road Accident Deaths by Year")
plt.xlabel("Year")
plt.ylabel("People Killed")
plt.grid(True)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "deaths_by_year.png",
    dpi=300
)

plt.close()

# ============================================================
# 14. CHART 2 - TOTAL CRASHES BY YEAR
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    yearly["year"],
    yearly["total_crashes"],
    marker="o"
)

plt.title("Bengaluru Total Road Crashes by Year")
plt.xlabel("Year")
plt.ylabel("Total Crashes")
plt.grid(True)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "crashes_by_year.png",
    dpi=300
)

plt.close()

# ============================================================
# 15. CHART 3 - FATALITY RATE
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    yearly["year"],
    yearly["fatality_rate_pct"],
    marker="o"
)

plt.title("Road Crash Fatality Rate by Year")
plt.xlabel("Year")
plt.ylabel("Fatality Rate (%)")
plt.grid(True)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "fatality_rate_by_year.png",
    dpi=300
)

plt.close()

# ============================================================
# 16. CHART 4 - TOP 10 STATIONS
# ============================================================

plt.figure(figsize=(12, 7))

plt.barh(
    top_10_stations["station"][::-1],
    top_10_stations["total_crashes"][::-1]
)

plt.title("Top 10 Police Stations by Total Crashes")
plt.xlabel("Total Crashes")
plt.ylabel("Police Station")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "top_10_crash_stations.png",
    dpi=300
)

plt.close()

# ============================================================
# 17. CHART 5 - ZONE-WISE CRASHES
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    zone_summary["zone"],
    zone_summary["total_crashes"]
)

plt.title("Zone-wise Road Crashes")
plt.xlabel("Zone")
plt.ylabel("Total Crashes")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "zone_wise_crashes.png",
    dpi=300
)

plt.close()

# ============================================================
# 18. CHART 6 - VIOLATION CATEGORIES
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    violation_summary["category"],
    violation_summary["total_cases"]
)

plt.title("Traffic Violation Cases by Category")
plt.xlabel("Violation Category")
plt.ylabel("Cases")

plt.xticks(rotation=45, ha="right")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "violation_categories.png",
    dpi=300
)

plt.close()

# ============================================================
# 19. CHART 7 - TOP 10 OFFENCES
# ============================================================

plt.figure(figsize=(12, 7))

plt.barh(
    top_10_offences["offence"][::-1],
    top_10_offences["total_cases"][::-1]
)

plt.title("Top 10 Traffic Offences")
plt.xlabel("Cases")
plt.ylabel("Offence")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "top_10_offences.png",
    dpi=300
)

plt.close()

# ============================================================
# 20. SAVE ANALYSIS RESULTS
# ============================================================

OUTPUT_FILE = PROJECT_DIR / "road_safety_analysis_results.xlsx"

with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:

    yearly.to_excel(
        writer,
        sheet_name="Yearly Analysis",
        index=False
    )

    station_summary.to_excel(
        writer,
        sheet_name="Station Analysis",
        index=False
    )

    zone_summary.to_excel(
        writer,
        sheet_name="Zone Analysis",
        index=False
    )

    violation_summary.to_excel(
        writer,
        sheet_name="Violation Categories",
        index=False
    )

    offence_summary.to_excel(
        writer,
        sheet_name="Offence Analysis",
        index=False
    )

# ============================================================
# 21. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 70)

print("\nCharts saved in:")
print(CHART_DIR)

print("\nResults Excel saved as:")
print(OUTPUT_FILE)

print("\nGenerated charts:")
print("1. deaths_by_year.png")
print("2. crashes_by_year.png")
print("3. fatality_rate_by_year.png")
print("4. top_10_crash_stations.png")
print("5. zone_wise_crashes.png")
print("6. violation_categories.png")
print("7. top_10_offences.png")