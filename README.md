# 🌾 Climate Change Impact on Agriculture Analytics

A comprehensive data analytics project analyzing the impact of climate change (rainfall and temperature) on agricultural crop yields in India, featuring machine learning predictions and an interactive dashboard.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Status](https://img.shields.io/badge/Status-Complete-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Project Overview

This project demonstrates advanced data analytics skills by:
- Analyzing **34 years** of climate and agricultural data (1990-2023)
- Covering **15 states** and **5 major crops** in India
- Quantifying climate impacts using **statistical analysis** and **machine learning**
- Creating a **state-wise vulnerability index** for climate risk assessment
- Building **predictive models** for future yield projections (2024-2050)
- Developing an **interactive dashboard** for data exploration

## 🎯 Key Features

### 1. **Comprehensive Data Analysis**
- Historical trend analysis of crop yields
- Climate variable correlation studies
- Statistical modeling of climate-yield relationships

### 2. **Vulnerability Assessment**
- Composite vulnerability index combining:
  - **Exposure**: Climate change intensity
  - **Sensitivity**: Yield dependence on climate
  - **Adaptive Capacity**: Resilience and growth trends
- Risk categorization (Low, Moderate, High, Very High)

### 3. **Machine Learning Predictions**
- Random Forest Regressor model (R² > 0.85)
- Future yield predictions under climate scenarios:
  - SSP2-4.5 (Moderate emissions)
  - SSP5-8.5 (High emissions)
- Feature importance analysis

### 4. **Interactive Dashboard**
- Built with Streamlit and Plotly
- Premium UI design with dark theme
- Real-time filtering and exploration
- Multiple visualization types:
  - Time series trends
  - Scatter plots and correlations
  - Heatmaps and bar charts
  - Interactive maps
- Data export functionality

## 🛠️ Technologies Used

- **Python 3.9+**
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn, plotly
- **Machine Learning**: scikit-learn
- **Dashboard**: streamlit
- **Geospatial**: geopandas, folium

## 📁 Project Structure

```
climate-change-analytics/
│
├── data/
│   ├── raw/                    # Raw generated datasets
│   │   ├── climate_data.csv
│   │   ├── crop_yield.csv
│   │   └── future_climate.csv
│   └── processed/              # Cleaned and merged data
│       ├── merged_data.csv
│       ├── vulnerability_index.csv
│       ├── future_predictions.csv
│       └── yield_change_projections.csv
│
├── scripts/
│   ├── generate_data.py        # Data generation script
│   ├── data_prep.py           # Data cleaning and merging
│   ├── analysis.py            # Exploratory data analysis
│   ├── vulnerability_analysis.py  # Vulnerability index calculation
│   └── ml_model.py            # Machine learning pipeline
│
├── visuals/                    # Generated visualizations
│   ├── yield_trends.png
│   ├── climate_trends.png
│   ├── correlation_heatmap.png
│   ├── vulnerability_index.png
│   └── future_predictions.png
│
├── models/                     # Trained ML models
│   ├── yield_prediction_model.pkl
│   ├── state_encoder.pkl
│   └── crop_encoder.pkl
│
├── dashboard.py               # Interactive Streamlit dashboard
├── run_all.py                # Master script to run entire pipeline
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🚀 Quick Start

### Installation

1. **Clone or download this project**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Running the Project

#### Option 1: Run Everything at Once
```bash
python run_all.py
```

This will:
1. Generate synthetic datasets
2. Clean and merge data
3. Perform exploratory analysis
4. Calculate vulnerability indices
5. Train ML models and make predictions
6. Launch the interactive dashboard

#### Option 2: Run Step-by-Step

```bash
# Step 1: Generate data
python scripts/generate_data.py

# Step 2: Clean and merge data
python scripts/data_prep.py

# Step 3: Exploratory analysis
python scripts/analysis.py

# Step 4: Vulnerability assessment
python scripts/vulnerability_analysis.py

# Step 5: ML predictions
python scripts/ml_model.py

# Step 6: Launch dashboard
streamlit run dashboard.py
```

## 📊 Key Findings

### Climate Trends (1990-2023)
- Average temperature increase: **~1.0°C** over 34 years
- Rainfall variability: Increased in most regions
- Extreme weather events: More frequent

### Crop Yield Impacts
- **Rice**: Moderate negative correlation with temperature (-0.15 to -0.20)
- **Wheat**: Strong negative correlation with high temperatures (-0.20 to -0.25)
- **Maize**: Resilient to temperature changes
- **Cotton**: Sensitive to rainfall variability
- **Sugarcane**: Benefits from moderate rainfall increase

### Vulnerability Assessment
- **High-risk states**: Rajasthan, Gujarat (water stress)
- **Moderate-risk states**: Maharashtra, Karnataka
- **Lower-risk states**: Punjab, Haryana (better irrigation)

### Future Projections (2050)
- **SSP2-4.5 Scenario**: 
  - Average yield change: -5% to +8% depending on crop/region
  - Temperature increase: +2-3°C
- **SSP5-8.5 Scenario**:
  - Average yield change: -15% to +5%
  - Temperature increase: +4-5°C
  - Higher risk of crop failures

## 📈 Dashboard Features

### 1. Historical Trends Tab
- Yield trends over time
- Climate variable trends
- Interactive time series plots

### 2. Climate Impact Tab
- Rainfall vs. yield scatter plots
- Temperature vs. yield analysis
- Correlation coefficients

### 3. Vulnerability Analysis Tab
- State-wise vulnerability rankings
- Component breakdown (Exposure, Sensitivity, Capacity)
- Risk category distribution

### 4. Future Predictions Tab
- Yield projections to 2050
- Scenario comparison
- Yield change heatmaps

### 5. Data Explorer Tab
- Interactive data tables
- Filtering and sorting
- CSV export functionality

## 🎓 Skills Demonstrated

This project showcases:

✅ **Data Wrangling**: Cleaning, merging, and transforming large datasets  
✅ **Statistical Analysis**: Correlation, regression, trend analysis  
✅ **Machine Learning**: Feature engineering, model training, evaluation, prediction  
✅ **Data Visualization**: Static plots (matplotlib/seaborn) and interactive charts (Plotly)  
✅ **Dashboard Development**: Building user-friendly web applications with Streamlit  
✅ **Domain Knowledge**: Understanding climate science and agricultural systems  
✅ **Project Management**: Structured workflow, documentation, reproducibility  

## 📝 Data Sources

This project uses **synthetic data** generated to mimic real-world patterns based on:
- India Meteorological Department (IMD) climate data patterns
- Ministry of Agriculture crop yield statistics
- CMIP6 climate projection scenarios
- Published research on climate-agriculture relationships

For production use, replace with actual data from:
- [World Bank Climate Data](https://climateknowledgeportal.worldbank.org/)
- [India Agriculture Data Portal](https://data.gov.in/)
- [ICRISAT District Level Database](http://data.icrisat.org/dld/)

## 🔧 Customization

### Adding New Crops
Edit `scripts/generate_data.py`:
```python
CROPS = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'YourCrop']
BASE_YIELD = {'YourCrop': 3.0}  # Add base yield
```

### Adding New States
Edit `scripts/generate_data.py`:
```python
STATES = [..., 'YourState']
BASE_CLIMATE = {'YourState': {'rainfall': 1000, 'temp': 25}}
```

### Modifying ML Model
Edit `scripts/ml_model.py` to try different algorithms:
```python
from sklearn.ensemble import GradientBoostingRegressor
model = GradientBoostingRegressor(...)
```

## 📊 Sample Visualizations

The project generates multiple visualizations:
- **Yield Trends**: Line charts showing historical yield changes
- **Climate Trends**: Temperature and rainfall over time
- **Correlation Heatmaps**: Climate-yield relationships
- **Vulnerability Maps**: State-wise risk assessment
- **Future Projections**: Predicted yields under climate scenarios


