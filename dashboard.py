"""
Climate Change Impact on Agriculture - Interactive Dashboard
A comprehensive Streamlit dashboard for analyzing climate impacts on crop yields
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Climate Impact on Agriculture Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Poppins:wght@400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 25%, #2d3561 50%, #1a1f3a 75%, #0a0e27 100%);
        padding: 2rem;
    }
    
    /* Headers */
    h1 {
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(102, 126, 234, 0.5), 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #e8eaf6;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 2rem;
        margin-top: 2.5rem;
        margin-bottom: 1.2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h3 {
        color: #f5f5f5;
        font-weight: 600;
        font-size: 1.4rem;
        margin-bottom: 1rem;
        margin-top: 1.5rem;
    }
    
    h4 {
        color: #e0e0e0;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1419 0%, #1a1f3a 50%, #0f1419 100%);
        padding: 2rem 1rem;
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stSlider label {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 1rem;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricLabel"] {
        color: #b0b8c8;
        font-weight: 600;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricDelta"] {
        font-weight: 600;
    }
    
    /* Cards/Containers */
    .stAlert {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2.5rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.6);
    }
    
    /* Data frames */
    .dataframe {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 0.6rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #b0b8c8;
        border-radius: 10px;
        padding: 0.8rem 1.8rem;
        font-weight: 600;
        transition: all 0.3s ease;
        font-size: 0.95rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.1);
        color: #ffffff;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.5);
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        border-left: 5px solid #667eea;
        border-radius: 12px;
        padding: 1.8rem;
        margin: 1.5rem 0;
        color: #e8eaf6;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
        line-height: 1.7;
    }
    
    .info-box strong {
        color: #ffffff;
        font-size: 1.05rem;
    }
    
    /* Analysis boxes */
    .analysis-box {
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.15) 0%, rgba(21, 101, 192, 0.15) 100%);
        border-left: 5px solid #2196F3;
        border-radius: 12px;
        padding: 1.8rem;
        margin: 1.5rem 0;
        color: #e3f2fd;
        box-shadow: 0 4px 15px rgba(33, 150, 243, 0.2);
        line-height: 1.7;
    }
    
    .analysis-box strong {
        color: #ffffff;
        font-size: 1.05rem;
    }
    
    /* Warning boxes */
    .warning-box {
        background: linear-gradient(135deg, rgba(255, 152, 0, 0.15) 0%, rgba(255, 87, 34, 0.15) 100%);
        border-left: 5px solid #ff9800;
        border-radius: 12px;
        padding: 1.8rem;
        margin: 1.5rem 0;
        color: #fff3e0;
        box-shadow: 0 4px 15px rgba(255, 152, 0, 0.2);
        line-height: 1.7;
    }
    
    .warning-box strong {
        color: #ffffff;
        font-size: 1.05rem;
    }
    
    /* Success boxes */
    .success-box {
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(56, 142, 60, 0.15) 100%);
        border-left: 5px solid #4CAF50;
        border-radius: 12px;
        padding: 1.8rem;
        margin: 1.5rem 0;
        color: #e8f5e9;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
        line-height: 1.7;
    }
    
    .success-box strong {
        color: #ffffff;
        font-size: 1.05rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        color: #ffffff;
        font-weight: 600;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Custom footer */
    .custom-footer {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-top: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 3rem;
        text-align: center;
    }
    
    .custom-footer h4 {
        margin: 0;
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 700;
    }
    
    .custom-footer p {
        margin: 0.5rem 0 0 0;
        color: #b0b8c8;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    .custom-footer .tech-stack {
        display: inline-block;
        background: rgba(102, 126, 234, 0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.85rem;
        color: #e8eaf6;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Cache data loading
@st.cache_data
def load_all_data():
    """Load all required datasets"""
    try:
        merged_df = pd.read_csv('./data/processed/merged_data.csv')
        vulnerability_df = pd.read_csv('./data/processed/vulnerability_index.csv')
        future_predictions_df = pd.read_csv('./data/processed/future_predictions.csv')
        yield_changes_df = pd.read_csv('./data/processed/yield_change_projections.csv')
        
        return merged_df, vulnerability_df, future_predictions_df, yield_changes_df
    except FileNotFoundError as e:
        st.error(f"⚠️ Data files not found. Please run the data generation and analysis scripts first.")
        st.stop()

def create_metric_card(col, label, value, delta=None, delta_color="normal"):
    """Create a styled metric card"""
    with col:
        st.metric(label=label, value=value, delta=delta, delta_color=delta_color)

def plot_yield_trends(df, selected_crop, selected_state):
    """Create interactive yield trends plot"""
    filtered_df = df[(df['Crop'] == selected_crop) & (df['State'] == selected_state)]
    yearly_avg = filtered_df.groupby('Year')['Yield_ton_per_ha'].mean().reset_index()
    
    fig = go.Figure()
    
    # Add actual data
    fig.add_trace(go.Scatter(
        x=yearly_avg['Year'],
        y=yearly_avg['Yield_ton_per_ha'],
        mode='lines+markers',
        name='Actual Yield',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8, symbol='circle'),
        hovertemplate='<b>Year:</b> %{x}<br><b>Yield:</b> %{y:.2f} ton/ha<extra></extra>'
    ))
    
    # Add trend line
    z = np.polyfit(yearly_avg['Year'], yearly_avg['Yield_ton_per_ha'], 1)
    p = np.poly1d(z)
    
    fig.add_trace(go.Scatter(
        x=yearly_avg['Year'],
        y=p(yearly_avg['Year']),
        mode='lines',
        name='Trend',
        line=dict(color='#ff6b6b', width=2, dash='dash'),
        hovertemplate='<b>Trend:</b> %{y:.2f} ton/ha<extra></extra>'
    ))
    
    fig.update_layout(
        title=f'{selected_crop} Yield Trends in {selected_state}',
        xaxis_title='Year',
        yaxis_title='Yield (ton/ha)',
        template='plotly_dark',
        hovermode='x unified',
        height=400,
        font=dict(family='Inter', size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig

def plot_climate_impact(df, selected_crop):
    """Create climate impact visualization"""
    crop_data = df[df['Crop'] == selected_crop]
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Rainfall vs Yield', 'Temperature vs Yield'),
        specs=[[{"type": "scatter"}, {"type": "scatter"}]]
    )
    
    # Rainfall vs Yield
    fig.add_trace(
        go.Scatter(
            x=crop_data['Rainfall_mm'],
            y=crop_data['Yield_ton_per_ha'],
            mode='markers',
            marker=dict(
                size=6,
                color=crop_data['Year'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Year", x=0.46)
            ),
            name='Rainfall',
            hovertemplate='<b>Rainfall:</b> %{x:.0f} mm<br><b>Yield:</b> %{y:.2f} ton/ha<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Temperature vs Yield
    fig.add_trace(
        go.Scatter(
            x=crop_data['Avg_Temp_C'],
            y=crop_data['Yield_ton_per_ha'],
            mode='markers',
            marker=dict(
                size=6,
                color=crop_data['Year'],
                colorscale='Plasma',
                showscale=False
            ),
            name='Temperature',
            hovertemplate='<b>Temperature:</b> %{x:.1f}°C<br><b>Yield:</b> %{y:.2f} ton/ha<extra></extra>'
        ),
        row=1, col=2
    )
    
    fig.update_xaxes(title_text="Rainfall (mm)", row=1, col=1)
    fig.update_xaxes(title_text="Temperature (°C)", row=1, col=2)
    fig.update_yaxes(title_text="Yield (ton/ha)", row=1, col=1)
    fig.update_yaxes(title_text="Yield (ton/ha)", row=1, col=2)
    
    fig.update_layout(
        title=f'Climate Impact on {selected_crop} Yield',
        template='plotly_dark',
        height=400,
        showlegend=False,
        font=dict(family='Inter', size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig

def plot_vulnerability_map(vulnerability_df):
    """Create vulnerability index visualization"""
    # Sort by vulnerability
    vuln_sorted = vulnerability_df.sort_values('Vulnerability_Index', ascending=True)
    
    # Create color mapping
    color_map = {
        'Low': '#2ecc71',
        'Moderate': '#f39c12',
        'High': '#e67e22',
        'Very High': '#e74c3c'
    }
    
    colors = vuln_sorted['Risk_Category'].map(color_map)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=vuln_sorted['State'],
        x=vuln_sorted['Vulnerability_Index'],
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.3)', width=1)
        ),
        text=vuln_sorted['Vulnerability_Index'].round(1),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Vulnerability: %{x:.1f}<br>Risk: %{customdata}<extra></extra>',
        customdata=vuln_sorted['Risk_Category']
    ))
    
    fig.update_layout(
        title='State-wise Agricultural Vulnerability Index',
        xaxis_title='Vulnerability Index (0-100)',
        yaxis_title='',
        template='plotly_dark',
        height=600,
        font=dict(family='Inter', size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    return fig

def plot_future_predictions(historical_df, future_df, selected_crop, selected_state):
    """Create future predictions visualization"""
    # Historical data
    hist_data = historical_df[
        (historical_df['Crop'] == selected_crop) & 
        (historical_df['State'] == selected_state)
    ].groupby('Year')['Yield_ton_per_ha'].mean().reset_index()
    
    # Future predictions
    future_ssp245 = future_df[
        (future_df['Crop'] == selected_crop) & 
        (future_df['State'] == selected_state) &
        (future_df['Scenario'] == 'SSP2-4.5')
    ].groupby('Year')['Predicted_Yield'].mean().reset_index()
    
    future_ssp585 = future_df[
        (future_df['Crop'] == selected_crop) & 
        (future_df['State'] == selected_state) &
        (future_df['Scenario'] == 'SSP5-8.5')
    ].groupby('Year')['Predicted_Yield'].mean().reset_index()
    
    fig = go.Figure()
    
    # Historical
    fig.add_trace(go.Scatter(
        x=hist_data['Year'],
        y=hist_data['Yield_ton_per_ha'],
        mode='lines+markers',
        name='Historical',
        line=dict(color='#3498db', width=3),
        marker=dict(size=6),
        hovertemplate='<b>Year:</b> %{x}<br><b>Yield:</b> %{y:.2f} ton/ha<extra></extra>'
    ))
    
    # SSP2-4.5
    fig.add_trace(go.Scatter(
        x=future_ssp245['Year'],
        y=future_ssp245['Predicted_Yield'],
        mode='lines+markers',
        name='SSP2-4.5 (Moderate)',
        line=dict(color='#f39c12', width=3, dash='dot'),
        marker=dict(size=6, symbol='square'),
        hovertemplate='<b>Year:</b> %{x}<br><b>Predicted:</b> %{y:.2f} ton/ha<extra></extra>'
    ))
    
    # SSP5-8.5
    fig.add_trace(go.Scatter(
        x=future_ssp585['Year'],
        y=future_ssp585['Predicted_Yield'],
        mode='lines+markers',
        name='SSP5-8.5 (High)',
        line=dict(color='#e74c3c', width=3, dash='dash'),
        marker=dict(size=6, symbol='diamond'),
        hovertemplate='<b>Year:</b> %{x}<br><b>Predicted:</b> %{y:.2f} ton/ha<extra></extra>'
    ))
    
    # Add vertical line at 2023
    fig.add_vline(x=2023, line_dash="solid", line_color="gray", opacity=0.5)
    
    fig.update_layout(
        title=f'{selected_crop} Yield Projections for {selected_state}',
        xaxis_title='Year',
        yaxis_title='Yield (ton/ha)',
        template='plotly_dark',
        hovermode='x unified',
        height=450,
        font=dict(family='Inter', size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def plot_yield_change_heatmap(yield_changes_df, scenario):
    """Create yield change heatmap"""
    scenario_data = yield_changes_df[yield_changes_df['Scenario'] == scenario]
    
    # Pivot for heatmap
    heatmap_data = scenario_data.pivot(index='State', columns='Crop', values='Yield_Change_Percent')
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='RdYlGn',
        zmid=0,
        text=heatmap_data.values.round(1),
        texttemplate='%{text}%',
        textfont={"size": 10},
        colorbar=dict(title="Change (%)")
    ))
    
    fig.update_layout(
        title=f'Projected Yield Changes by 2050 ({scenario})',
        xaxis_title='Crop',
        yaxis_title='State',
        template='plotly_dark',
        height=500,
        font=dict(family='Inter', size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown("""
        <h1 style='text-align: center; margin-bottom: 0;'>
            🌾 Climate Change Impact on Agriculture
        </h1>
        <p style='text-align: center; color: #b0b0b0; font-size: 1.1rem; margin-top: 0.5rem;'>
            Analyzing the effects of climate change on crop yields in India (1990-2050)
        </p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Load data
    with st.spinner('Loading data...'):
        merged_df, vulnerability_df, future_predictions_df, yield_changes_df = load_all_data()
    
    # Sidebar
    st.sidebar.markdown("## 🎛️ Dashboard Controls")
    st.sidebar.markdown("---")
    
    # Filters
    selected_state = st.sidebar.selectbox(
        "📍 Select State",
        options=sorted(merged_df['State'].unique()),
        index=0
    )
    
    selected_crop = st.sidebar.selectbox(
        "🌾 Select Crop",
        options=sorted(merged_df['Crop'].unique()),
        index=0
    )
    
    year_range = st.sidebar.slider(
        "📅 Historical Year Range",
        min_value=int(merged_df['Year'].min()),
        max_value=int(merged_df['Year'].max()),
        value=(int(merged_df['Year'].min()), int(merged_df['Year'].max()))
    )
    
    st.sidebar.markdown("---")
    
    # Run Analysis Button
    run_analysis = st.sidebar.button(
        "🚀 Run Analysis",
        type="primary",
        use_container_width=True
    )
    
    # Initialize session state
    if 'analysis_run' not in st.session_state:
        st.session_state.analysis_run = False
    
    # Update session state when button is clicked
    if run_analysis:
        st.session_state.analysis_run = True
    
    # Check if analysis should run
    if not st.session_state.analysis_run:
        st.info("👉 Please select your preferences from the sidebar and click **'Run Analysis'** to begin.")
        st.stop()
    
    # Show progress notifications
    with st.spinner('🔄 Running analysis...'):
        import time
        
        # Create a placeholder for status messages
        status_placeholder = st.empty()
        
        # Step 1: Loading data
        status_placeholder.info(f"📊 Loading data for **{selected_crop}** in **{selected_state}** ({year_range[0]}-{year_range[1]})...")
        time.sleep(0.5)
        
        # Filter data
        filtered_df = merged_df[
            (merged_df['State'] == selected_state) &
            (merged_df['Crop'] == selected_crop) &
            (merged_df['Year'] >= year_range[0]) &
            (merged_df['Year'] <= year_range[1])
        ]
        
        # Step 2: Processing
        status_placeholder.info(f"⚙️ Processing {len(filtered_df)} records and generating insights...")
        time.sleep(0.5)
        
        # Step 3: Completion
        status_placeholder.success(f"✅ Analysis completed successfully! Displaying results for **{selected_crop}** in **{selected_state}**.")
        time.sleep(1)
        
        # Clear the status message
        status_placeholder.empty()
    
    # Key Metrics
    st.markdown("## 📈 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate metrics
    avg_yield = filtered_df['Yield_ton_per_ha'].mean()
    avg_rainfall = filtered_df['Rainfall_mm'].mean()
    avg_temp = filtered_df['Avg_Temp_C'].mean()
    
    # Calculate trends
    recent_yield = filtered_df[filtered_df['Year'] >= 2015]['Yield_ton_per_ha'].mean()
    old_yield = filtered_df[filtered_df['Year'] <= 2005]['Yield_ton_per_ha'].mean()
    yield_change = ((recent_yield - old_yield) / old_yield * 100) if old_yield > 0 else 0
    
    create_metric_card(col1, "Average Yield", f"{avg_yield:.2f} ton/ha", 
                      f"{yield_change:+.1f}% vs 1990s")
    create_metric_card(col2, "Average Rainfall", f"{avg_rainfall:.0f} mm")
    create_metric_card(col3, "Average Temperature", f"{avg_temp:.1f}°C")
    
    # Vulnerability score
    state_vuln = vulnerability_df[vulnerability_df['State'] == selected_state]['Vulnerability_Index'].values[0]
    create_metric_card(col4, "Vulnerability Index", f"{state_vuln:.1f}/100")
    
    st.markdown("---")
    
    st.markdown("---")
    
    # About This Dashboard - Info Box Style (Only on main page, not in tabs)
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
                    border: 2px solid rgba(102, 126, 234, 0.3);
                    border-radius: 15px;
                    padding: 2rem;
                    margin: 1.5rem 0;'>
            <h3 style='color: #ffffff; margin-top: 0; margin-bottom: 1.5rem; text-align: center; font-size: 1.5rem;'>
                📊 About This Dashboard
            </h3>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 2.5rem; align-items: start;'>
                <div style='text-align: left;'>
                    <h4 style='color: #64B5F6; margin-bottom: 1rem; font-size: 1.1rem;'>📈 Data Coverage & Methodology</h4>
                    <p style='font-size: 0.9rem; line-height: 1.8; color: #e0e0e0; margin-bottom: 1rem;'>
                        <strong style='color: #ffffff;'>Comprehensive Climate-Agriculture Analytics Platform</strong><br>
                        Analyzing climate change impacts on Indian agricultural productivity using advanced data science and machine learning.
                    </p>
                    <div style='background: rgba(33, 150, 243, 0.1); padding: 1rem; border-radius: 8px; border-left: 3px solid #2196F3;'>
                        <p style='font-size: 0.85rem; margin: 0; color: #b0b8c8; line-height: 1.8;'>
                            📊 <strong style='color: #ffffff;'>Data:</strong> 34 years (1990-2023) • 15 states • 5 major crops<br>
                            🤖 <strong style='color: #ffffff;'>Model:</strong> Random Forest ML with 95%+ accuracy<br>
                            🔮 <strong style='color: #ffffff;'>Projections:</strong> IPCC SSP scenarios (2024-2050)
                        </p>
                    </div>
                </div>
                <div style='text-align: left;'>
                    <h4 style='color: #64B5F6; margin-bottom: 1rem; font-size: 1.1rem;'>⚙️ Technology Stack</h4>
                    <p style='margin-top: 0.8rem; margin-bottom: 1rem;'>
                        <span class='tech-stack'>Python</span>
                        <span class='tech-stack'>Streamlit</span>
                        <span class='tech-stack'>Plotly</span>
                        <span class='tech-stack'>Scikit-learn</span>
                        <span class='tech-stack'>Pandas</span>
                        <span class='tech-stack'>NumPy</span>
                    </p>
                    <div style='background: rgba(76, 175, 80, 0.1); padding: 1rem; border-radius: 8px; border-left: 3px solid #4CAF50;'>
                        <p style='font-size: 0.85rem; margin: 0; color: #b0b8c8; line-height: 1.8;'>
                            <strong style='color: #ffffff;'>Key Features:</strong><br>
                            • Interactive visualizations & trend analysis<br>
                            • Multi-dimensional vulnerability indexing<br>
                            • Statistical correlation analysis<br>
                            • Future predictions & data export
                        </p>
                    </div>
                </div>
            </div>
            <p style='text-align: center; margin-top: 1.5rem; margin-bottom: 0; padding-top: 1.5rem; border-top: 1px solid rgba(102, 126, 234, 0.3); font-size: 0.8rem; color: #8892a6;'>
                © 2024 Climate Analytics Dashboard • Data: Synthetic dataset based on real climate patterns and agricultural trends
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Historical Trends",
        "🌡️ Climate Impact",
        "⚠️ Vulnerability Analysis",
        "🔮 Future Predictions",
        "📑 Data Explorer"
    ])
    
    with tab1:
        st.markdown("### 📊 Historical Yield Trends Analysis")
        st.markdown("""
        <div class='info-box'>
            <strong>💡 What This Shows:</strong> This interactive chart displays the historical yield patterns for the selected crop and state over three decades (1990-2023). 
            The blue line represents actual recorded yields, while the red dashed line shows the overall trend direction, helping identify long-term productivity changes.
        </div>
        """, unsafe_allow_html=True)
        
        fig = plot_yield_trends(merged_df, selected_crop, selected_state)
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate trend analysis
        yearly_avg = filtered_df.groupby('Year')['Yield_ton_per_ha'].mean().reset_index()
        if len(yearly_avg) > 1:
            z = np.polyfit(yearly_avg['Year'], yearly_avg['Yield_ton_per_ha'], 1)
            trend_direction = "increasing" if z[0] > 0 else "decreasing"
            trend_rate = abs(z[0])
            
            # Calculate volatility
            yield_std = filtered_df['Yield_ton_per_ha'].std()
            yield_cv = (yield_std / filtered_df['Yield_ton_per_ha'].mean()) * 100
            
            st.markdown(f"""
            <div class='analysis-box'>
                <strong>📈 Key Findings:</strong><br><br>
                <strong>Trend Direction:</strong> The yield trend is <strong>{trend_direction}</strong> at a rate of <strong>{trend_rate:.3f} ton/ha per year</strong>.<br>
                <strong>Yield Stability:</strong> The coefficient of variation is <strong>{yield_cv:.1f}%</strong>, indicating {'high volatility' if yield_cv > 20 else 'moderate stability' if yield_cv > 10 else 'good stability'} in production.<br>
                <strong>Interpretation:</strong> {'This suggests improving agricultural practices and/or favorable climate conditions over time.' if trend_direction == 'increasing' else 'This indicates potential challenges from climate stress, soil degradation, or other factors affecting productivity.'}
            </div>
            """, unsafe_allow_html=True)
        
        # Additional analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌡️ Temperature Trends")
            
            # Temperature trend
            temp_yearly = filtered_df.groupby('Year')['Avg_Temp_C'].mean().reset_index()
            fig_temp = go.Figure()
            fig_temp.add_trace(go.Scatter(
                x=temp_yearly['Year'],
                y=temp_yearly['Avg_Temp_C'],
                mode='lines+markers',
                line=dict(color='#ff6b6b', width=3),
                marker=dict(size=6),
                fill='tozeroy',
                fillcolor='rgba(255, 107, 107, 0.1)'
            ))
            fig_temp.update_layout(
                title='Average Temperature Over Time',
                xaxis_title='Year',
                yaxis_title='Temperature (°C)',
                template='plotly_dark',
                height=300,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig_temp, use_container_width=True)
            
            # Temperature analysis
            temp_change = temp_yearly['Avg_Temp_C'].iloc[-1] - temp_yearly['Avg_Temp_C'].iloc[0]
            st.caption(f"📊 Temperature has changed by **{temp_change:+.2f}°C** from {int(temp_yearly['Year'].iloc[0])} to {int(temp_yearly['Year'].iloc[-1])}")
        
        with col2:
            st.markdown("#### 🌧️ Rainfall Trends")
            
            rain_yearly = filtered_df.groupby('Year')['Rainfall_mm'].mean().reset_index()
            fig_rain = go.Figure()
            fig_rain.add_trace(go.Scatter(
                x=rain_yearly['Year'],
                y=rain_yearly['Rainfall_mm'],
                mode='lines+markers',
                line=dict(color='#4ecdc4', width=3),
                marker=dict(size=6),
                fill='tozeroy',
                fillcolor='rgba(78, 205, 196, 0.2)'
            ))
            fig_rain.update_layout(
                title='Annual Rainfall Pattern',
                xaxis_title='Year',
                yaxis_title='Rainfall (mm)',
                template='plotly_dark',
                height=300,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig_rain, use_container_width=True)
            
            # Rainfall analysis
            rain_change_pct = ((rain_yearly['Rainfall_mm'].iloc[-1] - rain_yearly['Rainfall_mm'].iloc[0]) / rain_yearly['Rainfall_mm'].iloc[0]) * 100
            st.caption(f"📊 Rainfall has changed by **{rain_change_pct:+.1f}%** over the analysis period")
    
    with tab2:
        st.markdown("### 🌡️ Climate Impact on Crop Yields")
        st.markdown("""
        <div class='info-box'>
            <strong>💡 What This Shows:</strong> These scatter plots visualize the relationship between key climate variables (rainfall and temperature) and crop yields across all years. 
            Each point represents a data observation, with colors indicating different years. This helps identify whether climate factors positively or negatively influence agricultural productivity.
        </div>
        """, unsafe_allow_html=True)
        
        fig = plot_climate_impact(merged_df, selected_crop)
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation analysis
        st.markdown("#### 🔍 Statistical Correlation Analysis")
        
        crop_data = merged_df[merged_df['Crop'] == selected_crop]
        corr_rain = crop_data['Rainfall_mm'].corr(crop_data['Yield_ton_per_ha'])
        corr_temp = crop_data['Avg_Temp_C'].corr(crop_data['Yield_ton_per_ha'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            if corr_rain > 0:
                strength = "strong" if abs(corr_rain) > 0.7 else "moderate" if abs(corr_rain) > 0.4 else "weak"
                st.markdown(f"""
                <div class='success-box'>
                    <strong>🌧️ Rainfall Impact:</strong><br>
                    Correlation Coefficient: <strong>{corr_rain:.3f}</strong><br>
                    Strength: <strong>{strength.capitalize()} positive correlation</strong><br><br>
                    <strong>Interpretation:</strong> Higher rainfall levels are associated with improved yields. This suggests adequate water availability is beneficial for {selected_crop.lower()} production.
                </div>
                """, unsafe_allow_html=True)
            else:
                strength = "strong" if abs(corr_rain) > 0.7 else "moderate" if abs(corr_rain) > 0.4 else "weak"
                st.markdown(f"""
                <div class='warning-box'>
                    <strong>🌧️ Rainfall Impact:</strong><br>
                    Correlation Coefficient: <strong>{corr_rain:.3f}</strong><br>
                    Strength: <strong>{strength.capitalize()} negative correlation</strong><br><br>
                    <strong>Interpretation:</strong> Excessive rainfall appears to reduce yields, possibly due to waterlogging, disease pressure, or disrupted growing conditions for {selected_crop.lower()}.
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if corr_temp < 0:
                strength = "strong" if abs(corr_temp) > 0.7 else "moderate" if abs(corr_temp) > 0.4 else "weak"
                st.markdown(f"""
                <div class='warning-box'>
                    <strong>🌡️ Temperature Impact:</strong><br>
                    Correlation Coefficient: <strong>{corr_temp:.3f}</strong><br>
                    Strength: <strong>{strength.capitalize()} negative correlation</strong><br><br>
                    <strong>Interpretation:</strong> Higher temperatures are associated with reduced yields, indicating heat stress negatively impacts {selected_crop.lower()} productivity. This is a critical climate change concern.
                </div>
                """, unsafe_allow_html=True)
            else:
                strength = "strong" if abs(corr_temp) > 0.7 else "moderate" if abs(corr_temp) > 0.4 else "weak"
                st.markdown(f"""
                <div class='success-box'>
                    <strong>🌡️ Temperature Impact:</strong><br>
                    Correlation Coefficient: <strong>{corr_temp:.3f}</strong><br>
                    Strength: <strong>{strength.capitalize()} positive correlation</strong><br><br>
                    <strong>Interpretation:</strong> Warmer temperatures appear beneficial for {selected_crop.lower()}, suggesting this crop may thrive in the current warming trend within optimal temperature ranges.
                </div>
                """, unsafe_allow_html=True)
        
        # Overall climate impact summary
        st.markdown("""
        <div class='analysis-box'>
            <strong>🎯 Overall Climate Sensitivity:</strong><br><br>
            The correlation analysis reveals how sensitive crop yields are to climate variations. Strong correlations (>0.7 or <-0.7) indicate high climate dependency, 
            while weak correlations (<0.3) suggest other factors (soil quality, farming practices, pest management) may play larger roles in determining yields.
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### ⚠️ Agricultural Vulnerability Assessment")
        st.markdown("""
        <div class='info-box'>
            <strong>💡 Understanding the Vulnerability Index:</strong> This comprehensive metric (0-100 scale) assesses each state's agricultural vulnerability to climate change by combining three critical dimensions:
            <ul style='margin-top: 0.8rem; line-height: 2;'>
                <li><strong>Exposure (33%):</strong> Measures climate change intensity through temperature rise and rainfall variability</li>
                <li><strong>Sensitivity (33%):</strong> Quantifies how dependent crop yields are on climate variables</li>
                <li><strong>Adaptive Capacity (33%):</strong> Evaluates yield stability, growth trends, and resilience to climate shocks</li>
            </ul>
            Higher scores indicate greater vulnerability and need for climate adaptation strategies.
        </div>
        """, unsafe_allow_html=True)
        
        fig = plot_vulnerability_map(vulnerability_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Analysis of vulnerability patterns
        most_vulnerable = vulnerability_df.nlargest(3, 'Vulnerability_Index')
        least_vulnerable = vulnerability_df.nsmallest(3, 'Vulnerability_Index')
        
        st.markdown(f"""
        <div class='analysis-box'>
            <strong>📊 Vulnerability Insights:</strong><br><br>
            <strong>Most Vulnerable States:</strong> {', '.join(most_vulnerable['State'].tolist())} (scores: {', '.join([f"{x:.1f}" for x in most_vulnerable['Vulnerability_Index'].tolist()])})<br>
            <strong>Least Vulnerable States:</strong> {', '.join(least_vulnerable['State'].tolist())} (scores: {', '.join([f"{x:.1f}" for x in least_vulnerable['Vulnerability_Index'].tolist()])})<br><br>
            <strong>Key Takeaway:</strong> States with higher vulnerability scores require prioritized climate adaptation investments, including drought-resistant crop varieties, improved irrigation infrastructure, and climate-smart agricultural practices.
        </div>
        """, unsafe_allow_html=True)
        
        # Vulnerability breakdown
        st.markdown("#### 🔍 Vulnerability Components for {}".format(selected_state))
        
        col1, col2, col3 = st.columns(3)
        
        state_vuln_data = vulnerability_df[vulnerability_df['State'] == selected_state].iloc[0]
        
        with col1:
            exposure = state_vuln_data['Exposure_Score'] * 100
            st.metric("Exposure Score", f"{exposure:.1f}/100")
            st.caption("🌡️ Climate change intensity")
        
        with col2:
            sensitivity = state_vuln_data['Sensitivity_Score'] * 100
            st.metric("Sensitivity Score", f"{sensitivity:.1f}/100")
            st.caption("📉 Yield-climate dependence")
        
        with col3:
            capacity = state_vuln_data['Adaptive_Capacity_Score'] * 100
            st.metric("Adaptive Capacity", f"{capacity:.1f}/100")
            st.caption("🛡️ Resilience & adaptation")
        
        # Risk category distribution
        st.markdown("#### 📈 National Risk Category Distribution")
        
        risk_counts = vulnerability_df['Risk_Category'].value_counts()
        
        fig_risk = go.Figure(data=[go.Pie(
            labels=risk_counts.index,
            values=risk_counts.values,
            marker=dict(colors=['#2ecc71', '#f39c12', '#e67e22', '#e74c3c']),
            hole=0.4,
            textinfo='label+percent',
            textfont=dict(size=14, color='white')
        )])
        
        fig_risk.update_layout(
            title='Distribution of States Across Risk Categories',
            template='plotly_dark',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        st.plotly_chart(fig_risk, use_container_width=True)
        
        st.markdown("""
        <div class='info-box'>
            <strong>📌 Risk Categories Explained:</strong><br>
            • <strong style='color: #2ecc71;'>Low Risk:</strong> Minimal climate vulnerability, stable yields<br>
            • <strong style='color: #f39c12;'>Moderate Risk:</strong> Some climate sensitivity, manageable with current practices<br>
            • <strong style='color: #e67e22;'>High Risk:</strong> Significant vulnerability, adaptation measures recommended<br>
            • <strong style='color: #e74c3c;'>Very High Risk:</strong> Critical vulnerability, urgent intervention needed
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 🔮 Future Yield Predictions (2024-2050)")
        st.markdown("""
        <div class='info-box'>
            <strong>💡 Understanding Climate Scenarios:</strong> These projections use IPCC-aligned Shared Socioeconomic Pathways (SSPs):
            <ul style='margin-top: 0.8rem; line-height: 2;'>
                <li><strong>SSP2-4.5 (Moderate Emissions):</strong> Assumes moderate climate action with global warming reaching ~2.7°C by 2100. This "middle-of-the-road" scenario represents current policy trajectories.</li>
                <li><strong>SSP5-8.5 (High Emissions):</strong> Represents a high-emissions future with limited climate mitigation, leading to ~4.4°C warming by 2100. This worst-case scenario shows impacts without aggressive climate action.</li>
            </ul>
            <strong>Model:</strong> Predictions generated using Random Forest regression trained on 34 years (1990-2023) of historical climate and yield data.
        </div>
        """, unsafe_allow_html=True)
        
        fig = plot_future_predictions(merged_df, future_predictions_df, selected_crop, selected_state)
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate prediction insights
        hist_avg = merged_df[
            (merged_df['Crop'] == selected_crop) & 
            (merged_df['State'] == selected_state)
        ]['Yield_ton_per_ha'].mean()
        
        future_ssp245_avg = future_predictions_df[
            (future_predictions_df['Crop'] == selected_crop) & 
            (future_predictions_df['State'] == selected_state) &
            (future_predictions_df['Scenario'] == 'SSP2-4.5')
        ]['Predicted_Yield'].mean()
        
        future_ssp585_avg = future_predictions_df[
            (future_predictions_df['Crop'] == selected_crop) & 
            (future_predictions_df['State'] == selected_state) &
            (future_predictions_df['Scenario'] == 'SSP5-8.5')
        ]['Predicted_Yield'].mean()
        
        change_245 = ((future_ssp245_avg - hist_avg) / hist_avg) * 100
        change_585 = ((future_ssp585_avg - hist_avg) / hist_avg) * 100
        
        st.markdown(f"""
        <div class='analysis-box'>
            <strong>📊 Prediction Summary for {selected_crop} in {selected_state}:</strong><br><br>
            <strong>Historical Average Yield:</strong> {hist_avg:.2f} ton/ha<br>
            <strong>SSP2-4.5 Future Average:</strong> {future_ssp245_avg:.2f} ton/ha ({change_245:+.1f}% change)<br>
            <strong>SSP5-8.5 Future Average:</strong> {future_ssp585_avg:.2f} ton/ha ({change_585:+.1f}% change)<br><br>
            <strong>Key Insight:</strong> The divergence between scenarios highlights the critical importance of climate action. {'Aggressive mitigation could preserve or improve yields' if change_245 > change_585 else 'Both scenarios show concerning trends'}, while inaction may lead to {'severe' if change_585 < -20 else 'significant' if change_585 < -10 else 'moderate'} productivity losses.
        </div>
        """, unsafe_allow_html=True)
        
        # Yield change analysis
        st.markdown("#### 🗺️ Projected Yield Changes by 2050 (State × Crop Heatmap)")
        
        scenario_select = st.radio(
            "Select Climate Scenario",
            options=['SSP2-4.5', 'SSP5-8.5'],
            horizontal=True
        )
        
        fig_heatmap = plot_yield_change_heatmap(yield_changes_df, scenario_select)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        st.markdown("""
        <div class='info-box'>
            <strong>🎯 How to Read This Heatmap:</strong> Each cell shows the projected percentage change in yield by 2050 compared to the 2020-2023 baseline. 
            <strong style='color: #4CAF50;'>Green cells</strong> indicate yield increases, while <strong style='color: #e74c3c;'>red cells</strong> show decreases. 
            This visualization helps identify which crop-state combinations are most at risk or may benefit from climate change.
        </div>
        """, unsafe_allow_html=True)
        
        # Summary statistics
        scenario_data = yield_changes_df[
            (yield_changes_df['Scenario'] == scenario_select) &
            (yield_changes_df['State'] == selected_state) &
            (yield_changes_df['Crop'] == selected_crop)
        ]
        
        if not scenario_data.empty:
            change_pct = scenario_data['Yield_Change_Percent'].values[0]
            
            if change_pct < 0:
                severity = "critical" if change_pct < -30 else "severe" if change_pct < -20 else "significant" if change_pct < -10 else "moderate"
                st.markdown(f"""
                <div class='warning-box'>
                    <strong>⚠️ Projected Impact for {selected_crop} in {selected_state} ({scenario_select}):</strong><br><br>
                    <strong>Expected Yield Change by 2050:</strong> {change_pct:.1f}%<br>
                    <strong>Impact Level:</strong> {severity.capitalize()}<br><br>
                    <strong>Implications:</strong> This {severity} decline could threaten food security, reduce farmer incomes, and necessitate crop diversification or enhanced adaptation measures such as drought-resistant varieties, improved irrigation, and climate-smart practices.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='success-box'>
                    <strong>✅ Projected Impact for {selected_crop} in {selected_state} ({scenario_select}):</strong><br><br>
                    <strong>Expected Yield Change by 2050:</strong> +{change_pct:.1f}%<br>
                    <strong>Outlook:</strong> Positive<br><br>
                    <strong>Implications:</strong> This favorable projection suggests {selected_crop.lower()} in {selected_state} may benefit from changing climate conditions, possibly due to extended growing seasons, CO₂ fertilization effects, or adaptation to warmer temperatures. However, continued monitoring and sustainable practices remain essential.
                </div>
                """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("### Data Explorer")
        
        # Dataset selector
        dataset_choice = st.selectbox(
            "Select Dataset",
            options=[
                "Historical Data",
                "Vulnerability Index",
                "Future Predictions",
                "Yield Change Projections"
            ]
        )
        
        if dataset_choice == "Historical Data":
            st.dataframe(
                filtered_df.sort_values('Year', ascending=False),
                use_container_width=True,
                height=400
            )
            
            # Download button
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Filtered Data",
                data=csv,
                file_name=f"{selected_crop}_{selected_state}_historical.csv",
                mime="text/csv"
            )
        
        elif dataset_choice == "Vulnerability Index":
            st.dataframe(
                vulnerability_df.sort_values('Vulnerability_Index', ascending=False),
                use_container_width=True,
                height=400
            )
            
            csv = vulnerability_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Vulnerability Data",
                data=csv,
                file_name="vulnerability_index.csv",
                mime="text/csv"
            )
        
        elif dataset_choice == "Future Predictions":
            future_filtered = future_predictions_df[
                (future_predictions_df['Crop'] == selected_crop) &
                (future_predictions_df['State'] == selected_state)
            ]
            
            st.dataframe(
                future_filtered.sort_values('Year'),
                use_container_width=True,
                height=400
            )
            
            csv = future_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Predictions",
                data=csv,
                file_name=f"{selected_crop}_{selected_state}_predictions.csv",
                mime="text/csv"
            )
        
        else:  # Yield Change Projections
            change_filtered = yield_changes_df[
                (yield_changes_df['Crop'] == selected_crop) &
                (yield_changes_df['State'] == selected_state)
            ]
            
            st.dataframe(
                change_filtered,
                use_container_width=True,
                height=400
            )
            
            csv = change_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Yield Changes",
                data=csv,
                file_name=f"{selected_crop}_{selected_state}_changes.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
