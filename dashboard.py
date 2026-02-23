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
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1c2c 100%);
        color: #ffffff;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border: 1px solid #30363d;
    }
    .stDataFrame {
        border: 1px solid #30363d;
        border-radius: 5px;
    }
    h1, h2, h3 {
        color: #00d4ff;
    }
    .stSidebar {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    # Run agents if data doesn't exist
    if not os.path.exists('data/thefts_clean.json'):
        with st.spinner("Processing raw data..."):
            process_data("3_Bike_Thefts_FINAL_EXCEL.xlsx")
            run_analytics()
    
    with open('data/thefts_clean.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open('data/analytics_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
        
    return pd.DataFrame(data), results

def render_analytics_page(filtered_df):
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
        fig_trend.update_layout(showlegend=False)
        st.plotly_chart(fig_trend, use_container_width=True)

    with c2:
        st.subheader("Thefts by District")
        dist_df = filtered_df.groupby('district').size().reset_index(name='count').sort_values('count', ascending=False).head(10)
        fig_dist = px.bar(dist_df, x='count', y='district', orientation='h',
                        labels={'count': 'Number of Thefts', 'district': 'District'},
                        template="plotly_dark",
                        color='count',
                        color_continuous_scale='Blues')
        fig_dist.update_layout(showlegend=False)
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
        fig_bike.update_layout(showlegend=False)
        st.plotly_chart(fig_bike, use_container_width=True)

    with c4:
        st.subheader("Hourly Distribution")
        hour_df = filtered_df.groupby('start_hour').size().reset_index(name='count')
        fig_hour = px.bar(hour_df, x='start_hour', y='count',
                        labels={'count': 'Number of Thefts', 'start_hour': 'Hour of Day'},
                        template="plotly_dark",
                        color_discrete_sequence=['#ffaa00'])
        fig_hour.update_layout(showlegend=False)
        st.plotly_chart(fig_hour, use_container_width=True)

    # Weekly Pattern
    st.subheader("Weekly Distribution")
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # Check if weekday values exist in data
    if 'weekday' in filtered_df.columns and not filtered_df.empty:
        week_df = filtered_df.groupby('weekday').size().reindex(day_order).reset_index(name='count')
        fig_week = px.line_polar(week_df, r='count', theta='weekday', line_close=True,
                                template="plotly_dark",
                                color_discrete_sequence=['#00ffa2'])
        fig_week.update_traces(fill='toself')
        fig_week.update_layout(showlegend=False)
        st.plotly_chart(fig_week, use_container_width=True)
    else:
        st.info("No weekday data available for the current selection.")

def render_raw_data_page(filtered_df):
    st.subheader("📋 Raw Incident Data")
    st.markdown("Downloadable table of all filtered bike theft records.")
    
    # Add a search bar for the table
    search_query = st.text_input("Search in data...", "")
    
    display_df = filtered_df
    if search_query:
        # Simple string matching across all columns
        mask = display_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        display_df = display_df[mask]

    st.dataframe(display_df, use_container_width=True, height=600)
    
    st.download_button(
        label="Download Filtered Data as CSV",
        data=display_df.to_csv(index=False).encode('utf-8'),
        file_name="berlin_bike_thefts_filtered.csv",
        mime="text/csv",
    )

def render_damage_analysis_page(filtered_df):
    st.subheader("💰 Financial Damage Analysis")
    st.markdown("Detailed breakdown of financial losses by District and Bezirksregion (BZR).")

    if filtered_df.empty:
        st.warning("No data available for the current filters.")
        return

    # Local District Filter (Dropdown + Search)
    st.markdown("---")
    dist_all = sorted(filtered_df['district'].unique().tolist())
    
    col_f1, col_f2 = st.columns([1, 1])
    with col_f1:
        selected_local_dist = st.selectbox("🏘️ Filter by District (Dropdown)", ["All Districts"] + dist_all)
    with col_f2:
        local_search = st.text_input("🔍 Search District", "", help="Type to filter by district name")
    st.markdown("---")

    # Apply local filters
    local_filtered = filtered_df
    if selected_local_dist != "All Districts":
        local_filtered = local_filtered[local_filtered['district'] == selected_local_dist]
    if local_search:
        local_filtered = local_filtered[local_filtered['district'].str.contains(local_search, case=False, na=False)]

    if local_filtered.empty:
        st.warning("No data found for the selected local filters.")
        return

    # KPI Metrics for Damage Analysis
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric("Total Damage", f"€{local_filtered['damage'].sum():,.2f}")
    with kpi2:
        top_dist = local_filtered.groupby('district')['damage'].sum().idxmax()
        st.metric("Top Damage District", top_dist)
    with kpi3:
        top_bzr = local_filtered.groupby('bzr_name')['damage'].sum().idxmax()
        st.metric("Top Damage BZR", top_bzr)

    st.divider()

    # Aggregate data for the table and chart
    summary_df = local_filtered.groupby(['district', 'bzr_name'])['damage'].sum().reset_index()
    summary_df = summary_df.sort_values(['damage'], ascending=False)
    summary_df.columns = ['District', 'BZR Name', 'Total Financial Damage (€)']
    
    # 1. Bar Graph: Damage by BZR Name
    st.subheader("Total Damage Cost (€) by Area")
    # Show top 20 or all if smaller
    top_plot_df = summary_df.head(20)
    fig_bzr_damage = px.bar(
        top_plot_df,
        x='Total Financial Damage (€)',
        y='BZR Name',
        color='District',
        orientation='h',
        title=f"Top {len(top_plot_df)} Areas by Financial Damage",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_bzr_damage.update_layout(showlegend=False)
    st.plotly_chart(fig_bzr_damage, use_container_width=True)

    st.divider()

    # 2. Tabular Damage Summary
    st.subheader("📋 Damage Summary Data")
    st.dataframe(
        summary_df.style.format({'Total Financial Damage (€)': '€{:,.2f}'}),
        use_container_width=True,
        height=500
    )

def render_bzr_analysis_page(filtered_df):
    st.subheader("🏘️ BZR Area Analysis")
    st.markdown("Incident distribution and trends by Bezirksregion (BZR).")

    if filtered_df.empty:
        st.warning("No data available.")
        return

    # Local District Filter (Dropdown + Search)
    st.markdown("---")
    dist_all = sorted(filtered_df['district'].unique().tolist())
    
    col_f1, col_f2 = st.columns([1, 1])
    with col_f1:
        selected_local_dist = st.selectbox("🏘️ Filter by District (Dropdown)", ["All Districts"] + dist_all, key="bzr_dist_sel")
    with col_f2:
        local_search = st.text_input("🔍 Search District", "", key="bzr_dist_search", help="Type to filter by district name")
    st.markdown("---")

    # Apply local filters
    local_filtered = filtered_df
    if selected_local_dist != "All Districts":
        local_filtered = local_filtered[local_filtered['district'] == selected_local_dist]
    if local_search:
        local_filtered = local_filtered[local_filtered['district'].str.contains(local_search, case=False, na=False)]

    if local_filtered.empty:
        st.warning("No data found for the selected local filters.")
        return

    # Aggregate for table and metrics
    bzr_summary = local_filtered.groupby(['bzr_name', 'district']).size().reset_index(name='Incident Count')
    bzr_summary = bzr_summary.sort_values('Incident Count', ascending=False)
    bzr_summary.columns = ['BZR Name', 'District', 'Number of Incidents']

    # KPI Metrics for BZR Analysis
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric("Total Incidents", f"{len(local_filtered):,}")
    with kpi2:
        top_inc_bzr = bzr_summary.iloc[0]['BZR Name'] if not bzr_summary.empty else "N/A"
        st.metric("Top Incident BZR", top_inc_bzr)
    with kpi3:
        total_dist_count = local_filtered['district'].nunique()
        st.metric("Districts Covered", total_dist_count)

    st.divider()

    # 1. Incident Summary Table by BZR
    st.subheader("📋 Incident Count by Area")
    st.dataframe(bzr_summary, use_container_width=True, height=400)

    st.divider()

    # 2. Monthly Trends (Multi-Year Comparison)
    st.subheader("📈 Multi-Year Monthly Incident Trends")
    st.markdown("Comparing monthly bike theft trends across different years.")
    
    # Aggregate data by Year and Month
    trend_counts = local_filtered.groupby(['year', 'month']).size().reset_index(name='count')
    
    if not trend_counts.empty:
        # Sort months and map names
        month_names = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 
                       7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
        
        trend_counts['Month Name'] = trend_counts['month'].map(month_names)
        trend_counts['year'] = trend_counts['year'].astype(str) # For categorical coloring
        
        # Ensure sequential sorting by month for the line chart
        trend_counts = trend_counts.sort_values(['year', 'month'])
        
        fig_trend = px.line(
            trend_counts,
            x='Month Name',
            y='count',
            color='year',
            markers=True,
            labels={'count': 'Number of Incidents', 'Month Name': 'Month', 'year': 'Year'},
            title="Monthly Incident Trends (Yearly Comparison)",
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        
        # Improve layout
        fig_trend.update_layout(xaxis={'categoryorder':'array', 'categoryarray':list(month_names.values())}, showlegend=False)
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("No trend data available for the current selection.")

def render_filters(df):
    """Render global filters in a horizontal header layout."""
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader("📅 Time Period")
        min_date, max_date = df['start_date_dt'].min().date(), df['start_date_dt'].max().date()
        date_range = st.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date, label_visibility="collapsed")
    
    with col2:
        st.subheader("🏙️ District")
        districts = sorted(df['district'].unique().tolist())
        selected_districts = st.multiselect("Districts", districts, default=districts, label_visibility="collapsed")
    
    with col3:
        st.subheader("🚲 Bike Type")
        bike_types = sorted(df['bike_type'].unique().tolist())
        selected_bikes = st.multiselect("Bike Types", bike_types, default=bike_types, label_visibility="collapsed")
        
    with col4:
        st.subheader("🔍 Offence Type")
        offence_types = sorted(df['offence_type'].unique().tolist())
        selected_offences = st.multiselect("Offence Types", offence_types, default=offence_types, label_visibility="collapsed")
    st.markdown("---")

    return date_range, selected_districts, selected_bikes, selected_offences

def main():
    st.title("🚲 Berlin Bike Theft Analytics")
    st.markdown("### Interactive Dashboard for Crime Analysis (2023 - 2025)")

    try:
        df, analytics = load_data()
        # Convert start_date to datetime for filtering
        df['start_date_dt'] = pd.to_datetime(df['start_date'])
    except Exception as e:
        st.error(f"Error loading data: {e}. Please ensure '3_Bike_Thefts_FINAL_EXCEL.xlsx' is in the project root.")
        return

    # Sidebar Navigation Only
    st.sidebar.markdown("## 📍 Navigation")
    page = st.sidebar.radio("Select View", ["Analytics Dashboard", "Damage Analysis", "BZR Analysis", "Raw Data"], label_visibility="collapsed")

    # Render Filters ONLY on the Raw Data page
    if page == "Raw Data":
        date_range, selected_districts, selected_bikes, selected_offences = render_filters(df)
    else:
        # Provide default "all" values when filters are hidden
        date_range = (df['start_date_dt'].min().date(), df['start_date_dt'].max().date())
        selected_districts = df['district'].unique().tolist()
        selected_bikes = df['bike_type'].unique().tolist()
        selected_offences = df['offence_type'].unique().tolist()

    # Final Filtering Logic
    mask = (df['district'].isin(selected_districts)) & (df['bike_type'].isin(selected_bikes)) & (df['offence_type'].isin(selected_offences))
    
    # Apply date range mask if range is valid
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        mask &= (df['start_date_dt'].dt.date >= start_date) & (df['start_date_dt'].dt.date <= end_date)
    
    filtered_df = df[mask]

    if page == "Analytics Dashboard":
        render_analytics_page(filtered_df)
    elif page == "Damage Analysis":
        render_damage_analysis_page(filtered_df)
    elif page == "BZR Analysis":
        render_bzr_analysis_page(filtered_df)
    elif page == "Raw Data":
        render_raw_data_page(filtered_df)

if __name__ == "__main__":
    main()




