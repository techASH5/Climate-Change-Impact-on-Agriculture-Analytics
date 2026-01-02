"""
Data Generation Script for Climate Change Impact on Agriculture
Generates realistic synthetic datasets for demonstration purposes
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

# Set random seed for reproducibility
np.random.seed(42)

# Configuration
STATES = [
    'Punjab', 'Haryana', 'Uttar Pradesh', 'Bihar', 'West Bengal',
    'Madhya Pradesh', 'Maharashtra', 'Karnataka', 'Tamil Nadu', 'Andhra Pradesh',
    'Telangana', 'Gujarat', 'Rajasthan', 'Odisha', 'Chhattisgarh'
]

CROPS = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane']

YEARS = list(range(1990, 2024))
FUTURE_YEARS = list(range(2024, 2051))

# Base climate parameters (state-wise averages)
BASE_CLIMATE = {
    'Punjab': {'rainfall': 650, 'temp': 24.5},
    'Haryana': {'rainfall': 550, 'temp': 25.0},
    'Uttar Pradesh': {'rainfall': 1000, 'temp': 25.5},
    'Bihar': {'rainfall': 1200, 'temp': 26.0},
    'West Bengal': {'rainfall': 1600, 'temp': 26.5},
    'Madhya Pradesh': {'rainfall': 1150, 'temp': 26.0},
    'Maharashtra': {'rainfall': 1200, 'temp': 27.0},
    'Karnataka': {'rainfall': 1100, 'temp': 26.5},
    'Tamil Nadu': {'rainfall': 950, 'temp': 28.0},
    'Andhra Pradesh': {'rainfall': 900, 'temp': 28.5},
    'Telangana': {'rainfall': 950, 'temp': 27.5},
    'Gujarat': {'rainfall': 800, 'temp': 27.0},
    'Rajasthan': {'rainfall': 550, 'temp': 27.5},
    'Odisha': {'rainfall': 1450, 'temp': 27.0},
    'Chhattisgarh': {'rainfall': 1300, 'temp': 26.5}
}

# Base yield parameters (crop-wise, ton/ha)
BASE_YIELD = {
    'Rice': 3.5,
    'Wheat': 3.2,
    'Maize': 2.8,
    'Cotton': 2.0,
    'Sugarcane': 70.0
}

def generate_climate_data():
    """Generate historical climate data with trends"""
    print("Generating climate data...")
    
    data = []
    for state in STATES:
        base_rain = BASE_CLIMATE[state]['rainfall']
        base_temp = BASE_CLIMATE[state]['temp']
        
        for year in YEARS:
            # Add climate change trends
            year_offset = year - 1990
            
            # Temperature increasing trend: +0.03°C per year
            temp_trend = year_offset * 0.03
            # Rainfall variability: slight decrease in some regions
            rain_trend = year_offset * (-0.5 if state in ['Rajasthan', 'Gujarat'] else 0.2)
            
            # Add random variation
            rainfall = base_rain + rain_trend + np.random.normal(0, 100)
            temperature = base_temp + temp_trend + np.random.normal(0, 0.5)
            
            data.append({
                'Year': year,
                'State': state,
                'Rainfall_mm': max(0, rainfall),
                'Avg_Temp_C': temperature,
                'Max_Temp_C': temperature + np.random.uniform(5, 8),
                'Min_Temp_C': temperature - np.random.uniform(5, 8)
            })
    
    df = pd.DataFrame(data)
    df.to_csv('./data/raw/climate_data.csv', index=False)
    print(f"✓ Climate data saved: {len(df)} records")
    return df

def generate_crop_yield_data(climate_df):
    """Generate crop yield data correlated with climate"""
    print("Generating crop yield data...")
    
    data = []
    for state in STATES:
        state_climate = climate_df[climate_df['State'] == state]
        
        for crop in CROPS:
            base_yield = BASE_YIELD[crop]
            
            # Crop-specific climate sensitivity
            rain_sensitivity = {
                'Rice': 0.0015, 'Wheat': 0.001, 'Maize': 0.0012,
                'Cotton': 0.0008, 'Sugarcane': 0.02
            }[crop]
            
            temp_sensitivity = {
                'Rice': -0.15, 'Wheat': -0.20, 'Maize': -0.10,
                'Cotton': -0.08, 'Sugarcane': -0.5
            }[crop]
            
            for _, climate_row in state_climate.iterrows():
                year = climate_row['Year']
                rainfall = climate_row['Rainfall_mm']
                temp = climate_row['Avg_Temp_C']
                
                # Calculate yield based on climate
                rain_effect = (rainfall - BASE_CLIMATE[state]['rainfall']) * rain_sensitivity
                temp_effect = (temp - BASE_CLIMATE[state]['temp']) * temp_sensitivity
                
                # Technology improvement trend: +0.5% per year
                tech_trend = (year - 1990) * 0.015
                
                # Calculate final yield
                yield_value = base_yield * (1 + tech_trend + rain_effect + temp_effect)
                yield_value += np.random.normal(0, base_yield * 0.1)  # Random variation
                yield_value = max(0.1, yield_value)  # Ensure positive
                
                # Generate area and production
                area_ha = np.random.uniform(50000, 500000)
                production_ton = yield_value * area_ha
                
                data.append({
                    'Year': year,
                    'State': state,
                    'Crop': crop,
                    'Area_ha': area_ha,
                    'Production_ton': production_ton,
                    'Yield_ton_per_ha': yield_value
                })
    
    df = pd.DataFrame(data)
    df.to_csv('./data/raw/crop_yield.csv', index=False)
    print(f"✓ Crop yield data saved: {len(df)} records")
    return df

def generate_future_climate_data():
    """Generate future climate projections under different scenarios"""
    print("Generating future climate projections...")
    
    scenarios = {
        'SSP2-4.5': {'temp_increase': 0.04, 'rain_change': 0.3},  # Moderate
        'SSP5-8.5': {'temp_increase': 0.08, 'rain_change': 0.5}   # High emissions
    }
    
    all_data = []
    
    for scenario_name, params in scenarios.items():
        for state in STATES:
            base_rain = BASE_CLIMATE[state]['rainfall']
            base_temp = BASE_CLIMATE[state]['temp']
            
            # 2023 baseline (end of historical)
            baseline_temp = base_temp + (2023 - 1990) * 0.03
            baseline_rain = base_rain + (2023 - 1990) * (-0.5 if state in ['Rajasthan', 'Gujarat'] else 0.2)
            
            for year in FUTURE_YEARS:
                year_offset = year - 2024
                
                # Apply scenario-specific trends
                temp_trend = year_offset * params['temp_increase']
                rain_trend = year_offset * params['rain_change']
                
                # Add variation
                rainfall = baseline_rain + rain_trend + np.random.normal(0, 80)
                temperature = baseline_temp + temp_trend + np.random.normal(0, 0.4)
                
                all_data.append({
                    'Year': year,
                    'State': state,
                    'Scenario': scenario_name,
                    'Rainfall_mm': max(0, rainfall),
                    'Avg_Temp_C': temperature,
                    'Max_Temp_C': temperature + np.random.uniform(5, 8),
                    'Min_Temp_C': temperature - np.random.uniform(5, 8)
                })
    
    df = pd.DataFrame(all_data)
    df.to_csv('./data/raw/future_climate.csv', index=False)
    print(f"✓ Future climate data saved: {len(df)} records")
    return df

def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("Climate Change Impact on Agriculture - Data Generation")
    print("="*60 + "\n")
    
    # Create directories if they don't exist
    os.makedirs('./data/raw', exist_ok=True)
    os.makedirs('./data/processed', exist_ok=True)
    
    # Generate datasets
    climate_df = generate_climate_data()
    yield_df = generate_crop_yield_data(climate_df)
    future_climate_df = generate_future_climate_data()
    
    print("\n" + "="*60)
    print("Data generation complete!")
    print("="*60)
    print(f"\nGenerated files:")
    print(f"  • climate_data.csv ({len(climate_df):,} records)")
    print(f"  • crop_yield.csv ({len(yield_df):,} records)")
    print(f"  • future_climate.csv ({len(future_climate_df):,} records)")
    print("\nNext step: Run data_prep.py to clean and merge the data\n")

if __name__ == "__main__":
    main()
