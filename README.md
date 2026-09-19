# 🚦 Bangalore Road Safety Analytics

An end-to-end data analytics project focused on analyzing road crashes, fatalities, police-station-wise incidents, zones, and traffic violations in Bangalore.

## 📌 Project Overview

This project analyzes Bangalore road safety data to identify crash patterns, fatality trends, high-crash police stations, zone-wise incidents, and major traffic violations.

The project includes:

- Data cleaning and preprocessing
- Exploratory data analysis
- Year-wise crash analysis
- Fatality analysis
- Police station analysis
- Zone-wise analysis
- Traffic violation analysis
- Data visualization
- Interactive Streamlit dashboard

## 🛠️ Tech Stack

- **Python**
- **Pandas**
- **Matplotlib**
- **OpenPyXL**
- **Streamlit**
- **Excel**

## 📊 Dashboard Features

The interactive dashboard provides:

- 📅 Year-range filtering
- 📍 Zone filtering
- 🚔 Police station filtering
- 📈 Yearly crash trends
- ⚠️ Fatality trends
- 📉 Fatality rate analysis
- 🗺️ Zone-wise crash analysis
- 🚔 Top police stations by crashes
- 💀 Top police stations by fatalities
- 🚨 Traffic violation analysis
- 📋 Filtered data tables
- ⬇️ CSV download of filtered data

## 📂 Project Structure

```text
Bangalore_road_saftey/
│
├── Dashboard/
│   ├── app.py
│   ├── app_polished_backup.py
│   └── dashboard.py
│
├── Data/
│   ├── analysis.py
│   └── Banglore_road_saftey.xlsx
│
├── charts/
│   ├── crashes_by_year.png
│   ├── deaths_by_year.png
│   ├── fatality_rate_by_year.png
│   ├── top_10_crash_stations.png
│   ├── top_10_death_stations.png
│   ├── top_10_offences.png
│   ├── violation_categories.png
│   └── zone_wise_crashes.png
│
├── requirements.txt
├── README.md
└── road_safety_analysis_results.xlsx
