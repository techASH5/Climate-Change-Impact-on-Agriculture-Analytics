"""
Master Script - Climate Change Impact on Agriculture
Runs the entire data pipeline from data generation to dashboard launch
"""

import subprocess
import sys
import os
from datetime import datetime

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_step(step_num, total_steps, description):
    """Print step information"""
    print(f"\n{'─'*70}")
    print(f"📍 STEP {step_num}/{total_steps}: {description}")
    print(f"{'─'*70}\n")

def run_script(script_path, description):
    """Run a Python script and handle errors"""
    try:
        print(f"▶️  Running: {script_path}")
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        if result.stderr:
            print(f"⚠️  Warnings: {result.stderr}")
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}:")
        print(e.stdout)
        print(e.stderr)
        return False
    except Exception as e:
        print(f"❌ Unexpected error in {description}: {str(e)}")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print_step(0, 6, "Checking Dependencies")
    
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 
        'sklearn', 'streamlit', 'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is NOT installed")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies are installed!")
    return True

def main():
    """Main execution function"""
    start_time = datetime.now()
    
    print_header("🌾 CLIMATE CHANGE IMPACT ON AGRICULTURE - FULL PIPELINE")
    print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies before continuing.")
        sys.exit(1)
    
    # Define pipeline steps
    steps = [
        ("scripts/generate_data.py", "Data Generation"),
        ("scripts/data_prep.py", "Data Preparation & Cleaning"),
        ("scripts/analysis.py", "Exploratory Data Analysis"),
        ("scripts/vulnerability_analysis.py", "Vulnerability Assessment"),
        ("scripts/ml_model.py", "Machine Learning & Predictions"),
    ]
    
    total_steps = len(steps) + 1  # +1 for dashboard
    
    # Execute pipeline
    for i, (script, description) in enumerate(steps, 1):
        print_step(i, total_steps, description)
        
        if not run_script(script, description):
            print(f"\n❌ Pipeline failed at step {i}: {description}")
            print("Please check the error messages above and try again.")
            sys.exit(1)
    
    # Final step: Launch dashboard
    print_step(total_steps, total_steps, "Launching Interactive Dashboard")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n{'='*70}")
    print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"{'='*70}\n")
    print(f"⏱️  Total execution time: {duration:.2f} seconds ({duration/60:.2f} minutes)")
    print(f"\n📊 Generated Outputs:")
    print(f"   • Data files: ./data/processed/")
    print(f"   • Visualizations: ./visuals/")
    print(f"   • ML models: ./models/")
    print(f"\n🚀 Launching dashboard...")
    print(f"\n{'─'*70}")
    print("📱 The dashboard will open in your default web browser")
    print("🌐 Default URL: http://localhost:8501")
    print("⌨️  Press Ctrl+C in the terminal to stop the dashboard")
    print(f"{'─'*70}\n")
    
    # Launch dashboard
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"\n❌ Error launching dashboard: {str(e)}")
        print("You can manually launch it with: streamlit run dashboard.py")

if __name__ == "__main__":
    main()
