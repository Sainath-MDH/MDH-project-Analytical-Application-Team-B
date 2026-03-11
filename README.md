# **📊 MDH Analytical Application — End‑to‑End Data Insights Platform**

A full‑stack analytical application built to explore, visualize, and interpret multi‑dimensional datasets through an interactive Streamlit interface. The platform provides dynamic dashboards, advanced analytics, and intuitive visualizations designed to support data‑driven decision‑making.

---

## **🎯 Project Overview**

This project delivers a modular analytical application that transforms raw datasets into actionable insights. Users can explore trends, compare metrics, and interact with visual dashboards across multiple analytical pages. The system is built with a clean architecture, scalable components, and a user‑friendly UI.

---

## **🧩 Key Features**

- **Multi‑page Streamlit application** with modular navigation  
- **Interactive dashboards** for exploring trends, distributions, and correlations  
- **Advanced visualizations** using Plotly, Matplotlib, and Seaborn  
- **Dynamic filtering** for real‑time data exploration  
- **Clean, scalable code structure** for easy extension  
- **Fully deployed application** accessible via web interface  
- **Optimized UX** with responsive layouts and intuitive controls  

---

## **🏗️ Architecture**

- `app/Home.py`: Main entry point for the multi-page dashboard.
- `app/pages/`: Modular analytics pages (Overview, Damage, Raw Data).
- `utils/`: Core processing logic:
    - `data_loader.py`: Specialized Excel ingestion using Calamine.
    - `preprocess.py`: ETL, cleaning, and geographic enrichment.
    - `analytics.py`: Computational metrics and aggregations.
    - `insights.py`: Narrative summary generation.
- `data/raw/`: Original administrative datasets.
- `data/processed/`: Automated storage for cleaned JSON repositories.
- `deployment/`: Configuration for cloud hosting.


## **🛠️ Tech Stack**

- **Python**  
- **Streamlit** (multi‑page app framework)  
- **Pandas / NumPy** (data processing)  
- **Plotly / Matplotlib / Seaborn** (visualizations)  
- **GitHub** (version control)  
- **Cloud Deployment** (Streamlit Cloud)  

---

## **🚀 Live Demo**

https://mdh-project-analytical-application-team-b-go3kc3ufrawhegsug8zt.streamlit.app/

---

## **👤 Personal Contributions (Sai)**

Although this was a team project, I independently handled the **core functional and analytical development**, including:

- **Built all analytical pages and modules**  
- **Designed and implemented all visualizations** (Plotly, Seaborn, Matplotlib)  
- **Developed the complete data processing pipeline**  
- **Integrated interactive filters and UI components**  
- **Led the deployment process** (cloud hosting, configuration, testing)  

This effectively represents **end‑to‑end ownership** of the analytical and technical implementation.

---

## **📦 Installation & Running Locally**

```bash
git clone https://github.com/Sainath-MDH/MDH-project-Analytical-Application-Team-B.git
cd MDH-project-Analytical-Application-Team-B
pip install -r requirements.txt
streamlit run app/Home.py
```

---

## **📈 Future Improvements**

- Add machine learning prediction modules  
- Integrate real‑time data sources  
- Add user authentication  
- Improve UI/UX with custom components  
- Expand dataset coverage and domain insights  
