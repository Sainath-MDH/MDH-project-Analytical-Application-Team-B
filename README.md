# 🚲 Berlin Bike Theft Analytical Application

An advanced, interactive dashboard designed to analyze and visualize bike theft patterns across Berlin (2023–2025). This application transforms raw administrative data into actionable spatial and financial insights.

## 🚀 Key Features

- **Analytics Dashboard**: 
    - Real-time KPI tracking (Total Incidents, Financial Damage).
    - Temporal analysis: Monthly trends, hourly distributions, and weekly "risk" patterns.
    - Composition: Breakdown by bicycle type and offence category.
- **Financial Damage Analysis**: 
    - Granular view of economic impact across 12 Berlin Districts.
    - Detailed breakdown by **Bezirksregion (BZR)** to identify high-value theft hotspots.
- **BZR Area Analysis**: 
    - localized incident counts and multi-year trend comparisons.
    - Area-specific search and filtering.
- **Raw Data Exploration**: 
    - Full searchable table of all incidents.
    - **CSV Export** functionality for further offline analysis.

## 🛠️ Technology Stack

- **Frontend/Dashboard**: [Streamlit](https://streamlit.io/)
- **Data Engineering**: [Pandas](https://pandas.pydata.org/)
- **Visualizations**: [Plotly Express](https://plotly.com/python/plotly-express/)
- **Excel Engine**: [Calamine](https://github.com/tauri-apps/calamine) (for high-speed Excel reading)
- **Architecture**: Modular "Multi-Agent" design for decoupled ETL and Analytics.

## 📂 Project Structure

- `dashboard.py`: Main entry point for the Streamlit UI.
- `data_agent.py`: **ETL Agent** - Handles data cleaning, district mapping (LOR logic), and standardization.
- `analytics_agent.py`: **Processing Agent** - Calculates complex metrics and aggregations.
- `insights_agent.py`: **Reporting Agent** - Prepared for generating natural language insights.
- `data/`: Automated storage for cleaned JSON datasets and dimension maps.
- `berlin_LOR_hierarchy.xlsx`: Reference file for administrative mapping.

## ⚙️ Setup & Running

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

3. **Data Refresh** (Optional):
   The application automatically looks for `3_Bike_Thefts_FINAL_EXCEL.xlsx` in the root directory and regenerates the analytical cache on startup if missing.

---
*Created for the MDH Project - Analytical Application Team B*
