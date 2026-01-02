"""
Data Preparation and Cleaning Script
Loads, cleans, and merges climate and crop yield data
"""

import pandas as pd
import numpy as np
import os

def load_and_clean_climate_data():
    """Load and clean climate data"""
    print("Loading climate data...")
    
    df = pd.read_csv('./data/raw/climate_data.csv')
    
    # Handle missing values
    df.fillna(df.mean(numeric_only=True), inplace=True)
    
    # Standardize state names
    df['State'] = df['State'].str.strip()
    
    # Ensure valid ranges
    df['Rainfall_mm'] = df['Rainfall_mm'].clip(lower=0)
    df['Avg_Temp_C'] = df['Avg_Temp_C'].clip(lower=-10, upper=50)
    
    print(f"✓ Climate data loaded: {len(df)} records")
    return df

def load_and_clean_yield_data():
    """Load and clean crop yield data"""
    print("Loading crop yield data...")
    
    df = pd.read_csv('./data/raw/crop_yield.csv')
    
    # Handle missing values
    df.fillna(df.mean(numeric_only=True), inplace=True)
    
    # Standardize columns
    df['State'] = df['State'].str.strip()
    df['Crop'] = df['Crop'].str.strip()
    
    # Remove invalid records
    df = df[df['Yield_ton_per_ha'] > 0]
    df = df[df['Area_ha'] > 0]
    
    print(f"✓ Crop yield data loaded: {len(df)} records")
    return df

def merge_datasets(climate_df, yield_df):
    """Merge climate and yield datasets"""
    print("Merging datasets...")
    
    # Merge on Year and State
    merged_df = pd.merge(
        yield_df,
        climate_df,
        on=['Year', 'State'],
        how='inner'
    )
    
    # Add derived features
    merged_df['Rainfall_Deviation'] = merged_df.groupby('State')['Rainfall_mm'].transform(
        lambda x: (x - x.mean()) / x.std()
    )
    
    merged_df['Temp_Deviation'] = merged_df.groupby('State')['Avg_Temp_C'].transform(
        lambda x: (x - x.mean()) / x.std()
    )
    
    # Add decade column for grouping
    merged_df['Decade'] = (merged_df['Year'] // 10) * 10
    
    print(f"✓ Merged dataset created: {len(merged_df)} records")
    return merged_df

def save_processed_data(df, filename):
    """Save processed data"""
    filepath = f'./data/processed/{filename}'
    df.to_csv(filepath, index=False)
    print(f"✓ Saved: {filepath}")

def generate_summary_statistics(merged_df):
    """Generate and save summary statistics"""
    print("\nGenerating summary statistics...")
    
    # Overall statistics
    summary = merged_df.groupby(['State', 'Crop']).agg({
        'Yield_ton_per_ha': ['mean', 'std', 'min', 'max'],
        'Rainfall_mm': 'mean',
        'Avg_Temp_C': 'mean'
    }).round(2)
    
    summary.to_csv('./data/processed/summary_statistics.csv')
    print("✓ Summary statistics saved")
    
    # Yearly trends
    yearly_trends = merged_df.groupby(['Year', 'Crop']).agg({
        'Yield_ton_per_ha': 'mean',
        'Rainfall_mm': 'mean',
        'Avg_Temp_C': 'mean'
    }).reset_index()
    
    yearly_trends.to_csv('./data/processed/yearly_trends.csv', index=False)
    print("✓ Yearly trends saved")

def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("Data Preparation and Cleaning")
    print("="*60 + "\n")
    
    # Create output directory
    os.makedirs('./data/processed', exist_ok=True)
    
    # Load and clean data
    climate_df = load_and_clean_climate_data()
    yield_df = load_and_clean_yield_data()
    
    # Merge datasets
    merged_df = merge_datasets(climate_df, yield_df)
    
    # Save processed data
    save_processed_data(climate_df, 'clean_climate.csv')
    save_processed_data(yield_df, 'clean_yield.csv')
    save_processed_data(merged_df, 'merged_data.csv')
    
    # Generate summary statistics
    generate_summary_statistics(merged_df)
    
    print("\n" + "="*60)
    print("Data preparation complete!")
    print("="*60)
    print(f"\nProcessed files saved in ./data/processed/")
    print(f"Total merged records: {len(merged_df):,}")
    print(f"States: {merged_df['State'].nunique()}")
    print(f"Crops: {merged_df['Crop'].nunique()}")
    print(f"Years: {merged_df['Year'].min()} - {merged_df['Year'].max()}")
    print("\nNext step: Run analysis.py for exploratory data analysis\n")

if __name__ == "__main__":
    main()
