# MDH-project-Analytical-Application-Team-B
# README – Bike Thefts Web Analytics Dashboard

## 1. Project Overview

This project delivers a web-based analytical dashboard built on the daily updated bike thefts dataset contained in `3-Bike-Thefts-FINAL-EXCEL.xlsx`. The dashboard helps stakeholders understand patterns of bike thefts and monitor key metrics over time to support prevention, planning, and decision‑making.

## 2. Dataset

The data source is an Excel/CSV export that is updated daily from the underlying bike theft reporting system. Each row represents a single reported bike theft, with columns such as incident details, date and time, location, bike characteristics, and case status (exact column names depend on the source system).

## 3. Scope and Objectives

The scope is to design and implement an end‑to‑end analytics solution consisting of:

- A data ingestion pipeline that loads daily CSV exports into the system.  
- A transformation and calculation layer that cleans data, standardizes formats, and computes derived metrics (e.g. daily counts, rolling averages, hotspot indicators, recovery rates).  
- A web‑based visualization layer with charts, tables, and interactive controls that allows non‑technical users to explore the data intuitively.  

The goal is to provide a **user‑centered** dashboard that improves on a previous Tableau proof of concept by refining dashboard composition, visual design, interaction, and the relevance of metrics to real user questions.

## 4. Architecture

### 4.1 Data Ingestion

- Input format: Daily CSV export derived from `3-Bike-Thefts-FINAL-EXCEL.xlsx` or its equivalent.  
- Process:  
  - Automated scheduled import (e.g. daily) from a designated directory or data source.  
  - Schema validation to ensure column consistency over time.  
  - Logging of successful and failed ingestions for monitoring.  

### 4.2 Transformation & Calculation Layer

- Data cleaning: handle missing values, normalize dates/times, standardize location fields, and ensure consistent coding of categories (e.g. bike types, outcomes).  
- Derived metrics (examples):  
  - Daily, weekly, monthly theft counts.  
  - Theft density by area or neighborhood.  
  - Average and median bike value per segment.  
  - Recovery and resolution rates.  
  - Trend indicators (e.g. week‑over‑week or year‑over‑year change).  

The transformation layer is implemented to be modular so that new calculated fields can be added without disrupting existing dashboards.

### 4.3 Visualisation Layer (Web Dashboard)

The web application exposes an interactive dashboard composed of:

- KPI cards for high‑level metrics (e.g. total thefts, thefts in the last 7 days, recovery rate, average bike value).  
- Time‑series charts showing thefts over time with options to drill down by day, week, or month.  
- Geographic or area‑based visualisations (where location data supports it), highlighting hotspots.  
- Breakdown charts (bar, stacked bar, or similar) by bike type, location type, time of day, and outcome.  
- Detailed tables with filtering, sorting, and search to inspect individual incidents.  
- Interactive controls (filters and slicers) for date range, location, bike type, and other key dimensions.
## 5. User‑Centered Design

The dashboard builds on a previous Tableau project used as a proof of concept, but improves it from a user‑centered perspective:

- Dashboard composition: logical grouping of views into overview, trends, location, and detail sections.  
- Visualisation choices: charts and metrics selected to answer real user questions (e.g. “Where are thefts increasing?”, “What time of day is riskiest?”).  
- Metrics: focus on meaningful, interpretable measures instead of technically complex but opaque indicators.  
- Usability: clear titles, concise labels, helpful tooltips, and responsive interactions across devices where feasible. 

Regular feedback cycles with end users (e.g. analysts, planners, law enforcement, community stakeholders) guide layout and feature decisions to ensure the tool fits their workflows.

## 6. Agile Delivery Process

The project follows an agile, iterative approach:

- Short sprints with a prioritized backlog of user stories, such as:  
  - “As a planner, I want to see theft trends by district so I can allocate resources.”  
  - “As an analyst, I want to filter by bike type and time of day to discover risk patterns.”  
- Incremental feature growth:  
  - Experimental: initial prototypes and quick visual explorations, often inspired by the original Tableau project.  
  - MVP: a stable version with core ingestion, basic transformations, and the main dashboard views.  
  - Extended functionality: advanced filters, new metrics, additional pages, and performance optimizations based on user feedback.
Backlog grooming, sprint reviews, and demos ensure continuous alignment with user needs and data realities.

## 7. Getting Started

1. Place the latest CSV export derived from `3-Bike-Thefts-FINAL-EXCEL.xlsx` into the configured input location.
2. Run or schedule the ingestion job to load the data into the system.  
3. Deploy or start the web application server.  
4. Access the dashboard via your browser, select a date range, and begin exploring the data with the available filters and views.
## 8. Future Enhancements

Potential extensions include:

- Integration with live data sources or APIs to reduce manual CSV handling.  
- More advanced spatial analysis, such as heatmaps or clustering of theft hotspots.  
- Predictive models to forecast theft risk under different conditions.  
- Role‑based access and personalized views for different user groups.
***

You can copy this README into a `README.md` file in your project and adapt section titles, technical stack details, and metric definitions to match your actual implementation.
