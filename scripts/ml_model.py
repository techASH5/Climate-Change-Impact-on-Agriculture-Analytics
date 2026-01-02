"""
Machine Learning Model for Yield Prediction
Trains models to predict future crop yields under climate scenarios
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os

def load_data():
    """Load historical and future climate data"""
    print("Loading data...")
    
    historical_df = pd.read_csv('./data/processed/merged_data.csv')
    future_climate_df = pd.read_csv('./data/raw/future_climate.csv')
    
    print(f"✓ Historical data: {len(historical_df):,} records")
    print(f"✓ Future climate data: {len(future_climate_df):,} records")
    
    return historical_df, future_climate_df

def prepare_features(df):
    """Prepare features for machine learning"""
    print("\nPreparing features...")
    
    # Encode categorical variables
    le_state = LabelEncoder()
    le_crop = LabelEncoder()
    
    df['State_Encoded'] = le_state.fit_transform(df['State'])
    df['Crop_Encoded'] = le_crop.fit_transform(df['Crop'])
    
    # Create additional features
    df['Year_Normalized'] = (df['Year'] - df['Year'].min()) / (df['Year'].max() - df['Year'].min())
    df['Rainfall_Temp_Interaction'] = df['Rainfall_mm'] * df['Avg_Temp_C']
    
    # Feature columns
    feature_cols = [
        'Year', 'Year_Normalized', 'State_Encoded', 'Crop_Encoded',
        'Rainfall_mm', 'Avg_Temp_C', 'Rainfall_Temp_Interaction'
    ]
    
    print(f"✓ Features prepared: {len(feature_cols)} features")
    
    return df, feature_cols, le_state, le_crop

def train_model(X_train, X_test, y_train, y_test):
    """Train Random Forest model"""
    print("\nTraining Random Forest model...")
    
    # Initialize model
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    # Train
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
    test_mae = mean_absolute_error(y_test, y_pred_test)
    
    print(f"\n✓ Model trained successfully")
    print(f"  Training R²: {train_r2:.4f}")
    print(f"  Testing R²: {test_r2:.4f}")
    print(f"  Testing RMSE: {test_rmse:.4f}")
    print(f"  Testing MAE: {test_mae:.4f}")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, 
                                 scoring='r2', n_jobs=-1)
    print(f"  Cross-validation R² (mean): {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    
    return model, {
        'train_r2': train_r2,
        'test_r2': test_r2,
        'test_rmse': test_rmse,
        'test_mae': test_mae,
        'cv_r2_mean': cv_scores.mean(),
        'cv_r2_std': cv_scores.std()
    }

def analyze_feature_importance(model, feature_cols):
    """Analyze and visualize feature importance"""
    print("\nAnalyzing feature importance...")
    
    importance_df = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print("\nFeature Importance:")
    print(importance_df.to_string(index=False))
    
    # Visualize
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = sns.color_palette('viridis', len(importance_df))
    bars = ax.barh(importance_df['Feature'], importance_df['Importance'], color=colors)
    
    ax.set_xlabel('Importance', fontsize=12, fontweight='bold')
    ax.set_ylabel('Feature', fontsize=12, fontweight='bold')
    ax.set_title('Feature Importance in Yield Prediction Model', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig('./visuals/feature_importance.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: feature_importance.png")
    plt.close()
    
    return importance_df

def predict_future_yields(model, future_climate_df, le_state, le_crop, feature_cols):
    """Predict future yields under different scenarios"""
    print("\nPredicting future yields...")
    
    # Prepare future data for each crop
    crops = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane']
    all_predictions = []
    
    for scenario in future_climate_df['Scenario'].unique():
        scenario_data = future_climate_df[future_climate_df['Scenario'] == scenario].copy()
        
        for crop in crops:
            # Create prediction dataset
            pred_data = scenario_data.copy()
            pred_data['Crop'] = crop
            
            # Encode
            pred_data['State_Encoded'] = le_state.transform(pred_data['State'])
            pred_data['Crop_Encoded'] = le_crop.transform(pred_data['Crop'])
            
            # Create features
            pred_data['Year_Normalized'] = (pred_data['Year'] - 1990) / (2050 - 1990)
            pred_data['Rainfall_Temp_Interaction'] = pred_data['Rainfall_mm'] * pred_data['Avg_Temp_C']
            
            # Predict
            X_future = pred_data[feature_cols]
            predictions = model.predict(X_future)
            
            pred_data['Predicted_Yield'] = predictions
            pred_data['Crop'] = crop
            
            all_predictions.append(pred_data[['Year', 'State', 'Scenario', 'Crop', 
                                              'Rainfall_mm', 'Avg_Temp_C', 'Predicted_Yield']])
    
    future_predictions_df = pd.concat(all_predictions, ignore_index=True)
    
    print(f"✓ Generated {len(future_predictions_df):,} future predictions")
    
    return future_predictions_df

def visualize_predictions(historical_df, future_predictions_df):
    """Visualize historical and predicted yields"""
    print("\nCreating prediction visualizations...")
    
    # Select major crops and states for visualization
    crops = ['Rice', 'Wheat', 'Maize']
    states = ['Punjab', 'Uttar Pradesh', 'Maharashtra']
    
    fig, axes = plt.subplots(len(crops), len(states), figsize=(18, 12))
    fig.suptitle('Historical and Predicted Crop Yields (2024-2050)', 
                 fontsize=16, fontweight='bold')
    
    for i, crop in enumerate(crops):
        for j, state in enumerate(states):
            ax = axes[i, j]
            
            # Historical data
            hist_data = historical_df[(historical_df['Crop'] == crop) & 
                                     (historical_df['State'] == state)]
            hist_yearly = hist_data.groupby('Year')['Yield_ton_per_ha'].mean().reset_index()
            
            # Future predictions (both scenarios)
            future_ssp245 = future_predictions_df[
                (future_predictions_df['Crop'] == crop) & 
                (future_predictions_df['State'] == state) &
                (future_predictions_df['Scenario'] == 'SSP2-4.5')
            ].groupby('Year')['Predicted_Yield'].mean().reset_index()
            
            future_ssp585 = future_predictions_df[
                (future_predictions_df['Crop'] == crop) & 
                (future_predictions_df['State'] == state) &
                (future_predictions_df['Scenario'] == 'SSP5-8.5')
            ].groupby('Year')['Predicted_Yield'].mean().reset_index()
            
            # Plot
            ax.plot(hist_yearly['Year'], hist_yearly['Yield_ton_per_ha'], 
                   'o-', linewidth=2, markersize=3, label='Historical', color='#2c3e50')
            ax.plot(future_ssp245['Year'], future_ssp245['Predicted_Yield'], 
                   's-', linewidth=2, markersize=3, label='SSP2-4.5', color='#f39c12')
            ax.plot(future_ssp585['Year'], future_ssp585['Predicted_Yield'], 
                   '^-', linewidth=2, markersize=3, label='SSP5-8.5', color='#e74c3c')
            
            ax.axvline(x=2023, color='gray', linestyle='--', alpha=0.5)
            ax.set_title(f'{crop} - {state}', fontweight='bold', fontsize=10)
            ax.set_xlabel('Year', fontsize=9)
            ax.set_ylabel('Yield (ton/ha)', fontsize=9)
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=8)
    
    plt.tight_layout()
    plt.savefig('./visuals/future_predictions.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: future_predictions.png")
    plt.close()

def calculate_yield_changes(historical_df, future_predictions_df):
    """Calculate expected yield changes"""
    print("\nCalculating yield changes...")
    
    # Get baseline (2015-2023 average)
    baseline = historical_df[historical_df['Year'] >= 2015].groupby(['State', 'Crop'])['Yield_ton_per_ha'].mean().reset_index()
    baseline.columns = ['State', 'Crop', 'Baseline_Yield']
    
    # Get future predictions (2040-2050 average)
    future_avg = future_predictions_df[future_predictions_df['Year'] >= 2040].groupby(
        ['State', 'Crop', 'Scenario']
    )['Predicted_Yield'].mean().reset_index()
    
    # Merge and calculate changes
    changes = future_avg.merge(baseline, on=['State', 'Crop'])
    changes['Yield_Change_Percent'] = ((changes['Predicted_Yield'] - changes['Baseline_Yield']) / 
                                        changes['Baseline_Yield'] * 100)
    
    changes.to_csv('./data/processed/yield_change_projections.csv', index=False)
    print("✓ Saved: yield_change_projections.csv")
    
    # Summary by scenario
    print("\nProjected Yield Changes (2040-2050 vs 2015-2023):")
    print("="*60)
    
    for scenario in changes['Scenario'].unique():
        scenario_data = changes[changes['Scenario'] == scenario]
        print(f"\n{scenario}:")
        print(f"  Average change: {scenario_data['Yield_Change_Percent'].mean():.2f}%")
        print(f"  Range: {scenario_data['Yield_Change_Percent'].min():.2f}% to {scenario_data['Yield_Change_Percent'].max():.2f}%")
    
    return changes

def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("Machine Learning Model Training and Prediction")
    print("="*60 + "\n")
    
    # Create directories
    os.makedirs('./models', exist_ok=True)
    os.makedirs('./visuals', exist_ok=True)
    
    # Load data
    historical_df, future_climate_df = load_data()
    
    # Prepare features
    historical_df, feature_cols, le_state, le_crop = prepare_features(historical_df)
    
    # Split data
    X = historical_df[feature_cols]
    y = historical_df['Yield_ton_per_ha']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"\nTraining set: {len(X_train):,} samples")
    print(f"Testing set: {len(X_test):,} samples")
    
    # Train model
    model, metrics = train_model(X_train, X_test, y_train, y_test)
    
    # Analyze feature importance
    importance_df = analyze_feature_importance(model, feature_cols)
    
    # Save model and encoders
    joblib.dump(model, './models/yield_prediction_model.pkl')
    joblib.dump(le_state, './models/state_encoder.pkl')
    joblib.dump(le_crop, './models/crop_encoder.pkl')
    joblib.dump(feature_cols, './models/feature_cols.pkl')
    print("\n✓ Model and encoders saved")
    
    # Predict future yields
    future_predictions_df = predict_future_yields(
        model, future_climate_df, le_state, le_crop, feature_cols
    )
    
    # Save predictions
    future_predictions_df.to_csv('./data/processed/future_predictions.csv', index=False)
    print("✓ Saved: future_predictions.csv")
    
    # Visualize predictions
    visualize_predictions(historical_df, future_predictions_df)
    
    # Calculate yield changes
    yield_changes = calculate_yield_changes(historical_df, future_predictions_df)
    
    print("\n" + "="*60)
    print("Machine learning pipeline complete!")
    print("="*60)
    print(f"\nModel Performance:")
    print(f"  R² Score: {metrics['test_r2']:.4f}")
    print(f"  RMSE: {metrics['test_rmse']:.4f}")
    print(f"\nNext step: Run streamlit run dashboard.py\n")

if __name__ == "__main__":
    main()
