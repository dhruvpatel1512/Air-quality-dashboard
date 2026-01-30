"""
Air Quality Dashboard - Main Streamlit Application

This is the main application file for the UCI Air Quality Dataset dashboard.
Students will work in teams to enhance this dashboard through Git collaboration.
"""

import pip
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from analysis import load_data, clean_data, get_data_summary, calculate_air_quality_metrics
from visualize import (plot_co_over_time, plot_temperature_vs_humidity, 
                      plot_pollutant_distribution, plot_correlation_heatmap,
                      plot_nox_vs_sensor, create_summary_metrics_display,
                      plot_daily_averages)

# Configure the page
st.set_page_config(
    page_title="Air Quality Dashboard",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2E8B57;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #2E8B57;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">Air Quality Dashboard</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    **Welcome to the Air Quality Analysis Dashboard!** 
    
    This dashboard analyzes air quality data from an Italian city monitoring station. 
    The dataset includes various air pollutants and weather variables collected over time.
    """)
    
    # Load and cache data
    @st.cache_data
    def load_and_clean_data():
        """Load and clean the air quality data."""
        raw_data = load_data("data/AirQualityUCI.csv")
        if raw_data is not None:
            return clean_data(raw_data)
        return None
    
    # Load data
    with st.spinner("Loading air quality data..."):
        df = load_and_clean_data()
    
    if df is None:
        st.error("Could not load the air quality dataset. Please check if 'data/AirQualityUCI.csv' exists.")
        return

    # --- Sidebar filters (Feature) -------------------------------------------------
    st.sidebar.header('Filters')
    # Date range filter (uses parsed Date column if present)
    if 'Date' in df.columns and not df['Date'].isna().all():
        min_date = df['Date'].min().date()
        max_date = df['Date'].max().date()
        date_range = st.sidebar.date_input('Date range', value=(min_date, max_date), min_value=min_date, max_value=max_date)
    else:
        date_range = None

    # Pollutant selector (choose which pollutant to display in some charts)
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    pollutant_default = 'CO(GT)' if 'CO(GT)' in numeric_cols else (numeric_cols[0] if numeric_cols else None)
    pollutant = st.sidebar.selectbox('Pollutant for distribution/time series', options=numeric_cols, index=numeric_cols.index(pollutant_default) if pollutant_default in numeric_cols else 0) if numeric_cols else None

    # Apply filters to a working copy of the dataframe used for plots
    df_filtered = df.copy()
    if date_range and isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range
        # convert to datetime for comparison
        df_filtered = df_filtered[(df_filtered['Date'] >= pd.to_datetime(start_date)) & (df_filtered['Date'] <= pd.to_datetime(end_date))]
    
    # Make df_filtered available below for plotting
    
    # Key Metrics - KPI Boxes
    st.markdown('<h2 class="section-header">Key Metrics</h2>', unsafe_allow_html=True)
    
    # Calculate metrics
    metrics = calculate_air_quality_metrics(df)
    display_metrics = create_summary_metrics_display(metrics)
    
    if display_metrics:
        # Display metrics in cards
        cols = st.columns(len(display_metrics))
        
        for i, (metric_name, metric_values) in enumerate(display_metrics.items()):
            with cols[i]:
                st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
                st.subheader(metric_name)
                for key, value in metric_values.items():
                    st.metric(key, value)
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Data preview table
    st.markdown('<h2 class="section-header">Data Preview</h2>', unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True)
    
    # Visualizations
    st.markdown('<h2 class="section-header">Data Visualizations</h2>', unsafe_allow_html=True)
    
    # Base charts as required
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("CO Concentration Over Time")
        # prefer filtered data for plotting
        co_plot = plot_co_over_time(df_filtered)
        if co_plot:
            try:
                st.plotly_chart(co_plot, use_container_width=True)
            except Exception:
                st.pyplot(co_plot)
        else:
            st.warning("No CO data available for plotting")
    
    with col2:
        st.subheader("Temperature vs Absolute Humidity")
        temp_humidity_plot = plot_temperature_vs_humidity(df_filtered)
        if temp_humidity_plot:
            try:
                st.plotly_chart(temp_humidity_plot, use_container_width=True)
            except Exception:
                st.pyplot(temp_humidity_plot)
        else:
            st.warning("No temperature/humidity data available for plotting")
    
    # Additional visualizations
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("CO Distribution")
        # Use selected pollutant for distribution
        if pollutant:
            co_dist_plot = plot_pollutant_distribution(df_filtered, pollutant)
        else:
            co_dist_plot = None
        if co_dist_plot:
            try:
                st.plotly_chart(co_dist_plot, use_container_width=True)
            except Exception:
                st.pyplot(co_dist_plot)
    
    with col4:
        st.subheader("NOx(GT) vs Sensor Value")
        nox_plot = plot_nox_vs_sensor(df_filtered)
        if nox_plot:
            try:
                st.plotly_chart(nox_plot, use_container_width=True)
            except Exception:
                st.pyplot(nox_plot)
        else:
            st.warning("No NOx data available for plotting")
    
    # Correlation heatmap
    st.subheader("Correlation Heatmap")
    corr_plot = plot_correlation_heatmap(df_filtered)
    if corr_plot:
        try:
            st.plotly_chart(corr_plot, use_container_width=True)
        except Exception:
            st.pyplot(corr_plot)

    # New interactive daily average pollutant plot
    st.markdown('<h2 class="section-header">Daily Average - Selected Pollutant</h2>', unsafe_allow_html=True)
    if pollutant:
        daily_plot = None
        try:
            daily_plot = plot_daily_averages(df_filtered, pollutant)
        except Exception:
            daily_plot = None

        if daily_plot is not None:
            try:
                st.plotly_chart(daily_plot, use_container_width=True)
            except Exception:
                st.pyplot(daily_plot)
        else:
            st.info('No daily average data available for the selected pollutant')

if __name__ == "__main__":
    main()