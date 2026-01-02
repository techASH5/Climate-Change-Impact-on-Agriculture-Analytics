# 🚀 Quick Start Guide

## Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Complete Pipeline
```bash
python run_all.py
```

This single command will:
1. ✅ Generate synthetic climate and crop yield data
2. ✅ Clean and merge datasets
3. ✅ Perform exploratory data analysis
4. ✅ Calculate vulnerability indices
5. ✅ Train ML models and make predictions
6. ✅ Launch the interactive dashboard

### Step 3: Explore the Dashboard
- The dashboard will automatically open in your browser at `http://localhost:8501`
- Use the sidebar to filter by state and crop
- Explore different tabs for various analyses
- Download data as CSV files

## Alternative: Run Step-by-Step

If you prefer to run each component separately:

```bash
# Generate data
python scripts/generate_data.py

# Clean and merge
python scripts/data_prep.py

# Analyze
python scripts/analysis.py

# Calculate vulnerability
python scripts/vulnerability_analysis.py

# Train ML model
python scripts/ml_model.py

# Launch dashboard
streamlit run dashboard.py
```

## Dashboard Features

### 📊 Historical Trends
- View yield trends over 34 years
- Analyze climate variable changes
- Interactive time series plots

### 🌡️ Climate Impact
- Rainfall vs. yield correlations
- Temperature impact analysis
- Scatter plots with year coloring

### ⚠️ Vulnerability Analysis
- State-wise vulnerability rankings
- Risk category distribution
- Component breakdown

### 🔮 Future Predictions
- Yield projections to 2050
- Two climate scenarios (SSP2-4.5, SSP5-8.5)
- Yield change heatmaps

### 📑 Data Explorer
- Browse all datasets
- Filter and sort data
- Export to CSV

## Troubleshooting

### Issue: Module not found
**Solution**: Make sure all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Dashboard won't start
**Solution**: Run Streamlit directly
```bash
streamlit run dashboard.py
```

### Issue: Port already in use
**Solution**: Specify a different port
```bash
streamlit run dashboard.py --server.port 8502
```

## Project Structure

```
climate-change-analytics/
├── data/
│   ├── raw/              # Generated raw data
│   └── processed/        # Cleaned and merged data
├── scripts/              # Analysis scripts
├── visuals/              # Generated plots
├── models/               # Trained ML models
├── dashboard.py          # Interactive dashboard
└── run_all.py           # Master script
```

## Key Outputs

After running the pipeline, you'll have:

1. **Data Files** (./data/processed/)
   - merged_data.csv
   - vulnerability_index.csv
   - future_predictions.csv
   - yield_change_projections.csv

2. **Visualizations** (./visuals/)
   - yield_trends.png
   - climate_trends.png
   - correlation_heatmap.png
   - vulnerability_index.png
   - future_predictions.png

3. **ML Models** (./models/)
   - yield_prediction_model.pkl
   - state_encoder.pkl
   - crop_encoder.pkl

## Next Steps

1. ✅ Explore the dashboard
2. ✅ Review generated visualizations in ./visuals/
3. ✅ Examine the data in ./data/processed/
4. ✅ Customize the analysis for your needs
5. ✅ Add to your portfolio/GitHub

## Support

For issues or questions:
- Check the main README.md
- Review the code comments
- Examine error messages carefully

---

**Happy Analyzing! 🌾📊**
