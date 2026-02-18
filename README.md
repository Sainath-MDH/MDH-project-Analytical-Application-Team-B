# Bike Theft Analytical Dashboard

This project provides an interactive dashboard to analyze bike theft data, identifying trends, hotspots, and key metrics.

## Features
- **Auto-Detection**: Automatically identifies date, categorical, and numeric fields in your data.
- **Interactive Visualizations**:
    - **Trends**: Line charts showing incidents over time (Daily/Weekly/Monthly).
    - **Composition**: Bar and Pie charts for categorical breakdowns (e.g., Bike Type, Location).
    - **KPIs**: Immediate view of total incidents and financial impact.
- **Filtering**:
    - Filter by Date Range.
    - Filter by Categories (e.g., Status, Region).

## Setup & Running

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Dashboard**:
    ```bash
    streamlit run dashboard.py
    ```

3.  **Data Source**:
    - The dashboard automatically looks for `3 Bike Thefts  FINAL EXCEL.xlsx` in the root directory.
    - You can also upload your own Excel (`.xlsx`) or CSV (`.csv`) file via the sidebar.

## Project Structure
- `dashboard.py`: Main application logic.
- `requirements.txt`: Python dependencies.
- `3 Bike Thefts  FINAL EXCEL.xlsx`: Default dataset.
