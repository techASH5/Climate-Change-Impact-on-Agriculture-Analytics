# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 1. Installation Issues

#### Problem: `pip install` fails
**Symptoms**: Error messages during package installation

**Solutions**:
```bash
# Try upgrading pip first
python -m pip install --upgrade pip

# Install packages one by one
pip install pandas numpy matplotlib seaborn scikit-learn

# If still failing, try without version constraints
pip install pandas numpy matplotlib seaborn scikit-learn streamlit plotly
```

#### Problem: Permission denied
**Symptoms**: Access denied errors during installation

**Solutions**:
```bash
# Windows: Run as administrator or use --user flag
pip install --user -r requirements.txt

# Or create a virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Data Generation Issues

#### Problem: Script fails to create directories
**Symptoms**: FileNotFoundError or PermissionError

**Solutions**:
```bash
# Manually create directories
mkdir data
mkdir data\raw
mkdir data\processed
mkdir visuals
mkdir models
mkdir scripts

# Then run the script again
python scripts/generate_data.py
```

#### Problem: Out of memory
**Symptoms**: MemoryError during data generation

**Solutions**:
- Reduce the number of years in `generate_data.py`
- Reduce the number of states or crops
- Close other applications to free up RAM

### 3. Analysis Script Issues

#### Problem: Matplotlib/Seaborn plots not showing
**Symptoms**: Scripts run but no images saved

**Solutions**:
```python
# Add this at the top of analysis scripts
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
```

#### Problem: "No module named 'sklearn'"
**Symptoms**: ImportError for sklearn

**Solutions**:
```bash
# Install scikit-learn
pip install scikit-learn

# Note: Import as 'sklearn' but install as 'scikit-learn'
```

### 4. Machine Learning Issues

#### Problem: Model training is very slow
**Symptoms**: ml_model.py takes too long

**Solutions**:
- Reduce `n_estimators` in RandomForestRegressor (e.g., from 100 to 50)
- Use fewer cross-validation folds
- Reduce the dataset size for testing

#### Problem: Poor model performance (low R²)
**Symptoms**: R² score < 0.5

**Solutions**:
- Check data quality (look for NaN values)
- Verify feature scaling if needed
- Try different hyperparameters
- Ensure sufficient training data

### 5. Dashboard Issues

#### Problem: Dashboard won't start
**Symptoms**: Error when running `streamlit run dashboard.py`

**Solutions**:
```bash
# Check if streamlit is installed
pip install streamlit

# Try specifying full path
python -m streamlit run dashboard.py

# Check for port conflicts
streamlit run dashboard.py --server.port 8502
```

#### Problem: "Data files not found" error
**Symptoms**: Dashboard shows error about missing CSV files

**Solutions**:
1. Make sure you've run all previous scripts:
```bash
python scripts/generate_data.py
python scripts/data_prep.py
python scripts/analysis.py
python scripts/vulnerability_analysis.py
python scripts/ml_model.py
```

2. Or run the master script:
```bash
python run_all.py
```

#### Problem: Dashboard looks broken/unstyled
**Symptoms**: Missing colors, poor layout

**Solutions**:
- Clear browser cache
- Try a different browser (Chrome recommended)
- Check if custom CSS is loading
- Verify Streamlit version: `pip install --upgrade streamlit`

#### Problem: Plots not interactive
**Symptoms**: Can't hover or zoom on charts

**Solutions**:
```bash
# Ensure Plotly is installed
pip install plotly

# Update to latest version
pip install --upgrade plotly
```

### 6. Performance Issues

#### Problem: Scripts are very slow
**Symptoms**: Each script takes minutes to run

**Solutions**:
- Reduce data size in `generate_data.py`
- Use fewer states/crops for testing
- Check system resources (CPU, RAM)
- Close unnecessary applications

#### Problem: High memory usage
**Symptoms**: System becomes unresponsive

**Solutions**:
- Process data in chunks
- Use `del` to free variables after use
- Reduce visualization resolution (lower DPI)
- Use `gc.collect()` to force garbage collection

### 7. File Path Issues

#### Problem: "File not found" errors
**Symptoms**: Scripts can't find data files

**Solutions**:
```python
# Use absolute paths or ensure you're in the right directory
import os
os.chdir('c:/Users/mdash/OneDrive/Documents/Data-analytics/climate-change-analytics')

# Or modify scripts to use absolute paths
```

#### Problem: Path separator issues (Windows)
**Symptoms**: Errors with backslashes in paths

**Solutions**:
```python
# Use forward slashes (works on Windows too)
'./data/processed/merged_data.csv'

# Or use os.path.join
import os
os.path.join('data', 'processed', 'merged_data.csv')
```

### 8. Visualization Issues

#### Problem: Plots are blank or corrupted
**Symptoms**: PNG files are empty or show errors

**Solutions**:
```bash
# Reinstall matplotlib
pip uninstall matplotlib
pip install matplotlib

# Try different backend
import matplotlib
matplotlib.use('TkAgg')  # or 'Qt5Agg'
```

#### Problem: Font warnings
**Symptoms**: Warnings about missing fonts

**Solutions**:
- Ignore warnings (they don't affect functionality)
- Or install fonts: `pip install font-manager`

### 9. Data Quality Issues

#### Problem: Unrealistic values in generated data
**Symptoms**: Negative yields, extreme temperatures

**Solutions**:
- Check data generation parameters in `generate_data.py`
- Verify clipping operations are working
- Add validation checks after generation

#### Problem: Merge results in empty dataframe
**Symptoms**: merged_data.csv is empty or very small

**Solutions**:
- Check state name consistency (case, spaces)
- Verify year ranges overlap
- Print intermediate results to debug

### 10. General Debugging Tips

#### Enable Verbose Output
```python
# Add print statements
print(f"Data shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Sample:\n{df.head()}")
```

#### Check Data at Each Step
```python
# After each major operation
df.info()
df.describe()
df.isnull().sum()
```

#### Use Try-Except Blocks
```python
try:
    # Your code
    result = some_function()
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
```

## Getting Help

If you're still stuck:

1. **Check Error Messages**: Read the full error message carefully
2. **Review Code Comments**: Scripts have detailed comments
3. **Check README**: Main documentation has more details
4. **Verify Prerequisites**: Python 3.9+, all packages installed
5. **Test Step-by-Step**: Run each script individually
6. **Check File Permissions**: Ensure you can read/write in the directory

## Quick Diagnostics

Run this diagnostic script to check your setup:

```python
# diagnostic.py
import sys
print(f"Python version: {sys.version}")

packages = ['pandas', 'numpy', 'matplotlib', 'seaborn', 'sklearn', 'streamlit', 'plotly']
for package in packages:
    try:
        __import__(package)
        print(f"✅ {package} installed")
    except ImportError:
        print(f"❌ {package} NOT installed")

import os
print(f"\nCurrent directory: {os.getcwd()}")
print(f"Data directory exists: {os.path.exists('./data')}")
print(f"Scripts directory exists: {os.path.exists('./scripts')}")
```

## Still Need Help?

1. Review the error message carefully
2. Check if the issue is listed above
3. Try the suggested solutions
4. Search for the specific error message online
5. Check package documentation

---

**Remember**: Most issues are due to:
- Missing dependencies
- Wrong working directory
- File path issues
- Insufficient permissions

**Pro Tip**: Always run scripts from the project root directory!
