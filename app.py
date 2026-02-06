"""
Air Quality Dashboard - Main Streamlit Application

This is the main application file for the UCI Air Quality Dataset dashboard.
Students will work in teams to enhance this dashboard through Git collaboration.
"""


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from analysis import load_data, clean_data, get_data_summary, calculate_air_quality_metrics
from visualize import (plot_co_over_time, plot_temperature_vs_humidity, 
                      plot_pollutant_distribution, plot_correlation_heatmap,
                      plot_nox_vs_sensor, create_summary_metrics_display)

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
    
    # Clear Streamlit cached data to ensure latest cleaning is used (development only)
    st.cache_data.clear()

    # Load data
    with st.spinner("Loading air quality data..."):
        df = load_and_clean_data()

    
    if df is None:
        st.error("Could not load the air quality dataset. Please check if 'data/AirQualityUCI.csv' exists.")
        return
    
    # Data Cleaning   
    # Convert invalid placeholders to proper nulls
    df = df.replace(-200, pd.NA)

    # Define critical columns that must exist
    key_cols = [c for c in ['CO(GT)', 'NOx(GT)', 'T', 'AH'] if c in df.columns]

    # Drop rows missing critical sensor values
    df = df.dropna(subset=key_cols)

    # Fill remaining numeric nulls EXCEPT target pollutants (to avoid skewing distributions)
    exclude_cols = [c for c in ['CO(GT)', 'NOx(GT)'] if c in df.columns]
    num_cols = [c for c in df.select_dtypes(include='number').columns if c not in exclude_cols]

    df[num_cols] = df[num_cols].fillna(df[num_cols].median())


    # Treat -200 values as missing data (NaN)
    #df = df.replace(-200, pd.NA)

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
        co_plot = plot_co_over_time(df)
        if co_plot:
            st.pyplot(co_plot)
        else:
            st.warning("No CO data available for plotting")
    
    with col2:
        st.subheader("Temperature vs Absolute Humidity")
        temp_humidity_plot = plot_temperature_vs_humidity(df)
        if temp_humidity_plot:
            st.pyplot(temp_humidity_plot)
        else:
            st.warning("No temperature/humidity data available for plotting")
    
    # Additional visualizations
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("CO Distribution")
        co_dist_plot = plot_pollutant_distribution(df, 'CO(GT)')
        if co_dist_plot:
            st.pyplot(co_dist_plot)
    
    with col4:
        st.subheader("NOx(GT) vs Sensor Value")
        nox_plot = plot_nox_vs_sensor(df)
        if nox_plot:
            st.pyplot(nox_plot)
        else:
            st.warning("No NOx data available for plotting")
    
    # Correlation heatmap
    st.subheader("Correlation Heatmap")
    corr_plot = plot_correlation_heatmap(df)
    if corr_plot:
        st.pyplot(corr_plot)

if __name__ == "__main__":
    main()
