import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# PATH
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULT_FILE = PROJECT_DIR / "road_safety_analysis_results.xlsx"

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
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Main content */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Header */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0;
        color: #172033;
    }

    .subtitle {
        font-size: 17px;
        color: #667085;
        margin-top: 5px;
        margin-bottom: 25px;
    }

    /* KPI cards */
    .kpi-card {
        background: white;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #e4e7ec;
        box-shadow: 0 4px 14px rgba(16, 24, 40, 0.06);
        min-height: 125px;
    }

    .kpi-title {
        font-size: 14px;
        font-weight: 600;
        color: #667085;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 30px;
        font-weight: 800;
        color: #101828;
    }

    /* Section headers */
    .section-title {
        font-size: 23px;
        font-weight: 750;
        color: #172033;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    .section-subtitle {
        color: #667085;
        font-size: 14px;
        margin-bottom: 15px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Info box */
    .filter-box {
        background: white;
        padding: 12px 18px;
        border-radius: 10px;
        border-left: 4px solid #344054;
        margin-bottom: 20px;
        color: #344054;
    }

</style>
""", unsafe_allow_html=True)

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

    violation = pd.read_excel(
        RESULT_FILE,
        sheet_name="Violation Categories"
    )

    offence = pd.read_excel(
        RESULT_FILE,
        sheet_name="Offence Analysis"
    )

    return yearly, station, zone, violation, offence


yearly, station, zone, violation, offence = load_data()

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## 🚦 ROAD SAFETY")
st.sidebar.markdown("---")

st.sidebar.markdown("### Dashboard Filters")

min_year = int(yearly["year"].min())
max_year = int(yearly["year"].max())

selected_years = st.sidebar.slider(
    "Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Bangalore Road Safety Analytics"
)

st.sidebar.caption(
    "Data period: 2007–2025"
)

# ============================================================
# FILTER YEARLY DATA
# ============================================================

filtered_yearly = yearly[
    (yearly["year"] >= selected_years[0]) &
    (yearly["year"] <= selected_years[1])
].copy()

# ============================================================
# FILTER INFORMATION
# ============================================================

total_crashes = filtered_yearly["total_crashes"].sum()
total_fatal = filtered_yearly["fatal_crashes"].sum()
total_killed = filtered_yearly["killed"].sum()
total_non_fatal = filtered_yearly["non_fatal_crashes"].sum()

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🚦 Bangalore Road Safety Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Road crash, fatality, police station, zone and traffic violation analysis'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="filter-box">
        <b>Selected period:</b> {selected_years[0]} – {selected_years[1]}
        &nbsp;&nbsp; | &nbsp;&nbsp;
        <b>Years included:</b> {len(filtered_yearly)}
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# KPI CARDS
# ============================================================

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">TOTAL CRASHES</div>
            <div class="kpi-value">{total_crashes:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">FATAL CRASHES</div>
            <div class="kpi-value">{total_fatal:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">PEOPLE KILLED</div>
            <div class="kpi-value">{total_killed:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">NON-FATAL CRASHES</div>
            <div class="kpi-value">{total_non_fatal:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# YEARLY TRENDS
# ============================================================

st.markdown(
    '<div class="section-title">📈 Crash & Fatality Trends</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Annual road crash and fatality patterns for the selected period'
    '</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns(2)

with c1:

    fig, ax = plt.subplots(figsize=(8, 4.5))

    ax.plot(
        filtered_yearly["year"],
        filtered_yearly["total_crashes"],
        marker="o",
        linewidth=2
    )

    ax.set_title("Total Crashes by Year", fontsize=15)
    ax.set_xlabel("Year")
    ax.set_ylabel("Crashes")
    ax.grid(True, alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


with c2:

    fig, ax = plt.subplots(figsize=(8, 4.5))

    ax.bar(
        filtered_yearly["year"],
        filtered_yearly["killed"]
    )

    ax.set_title("People Killed by Year", fontsize=15)
    ax.set_xlabel("Year")
    ax.set_ylabel("People Killed")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ============================================================
# ZONE ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">🗺️ Zone-Level Analysis</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns(2)

with c1:

    fig, ax = plt.subplots(figsize=(8, 4.5))

    ax.bar(
        zone["zone"],
        zone["total_crashes"]
    )

    ax.set_title("Total Crashes by Zone", fontsize=15)
    ax.set_xlabel("Zone")
    ax.set_ylabel("Crashes")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


with c2:

    fig, ax = plt.subplots(figsize=(8, 4.5))

    ax.bar(
        zone["zone"],
        zone["killed"]
    )

    ax.set_title("People Killed by Zone", fontsize=15)
    ax.set_xlabel("Zone")
    ax.set_ylabel("People Killed")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ============================================================
# STATION ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">🚨 High-Risk Police Stations</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns(2)

with c1:

    st.markdown("#### Top 10 Stations by Total Crashes")

    top_crash = (
        station
        .sort_values("total_crashes", ascending=False)
        .head(10)
        .sort_values("total_crashes")
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(
        top_crash["station"],
        top_crash["total_crashes"]
    )

    ax.set_xlabel("Total Crashes")
    ax.set_ylabel("Police Station")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


with c2:

    st.markdown("#### Top 10 Stations by People Killed")

    top_death = (
        station
        .sort_values("killed", ascending=False)
        .head(10)
        .sort_values("killed")
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(
        top_death["station"],
        top_death["killed"]
    )

    ax.set_xlabel("People Killed")
    ax.set_ylabel("Police Station")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ============================================================
# VIOLATIONS
# ============================================================

st.markdown(
    '<div class="section-title">🚦 Traffic Violation Analysis</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns(2)

with c1:

    st.markdown("#### Violation Categories")

    top_violation = (
        violation
        .sort_values("total_cases", ascending=False)
        .head(10)
        .sort_values("total_cases")
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(
        top_violation["category"],
        top_violation["total_cases"]
    )

    ax.set_xlabel("Cases")
    ax.set_ylabel("Category")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


with c2:

    st.markdown("#### Top 10 Traffic Offences")

    top_offence = (
        offence
        .sort_values("total_cases", ascending=False)
        .head(10)
        .sort_values("total_cases")
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(
        top_offence["offence"],
        top_offence["total_cases"]
    )

    ax.set_xlabel("Cases")
    ax.set_ylabel("Offence")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ============================================================
# YEARLY DATA TABLE
# ============================================================

st.markdown(
    '<div class="section-title">📊 Detailed Yearly Data</div>',
    unsafe_allow_html=True
)

st.dataframe(
    filtered_yearly,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Bangalore Road Safety Analytics | "
    "Python • Pandas • Matplotlib • Streamlit"
)