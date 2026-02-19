import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from data_agent import process_data
from analytics_agent import run_analytics

# Set page config
st.set_page_config(
    page_title="Berlin Bike Theft Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #00d4ff;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    # Run agents if data doesn't exist
    if not os.path.exists('data/thefts_clean.json'):
        with st.spinner("Processing raw data..."):
            process_data("3_Bike_Thefts_FINAL_EXCEL.xlsx")
            run_analytics()
    
    with open('data/thefts_clean.json', 'r') as f:
        data = json.load(f)
    
    with open('data/analytics_results.json', 'r') as f:
        results = json.load(f)
        
    return pd.DataFrame(data), results

def main():
    st.title("🚲 Berlin Bike Theft Analytics")
    st.markdown("### Interactive Dashboard for Crime Analysis (2023 - 2025)")

    try:
        df, analytics = load_data()
    except Exception as e:
        st.error(f"Error loading data: {e}. Please ensure '3_Bike_Thefts_FINAL_EXCEL.xlsx' is in the project root.")
        return

    # Sidebar Filters
    st.sidebar.header("Filters")
    districts = sorted(df['district'].unique().tolist())
    selected_districts = st.sidebar.multiselect("Select Districts", districts, default=districts[:5])
    
    bike_types = sorted(df['bike_type'].unique().tolist())
    selected_bikes = st.sidebar.multiselect("Select Bike Types", bike_types, default=bike_types)

    # Filter data
    filtered_df = df[
        (df['district'].isin(selected_districts)) & 
        (df['bike_type'].isin(selected_bikes))
    ]

    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Incidents", f"{len(filtered_df):,}")
    with col2:
        total_damage = filtered_df['damage'].sum()
        st.metric("Total Damage", f"€{total_damage:,.2f}")
    with col3:
        avg_damage = filtered_df['damage'].mean()
        st.metric("Avg. Damage", f"€{avg_damage:,.2f}")
    with col4:
        most_common_hour = filtered_df['start_hour'].mode()[0] if not filtered_df.empty else "N/A"
        st.metric("Peak Hour", f"{most_common_hour}:00")

    st.divider()

    # Charts Row 1
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Monthly Incident Trend")
        trend_df = filtered_df.groupby('start_date').size().reset_index(name='count')
        fig_trend = px.line(trend_df, x='start_date', y='count', 
                          labels={'count': 'Number of Thefts', 'start_date': 'Date'},
                          template="plotly_dark",
                          color_discrete_sequence=['#00d4ff'])
        st.plotly_chart(fig_trend, use_container_width=True)

    with c2:
        st.subheader("Thefts by District")
        dist_df = filtered_df.groupby('district').size().reset_index(name='count').sort_values('count', ascending=False).head(10)
        fig_dist = px.bar(dist_df, x='count', y='district', orientation='h',
                        labels={'count': 'Number of Thefts', 'district': 'District'},
                        template="plotly_dark",
                        color='count',
                        color_continuous_scale='Blues')
        st.plotly_chart(fig_dist, use_container_width=True)

    # Charts Row 2
    c3, c4 = st.columns(2)
    
    with c3:
        st.subheader("Bike Type Distribution")
        bike_df = filtered_df.groupby('bike_type').size().reset_index(name='count')
        fig_bike = px.pie(bike_df, values='count', names='bike_type', 
                        template="plotly_dark",
                        hole=0.4,
                        color_discrete_sequence=px.colors.sequential.Tealgrn)
        st.plotly_chart(fig_bike, use_container_width=True)

    with c4:
        st.subheader("Hourly Distribution")
        hour_df = filtered_df.groupby('start_hour').size().reset_index(name='count')
        fig_hour = px.bar(hour_df, x='start_hour', y='count',
                        labels={'count': 'Number of Thefts', 'start_hour': 'Hour of Day'},
                        template="plotly_dark",
                        color_discrete_sequence=['#ffaa00'])
        st.plotly_chart(fig_hour, use_container_width=True)

    # Weekly Pattern
    st.subheader("Weekly Distribution")
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    week_df = filtered_df.groupby('weekday').size().reindex(day_order).reset_index(name='count')
    fig_week = px.line_polar(week_df, r='count', theta='weekday', line_close=True,
                           template="plotly_dark",
                           color_discrete_sequence=['#00ffa2'])
    fig_week.update_traces(fill='toself')
    st.plotly_chart(fig_week, use_container_width=True)

    # Data Table
    if st.checkbox("Show Raw Data"):
        st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()




