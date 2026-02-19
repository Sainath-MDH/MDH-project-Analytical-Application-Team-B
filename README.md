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

2.  **Run the Agents**:
    - Data Agent: `python data_agent.py`
    - Analytics Agent: `python analytics_agent.py`
    - Insights Agent: `python insights_agent.py`

3.  **Data Source**:
    - The dashboard automatically looks for `3_Bike_Thefts_FINAL_EXCEL.xlsx` in the root directory.

## Project Structure
- `data_agent.py`: Data cleaning and standardization.
- `analytics_agent.py`: Metric calculation and trend analysis.
- `insights_agent.py`: Natural language insights generation.
- `requirements.txt`: Python dependencies.
- `3_Bike_Thefts_FINAL_EXCEL.xlsx`: Default dataset.
- `data/`: Directory for intermediate JSON results.
