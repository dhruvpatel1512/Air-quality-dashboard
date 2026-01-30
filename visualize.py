"""
Visualization functions for the UCI Air Quality Dataset.

This module contains functions for creating charts and plots
to visualize air quality data patterns and relationships.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def plot_co_over_time(df, title="CO(GT) Concentration Over Time"):
    """
    Create a line plot showing CO concentration over time.
    
    Args:
        df (pd.DataFrame): Cleaned dataset with DateTime column
        title (str): Chart title
        
    Returns:
        matplotlib.figure.Figure: The plot figure
    """
    if df is None or 'CO(GT)' not in df.columns:
        return None
    
    # Filter out missing values
    plot_data = df[['DateTime', 'CO(GT)']].dropna()
    
    # Additional filter to remove NaT values from DateTime
    plot_data = plot_data[plot_data['DateTime'].notna()]
    
    if plot_data.empty:
        return None
    
    # Return a Plotly interactive line chart for CO over time
    fig = px.line(plot_data, x='DateTime', y='CO(GT)', title=title, labels={'CO(GT)': 'CO (mg/m³)', 'DateTime': 'Date'})
    fig.update_traces(line=dict(color='#2E8B57'))
    fig.update_layout(hovermode='x unified', template='plotly_white')
    return fig


def plot_temperature_vs_humidity(df, title="Temperature vs Absolute Humidity"):
    """
    Create a scatter plot showing relationship between temperature and absolute humidity.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        title (str): Chart title
        
    Returns:
        matplotlib.figure.Figure: The plot figure
    """
    if df is None or 'T' not in df.columns or 'AH' not in df.columns:
        return None
    
    # Filter out missing values
    plot_data = df[['T', 'AH']].dropna()
    
    if plot_data.empty:
        return None
    
    # Use Plotly scatter for interactivity
    fig = px.scatter(plot_data, x='T', y='AH', color='T', color_continuous_scale='viridis',
                     title=title, labels={'T': 'Temperature (°C)', 'AH': 'Absolute Humidity'})
    fig.update_layout(template='plotly_white', hovermode='closest')
    return fig


def plot_pollutant_distribution(df, pollutant='CO(GT)', title=None):
    """
    Create a histogram showing the distribution of a pollutant.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        pollutant (str): Name of the pollutant column
        title (str): Chart title
        
    Returns:
        matplotlib.figure.Figure: The plot figure
    """
    if df is None or pollutant not in df.columns:
        return None
    
    # Filter out missing values
    plot_data = df[pollutant].dropna()
    
    if plot_data.empty:
        return None
    
    if title is None:
        title = f"Distribution of {pollutant}"
    
    # Interactive histogram with Plotly
    fig = px.histogram(plot_data, x=plot_data, nbins=50, title=title, labels={'value': pollutant})
    mean_val = plot_data.mean()
    median_val = plot_data.median()
    fig.add_vline(x=mean_val, line_dash='dash', line_color='red', annotation_text=f'Mean: {mean_val:.2f}', annotation_position='top left')
    fig.add_vline(x=median_val, line_dash='dash', line_color='blue', annotation_text=f'Median: {median_val:.2f}', annotation_position='top right')
    fig.update_layout(template='plotly_white')
    return fig


def plot_correlation_heatmap(df, title="Air Quality Variables Correlation"):
    """
    Create a correlation heatmap for numeric variables.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        title (str): Chart title
        
    Returns:
        matplotlib.figure.Figure: The plot figure
    """
    if df is None:
        return None
    
    # Select only numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) < 2:
        return None
    
    # Calculate correlation matrix
    corr_matrix = df[numeric_cols].corr()
    
    # Use Plotly heatmap for interactivity
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns.tolist(),
        y=corr_matrix.index.tolist(),
        colorscale='RdBu', zmid=0,
        colorbar=dict(lenmode='fraction', len=0.8)
    ))
    fig.update_layout(title=title, template='plotly_white', autosize=True)
    return fig


def plot_daily_averages(df, pollutant='CO(GT)', title=None):
    """
    Create a line plot showing daily averages of a pollutant.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        pollutant (str): Name of the pollutant column
        title (str): Chart title
        
    Returns:
        matplotlib.figure.Figure: The plot figure
    """
    if df is None or pollutant not in df.columns:
        return None
    
    # Calculate daily averages
    daily_avg = df.groupby('Date')[pollutant].mean().reset_index()
    
    if daily_avg.empty:
        return None
    
    if title is None:
        title = f"Daily Average {pollutant} Concentration"
    
    # Interactive daily averages with Plotly
    fig = px.line(daily_avg, x='Date', y=pollutant, title=title or f'Daily Average {pollutant}',
          labels={'Date': 'Date', pollutant: f'Average {pollutant}'})
    fig.update_traces(mode='lines+markers')
    fig.update_layout(template='plotly_white', hovermode='x unified')
    return fig


def plot_multiple_pollutants(df, pollutants=None, title="Multiple Pollutants Over Time"):
    """
    Create a multi-line plot showing multiple pollutants over time.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        pollutants (list): List of pollutant column names
        title (str): Chart title
        
    Returns:
        matplotlib.figure.Figure: The plot figure
    """
    if df is None:
        return None
    
    if pollutants is None:
        pollutants = ['CO(GT)', 'NOx(GT)', 'NO2(GT)']
    
    # Filter pollutants that exist in the dataset
    available_pollutants = [p for p in pollutants if p in df.columns]
    
    if not available_pollutants:
        return None
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = ['#2E8B57', '#FF6B6B', '#4A90E2', '#FFD93D', '#6A5ACD']
    
    for i, pollutant in enumerate(available_pollutants):
        plot_data = df[['DateTime', pollutant]].dropna()
        # Additional filter to remove NaT values from DateTime
        plot_data = plot_data[plot_data['DateTime'].notna()]
        if not plot_data.empty:
            ax.plot(plot_data['DateTime'], plot_data[pollutant], 
                   label=pollutant, linewidth=1.5, alpha=0.8,
                   color=colors[i % len(colors)])
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Concentration', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig


def plot_nox_vs_sensor(df, title="NOx(GT) vs Sensor Reading"):
    """
    Create a scatter plot showing relationship between NOx(GT) and PT08.S3(NOx) sensor reading.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        title (str): Chart title
        
    Returns:
        matplotlib.figure.Figure: The plot figure
    """
    if df is None or 'NOx(GT)' not in df.columns or 'PT08.S3(NOx)' not in df.columns:
        return None
    
    # Filter out missing values
    plot_data = df[['NOx(GT)', 'PT08.S3(NOx)']].dropna()
    
    if plot_data.empty:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    scatter = ax.scatter(plot_data['NOx(GT)'], plot_data['PT08.S3(NOx)'], 
                        alpha=0.6, c=plot_data['NOx(GT)'], 
                        cmap='Reds', s=20)
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('NOx(GT) Concentration (µg/m³)', fontsize=12)
    ax.set_ylabel('PT08.S3(NOx) Sensor Reading', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('NOx(GT) Concentration (µg/m³)', fontsize=10)
    
    plt.tight_layout()
    
    return fig


def create_summary_metrics_display(metrics):
    """
    Create a formatted display of key metrics for Streamlit.
    
    Args:
        metrics (dict): Air quality metrics from analysis.py
        
    Returns:
        dict: Formatted metrics for display
    """
    if not metrics:
        return {}
    
    display_metrics = {}
    
    # Format CO metrics
    if 'co' in metrics:
        co_metrics = metrics['co']
        display_metrics['CO Concentration'] = {
            'Average': f"{co_metrics['mean']:.2f} mg/m³",
            'Maximum': f"{co_metrics['max']:.2f} mg/m³",
            'Minimum': f"{co_metrics['min']:.2f} mg/m³"
        }
    
    # Format Temperature metrics
    if 'temperature' in metrics:
        temp_metrics = metrics['temperature']
        display_metrics['Temperature'] = {
            'Average': f"{temp_metrics['mean']:.1f} °C",
            'Maximum': f"{temp_metrics['max']:.1f} °C",
            'Minimum': f"{temp_metrics['min']:.1f} °C"
        }
    
    # Format Humidity metrics
    if 'humidity' in metrics:
        rh_metrics = metrics['humidity']
        display_metrics['Relative Humidity'] = {
            'Average': f"{rh_metrics['mean']:.1f}%",
            'Maximum': f"{rh_metrics['max']:.1f}%",
            'Minimum': f"{rh_metrics['min']:.1f}%"
        }
    
    return display_metrics
