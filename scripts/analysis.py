"""
Exploratory Data Analysis and Visualization
Analyzes climate-crop relationships and generates visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from scipy import stats
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

def load_data():
    """Load processed data"""
    print("Loading processed data...")
    merged_df = pd.read_csv('./data/processed/merged_data.csv')
    print(f"✓ Loaded {len(merged_df):,} records")
    return merged_df

def analyze_yield_trends(df):
    """Analyze and visualize yield trends over time"""
    print("\nAnalyzing yield trends...")
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Crop Yield Trends Over Time (1990-2023)', fontsize=16, fontweight='bold')
    
    crops = df['Crop'].unique()[:5]
    
    for idx, crop in enumerate(crops):
        ax = axes[idx // 3, idx % 3]
        crop_data = df[df['Crop'] == crop].groupby('Year')['Yield_ton_per_ha'].mean().reset_index()
        
        # Plot trend
        ax.plot(crop_data['Year'], crop_data['Yield_ton_per_ha'], 
                marker='o', linewidth=2, markersize=4, label=crop)
        
        # Add trend line
        z = np.polyfit(crop_data['Year'], crop_data['Yield_ton_per_ha'], 1)
        p = np.poly1d(z)
        ax.plot(crop_data['Year'], p(crop_data['Year']), 
                "--", alpha=0.7, linewidth=2, color='red', label='Trend')
        
        ax.set_title(f'{crop}', fontweight='bold')
        ax.set_xlabel('Year')
        ax.set_ylabel('Yield (ton/ha)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # Remove extra subplot
    if len(crops) < 6:
        fig.delaxes(axes[1, 2])
    
    plt.tight_layout()
    plt.savefig('./visuals/yield_trends.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: yield_trends.png")
    plt.close()

def analyze_climate_trends(df):
    """Analyze climate variable trends"""
    print("Analyzing climate trends...")
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Climate Trends in India (1990-2023)', fontsize=16, fontweight='bold')
    
    # Temperature trend
    temp_yearly = df.groupby('Year')['Avg_Temp_C'].mean().reset_index()
    axes[0].plot(temp_yearly['Year'], temp_yearly['Avg_Temp_C'], 
                 marker='o', linewidth=2, color='orangered', markersize=5)
    
    z = np.polyfit(temp_yearly['Year'], temp_yearly['Avg_Temp_C'], 1)
    p = np.poly1d(z)
    axes[0].plot(temp_yearly['Year'], p(temp_yearly['Year']), 
                 "--", linewidth=2, color='darkred', label=f'Trend: +{z[0]:.3f}°C/year')
    
    axes[0].set_title('Average Temperature Trend', fontweight='bold')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Temperature (°C)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Rainfall trend
    rain_yearly = df.groupby('Year')['Rainfall_mm'].mean().reset_index()
    axes[1].plot(rain_yearly['Year'], rain_yearly['Rainfall_mm'], 
                 marker='o', linewidth=2, color='steelblue', markersize=5)
    
    z = np.polyfit(rain_yearly['Year'], rain_yearly['Rainfall_mm'], 1)
    p = np.poly1d(z)
    axes[1].plot(rain_yearly['Year'], p(rain_yearly['Year']), 
                 "--", linewidth=2, color='navy', label=f'Trend: {z[0]:.2f} mm/year')
    
    axes[1].set_title('Average Rainfall Trend', fontweight='bold')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('Rainfall (mm)')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('./visuals/climate_trends.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: climate_trends.png")
    plt.close()

def analyze_correlations(df):
    """Analyze correlations between climate and yield"""
    print("Analyzing correlations...")
    
    # Calculate correlations by crop
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Climate-Yield Correlations by Crop', fontsize=16, fontweight='bold')
    
    crops = df['Crop'].unique()[:5]
    
    for idx, crop in enumerate(crops):
        ax = axes[idx // 3, idx % 3]
        crop_data = df[df['Crop'] == crop]
        
        # Select numeric columns for correlation
        corr_cols = ['Yield_ton_per_ha', 'Rainfall_mm', 'Avg_Temp_C', 
                     'Max_Temp_C', 'Min_Temp_C']
        corr_matrix = crop_data[corr_cols].corr()
        
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                    center=0, ax=ax, cbar_kws={'shrink': 0.8})
        ax.set_title(f'{crop}', fontweight='bold')
    
    # Remove extra subplot
    if len(crops) < 6:
        fig.delaxes(axes[1, 2])
    
    plt.tight_layout()
    plt.savefig('./visuals/correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: correlation_heatmap.png")
    plt.close()

def analyze_climate_impact(df):
    """Quantify climate impact using regression"""
    print("\nQuantifying climate impact...")
    
    results = []
    
    for crop in df['Crop'].unique():
        crop_data = df[df['Crop'] == crop].copy()
        
        # Prepare features
        X = crop_data[['Rainfall_mm', 'Avg_Temp_C']]
        y = crop_data['Yield_ton_per_ha']
        
        # Fit model
        model = LinearRegression()
        model.fit(X, y)
        
        # Calculate R²
        r2 = model.score(X, y)
        
        results.append({
            'Crop': crop,
            'Rainfall_Coefficient': model.coef_[0],
            'Temperature_Coefficient': model.coef_[1],
            'R_squared': r2
        })
    
    results_df = pd.DataFrame(results)
    results_df.to_csv('./data/processed/climate_impact_coefficients.csv', index=False)
    
    print("\nClimate Impact Coefficients:")
    print(results_df.to_string(index=False))
    print("\n✓ Saved: climate_impact_coefficients.csv")
    
    return results_df

def plot_state_comparison(df):
    """Compare yields across states"""
    print("Creating state comparison plots...")
    
    # Top 10 states by average yield for each major crop
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('State-wise Average Crop Yields', fontsize=16, fontweight='bold')
    
    major_crops = ['Rice', 'Wheat', 'Maize', 'Cotton']
    
    for idx, crop in enumerate(major_crops):
        ax = axes[idx // 2, idx % 2]
        crop_data = df[df['Crop'] == crop].groupby('State')['Yield_ton_per_ha'].mean().sort_values(ascending=False).head(10)
        
        colors = sns.color_palette('viridis', len(crop_data))
        crop_data.plot(kind='barh', ax=ax, color=colors)
        
        ax.set_title(f'{crop}', fontweight='bold', fontsize=12)
        ax.set_xlabel('Average Yield (ton/ha)')
        ax.set_ylabel('State')
        ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig('./visuals/state_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: state_comparison.png")
    plt.close()

def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("Exploratory Data Analysis")
    print("="*60 + "\n")
    
    # Create visuals directory
    os.makedirs('./visuals', exist_ok=True)
    
    # Load data
    df = load_data()
    
    # Run analyses
    analyze_yield_trends(df)
    analyze_climate_trends(df)
    analyze_correlations(df)
    impact_results = analyze_climate_impact(df)
    plot_state_comparison(df)
    
    print("\n" + "="*60)
    print("Analysis complete!")
    print("="*60)
    print(f"\nVisualizations saved in ./visuals/")
    print(f"Analysis results saved in ./data/processed/")
    print("\nNext step: Run vulnerability_analysis.py\n")

if __name__ == "__main__":
    main()
