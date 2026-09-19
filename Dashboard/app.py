import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Bangalore Road Safety Analytics",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

RESULT_FILE = PROJECT_DIR / "road_safety_analysis_results.xlsx"
RAW_FILE = PROJECT_DIR / "Data" / "Banglore_road_saftey.xlsx"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f5f7fa;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .main-title {
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .subtitle {
        color: #6b7280;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        text-align: center;
    }

    .kpi-title {
        color: #6b7280;
        font-size: 14px;
        font-weight: 600;
    }

    .kpi-value {
        font-size: 30px;
        font-weight: 800;
        margin-top: 5px;
    }

    .section-title {
        font-size: 23px;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    .insight-card {
        background: white;
        padding: 18px;
        border-radius: 12px;
        border-left: 5px solid #2563eb;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    yearly = pd.read_excel(
        RESULT_FILE,
        sheet_name="Yearly Analysis"
    )

    station = pd.read_excel(
        RESULT_FILE,
        sheet_name="Station Analysis"
    )

    zone = pd.read_excel(
        RESULT_FILE,
        sheet_name="Zone Analysis"
    )

    violations = pd.read_excel(
        RESULT_FILE,
        sheet_name="Violation Categories"
    )

    offences = pd.read_excel(
        RESULT_FILE,
        sheet_name="Offence Analysis"
    )

    # Raw data
    station_raw = pd.read_excel(
        RAW_FILE,
        sheet_name="Station_Crashes"
    )

    try:
        violations_raw = pd.read_excel(
            RAW_FILE,
            sheet_name="Violations"
        )
    except Exception:
        violations_raw = pd.DataFrame()

    return (
        yearly,
        station,
        zone,
        violations,
        offences,
        station_raw,
        violations_raw
    )


(
    yearly,
    station,
    zone,
    violations,
    offences,
    station_raw,
    violations_raw
) = load_data()


# ============================================================
# DATA CLEANING
# ============================================================

yearly["year"] = pd.to_numeric(
    yearly["year"],
    errors="coerce"
)

station_raw["year"] = pd.to_numeric(
    station_raw["year"],
    errors="coerce"
)

station_raw["zone"] = (
    station_raw["zone"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

station_raw["station"] = (
    station_raw["station"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

station_raw["total_crashes"] = pd.to_numeric(
    station_raw["total_crashes"],
    errors="coerce"
)

station_raw["killed"] = pd.to_numeric(
    station_raw["killed"],
    errors="coerce"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## 🚦 Road Safety Analytics")

st.sidebar.markdown("---")

st.sidebar.markdown("### 📅 Time Period")

min_year = int(yearly["year"].min())
max_year = int(yearly["year"].max())

year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1
)

start_year, end_year = year_range


# ============================================================
# ZONE FILTER
# ============================================================

available_zones = sorted(
    station_raw["zone"]
    .dropna()
    .unique()
    .tolist()
)

zone_options = ["All Zones"] + available_zones

selected_zone = st.sidebar.selectbox(
    "📍 Select Zone",
    zone_options
)


# ============================================================
# STATION FILTER
# ============================================================

filtered_for_station_options = station_raw[
    (station_raw["year"] >= start_year) &
    (station_raw["year"] <= end_year)
].copy()

if selected_zone != "All Zones":

    filtered_for_station_options = filtered_for_station_options[
        filtered_for_station_options["zone"] == selected_zone
    ]

available_stations = sorted(
    filtered_for_station_options["station"]
    .dropna()
    .unique()
    .tolist()
)

station_options = ["All Stations"] + available_stations

selected_station = st.sidebar.selectbox(
    "🚔 Select Police Station",
    station_options
)


st.sidebar.markdown("---")

st.sidebar.markdown(
    f"""
    **Dashboard Period**

    `{start_year} – {end_year}`

    **Data Source**

    Bangalore Road Safety Dataset
    """
)


# ============================================================
# FILTER YEARLY DATA
# ============================================================

filtered_yearly = yearly[
    (yearly["year"] >= start_year) &
    (yearly["year"] <= end_year)
].copy()


# ============================================================
# FILTER STATION RAW DATA
# ============================================================

filtered_station = station_raw[
    (station_raw["year"] >= start_year) &
    (station_raw["year"] <= end_year)
].copy()


if selected_zone != "All Zones":

    filtered_station = filtered_station[
        filtered_station["zone"] == selected_zone
    ]


if selected_station != "All Stations":

    filtered_station = filtered_station[
        filtered_station["station"] == selected_station
    ]


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🚦 Bangalore Road Safety Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Data-driven analysis of road crashes, fatalities, police stations, zones and traffic violations'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# FILTER SUMMARY
# ============================================================

filter_text = f"**Showing:** {start_year}–{end_year}"

if selected_zone != "All Zones":
    filter_text += f"  |  **Zone:** {selected_zone}"

if selected_station != "All Stations":
    filter_text += f"  |  **Station:** {selected_station}"

st.info(filter_text)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_crashes = filtered_yearly["total_crashes"].sum()

fatal_crashes = filtered_yearly["fatal_crashes"].sum()

people_killed = filtered_yearly["killed"].sum()

non_fatal_crashes = filtered_yearly["non_fatal_crashes"].sum()


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">TOTAL CRASHES</div>
            <div class="kpi-value">{total_crashes:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">FATAL CRASHES</div>
            <div class="kpi-value">{fatal_crashes:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">PEOPLE KILLED</div>
            <div class="kpi-value">{people_killed:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">NON-FATAL CRASHES</div>
            <div class="kpi-value">{non_fatal_crashes:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# KEY INSIGHTS
# ============================================================

st.markdown(
    '<div class="section-title">💡 Key Insights</div>',
    unsafe_allow_html=True
)

ins1, ins2, ins3 = st.columns(3)


# Highest crash year
if not filtered_yearly.empty:

    highest_crash_year = filtered_yearly.loc[
        filtered_yearly["total_crashes"].idxmax()
    ]

    highest_death_year = filtered_yearly.loc[
        filtered_yearly["killed"].idxmax()
    ]

    with ins1:

        st.markdown(
            f"""
            <div class="insight-card">
                <b>📈 Highest Crash Year</b><br>
                {int(highest_crash_year["year"])}<br>
                <b>{highest_crash_year["total_crashes"]:,.0f}</b> crashes
            </div>
            """,
            unsafe_allow_html=True
        )

    with ins2:

        st.markdown(
            f"""
            <div class="insight-card">
                <b>⚠️ Highest Death Year</b><br>
                {int(highest_death_year["year"])}<br>
                <b>{highest_death_year["killed"]:,.0f}</b> people killed
            </div>
            """,
            unsafe_allow_html=True
        )


# Highest crash station
if not filtered_station.empty:

    station_totals = (
        filtered_station
        .groupby("station", as_index=False)["total_crashes"]
        .sum()
        .sort_values("total_crashes", ascending=False)
    )

    if not station_totals.empty:

        highest_station = station_totals.iloc[0]

        with ins3:

            st.markdown(
                f"""
                <div class="insight-card">
                    <b>🚔 Highest Crash Station</b><br>
                    {highest_station["station"]}<br>
                    <b>{highest_station["total_crashes"]:,.0f}</b> crashes
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# YEARLY TRENDS
# ============================================================

st.markdown(
    '<div class="section-title">📊 Yearly Crash Trends</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# CRASH TREND
# ------------------------------------------------------------

with col1:

    fig, ax = plt.subplots(figsize=(8, 4.5))

    ax.plot(
        filtered_yearly["year"],
        filtered_yearly["total_crashes"],
        marker="o",
        linewidth=2
    )

    ax.set_title(
        "Total Crashes by Year",
        fontweight="bold"
    )

    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Crashes")

    ax.grid(alpha=0.2)

    plt.tight_layout()

    st.pyplot(fig, width="stretch")

    plt.close(fig)


# ------------------------------------------------------------
# DEATH TREND
# ------------------------------------------------------------

with col2:

    fig, ax = plt.subplots(figsize=(8, 4.5))

    ax.plot(
        filtered_yearly["year"],
        filtered_yearly["killed"],
        marker="o",
        linewidth=2
    )

    ax.set_title(
        "People Killed by Year",
        fontweight="bold"
    )

    ax.set_xlabel("Year")
    ax.set_ylabel("People Killed")

    ax.grid(alpha=0.2)

    plt.tight_layout()

    st.pyplot(fig, width="stretch")

    plt.close(fig)


# ============================================================
# FATALITY RATE
# ============================================================

if "fatality_rate_pct" in filtered_yearly.columns:

    st.markdown(
        '<div class="section-title">📉 Fatality Rate Trend</div>',
        unsafe_allow_html=True
    )

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(
        filtered_yearly["year"],
        filtered_yearly["fatality_rate_pct"],
        marker="o",
        linewidth=2
    )

    ax.set_title(
        "Fatality Rate by Year",
        fontweight="bold"
    )

    ax.set_xlabel("Year")
    ax.set_ylabel("Fatality Rate (%)")

    ax.grid(alpha=0.2)

    plt.tight_layout()

    st.pyplot(fig, width="stretch")

    plt.close(fig)


# ============================================================
# ZONE ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">📍 Zone-wise Analysis</div>',
    unsafe_allow_html=True
)


zone_filtered = (
    filtered_station
    .groupby("zone", as_index=False)
    .agg(
        total_crashes=("total_crashes", "sum"),
        people_killed=("killed", "sum")
    )
    .sort_values("total_crashes", ascending=False)
)


z1, z2 = st.columns(2)


with z1:

    if not zone_filtered.empty:

        fig, ax = plt.subplots(figsize=(7, 4.5))

        ax.bar(
            zone_filtered["zone"],
            zone_filtered["total_crashes"]
        )

        ax.set_title(
            "Crashes by Zone",
            fontweight="bold"
        )

        ax.set_xlabel("Zone")
        ax.set_ylabel("Total Crashes")

        plt.xticks(rotation=20)

        plt.tight_layout()

        st.pyplot(fig, width="stretch")

        plt.close(fig)


with z2:

    if not zone_filtered.empty:

        fig, ax = plt.subplots(figsize=(7, 4.5))

        ax.bar(
            zone_filtered["zone"],
            zone_filtered["people_killed"]
        )

        ax.set_title(
            "Deaths by Zone",
            fontweight="bold"
        )

        ax.set_xlabel("Zone")
        ax.set_ylabel("People Killed")

        plt.xticks(rotation=20)

        plt.tight_layout()

        st.pyplot(fig, width="stretch")

        plt.close(fig)


# ============================================================
# STATION ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">🚔 Police Station Analysis</div>',
    unsafe_allow_html=True
)


station_summary_filtered = (
    filtered_station
    .groupby("station", as_index=False)
    .agg(
        total_crashes=("total_crashes", "sum"),
        people_killed=("killed", "sum")
    )
)


s1, s2 = st.columns(2)


# ------------------------------------------------------------
# TOP CRASH STATIONS
# ------------------------------------------------------------

with s1:

    top_crash_stations = (
        station_summary_filtered
        .sort_values(
            "total_crashes",
            ascending=False
        )
        .head(10)
    )

    if not top_crash_stations.empty:

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.barh(
            top_crash_stations["station"][::-1],
            top_crash_stations["total_crashes"][::-1]
        )

        ax.set_title(
            "Top 10 Stations by Total Crashes",
            fontweight="bold"
        )

        ax.set_xlabel("Total Crashes")

        plt.tight_layout()

        st.pyplot(fig, width="stretch")

        plt.close(fig)


# ------------------------------------------------------------
# TOP DEATH STATIONS
# ------------------------------------------------------------

with s2:

    top_death_stations = (
        station_summary_filtered
        .sort_values(
            "people_killed",
            ascending=False
        )
        .head(10)
    )

    if not top_death_stations.empty:

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.barh(
            top_death_stations["station"][::-1],
            top_death_stations["people_killed"][::-1]
        )

        ax.set_title(
            "Top 10 Stations by People Killed",
            fontweight="bold"
        )

        ax.set_xlabel("People Killed")

        plt.tight_layout()

        st.pyplot(fig, width="stretch")

        plt.close(fig)


# ============================================================
# SELECTED STATION DETAILS
# ============================================================

if selected_station != "All Stations" and not filtered_station.empty:

    st.markdown(
        '<div class="section-title">🔎 Selected Station Details</div>',
        unsafe_allow_html=True
    )

    selected_crashes = filtered_station["total_crashes"].sum()

    selected_killed = filtered_station["killed"].sum()

    d1, d2, d3 = st.columns(3)

    with d1:
        st.metric(
            "Selected Station",
            selected_station
        )

    with d2:
        st.metric(
            "Total Crashes",
            f"{selected_crashes:,.0f}"
        )

    with d3:
        st.metric(
            "People Killed",
            f"{selected_killed:,.0f}"
        )


# ============================================================
# VIOLATION ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">🚨 Traffic Violation Analysis</div>',
    unsafe_allow_html=True
)


v1, v2 = st.columns(2)


# ------------------------------------------------------------
# VIOLATION CATEGORIES
# ------------------------------------------------------------

with v1:

    if not violations.empty:

        category_col = None

        for col in [
            "category",
            "Category",
            "violation_category"
        ]:
            if col in violations.columns:
                category_col = col
                break

        cases_col = None

        for col in [
            "cases",
            "Cases",
            "total_cases"
        ]:
            if col in violations.columns:
                cases_col = col
                break

        if category_col and cases_col:

            violation_plot = (
                violations
                .sort_values(
                    cases_col,
                    ascending=False
                )
                .head(10)
            )

            fig, ax = plt.subplots(figsize=(8, 5))

            ax.barh(
                violation_plot[category_col][::-1],
                violation_plot[cases_col][::-1]
            )

            ax.set_title(
                "Major Violation Categories",
                fontweight="bold"
            )

            ax.set_xlabel("Cases")

            plt.tight_layout()

            st.pyplot(fig, width="stretch")

            plt.close(fig)


# ------------------------------------------------------------
# TOP OFFENCES
# ------------------------------------------------------------

with v2:

    if not offences.empty:

        offence_col = None

        for col in [
            "offence",
            "Offence",
            "offense",
            "Offense"
        ]:
            if col in offences.columns:
                offence_col = col
                break

        cases_col = None

        for col in [
            "cases",
            "Cases",
            "total_cases"
        ]:
            if col in offences.columns:
                cases_col = col
                break

        if offence_col and cases_col:

            offence_plot = (
                offences
                .sort_values(
                    cases_col,
                    ascending=False
                )
                .head(10)
            )

            fig, ax = plt.subplots(figsize=(8, 5))

            ax.barh(
                offence_plot[offence_col][::-1],
                offence_plot[cases_col][::-1]
            )

            ax.set_title(
                "Top 10 Traffic Offences",
                fontweight="bold"
            )

            ax.set_xlabel("Cases")

            plt.tight_layout()

            st.pyplot(fig, width="stretch")

            plt.close(fig)


# ============================================================
# YEARLY DATA TABLE
# ============================================================

st.markdown(
    '<div class="section-title">📋 Yearly Data</div>',
    unsafe_allow_html=True
)

display_yearly = filtered_yearly.copy()

st.dataframe(
    display_yearly,
    width="stretch",
    hide_index=True
)


# ============================================================
# DOWNLOAD BUTTON
# ============================================================

csv_data = filtered_yearly.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Yearly Data (CSV)",
    data=csv_data,
    file_name=f"bangalore_road_safety_{start_year}_{end_year}.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Bangalore Road Safety Analytics | "
    "Python • Pandas • Matplotlib • Streamlit | "
    f"Data Period: {min_year}–{max_year}"
)