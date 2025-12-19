#!/usr/bin/env python3
"""
Quick test script for AirFly Insights Dashboard
"""

import pandas as pd
import json
import os

def test_data_loading():
    """Test if all required data files can be loaded"""
    print("🧪 Testing AirFly Insights Dashboard Data Loading")
    print("=" * 50)

    # Test main data files
    files_to_test = [
        'dataset/final_processed_flights.csv',
        'dataset/airlines.csv',
        'dataset/airports.csv',
        'analysis_summary.json'
    ]

    all_good = True

    for file_path in files_to_test:
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
                print(f"✅ {file_path}: {df.shape[0]} rows, {df.shape[1]} columns")
            elif file_path.endswith('.json'):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                print(f"✅ {file_path}: {len(data)} metrics loaded")
        except Exception as e:
            print(f"❌ {file_path}: Error - {e}")
            all_good = False

    # Test key columns exist
    try:
        flights_df = pd.read_csv('dataset/final_processed_flights.csv', nrows=100)
        required_columns = ['AIRLINE', 'ARRIVAL_DELAY', 'DEPARTURE_DELAY', 'ROUTE', 'MONTH']
        missing_cols = [col for col in required_columns if col not in flights_df.columns]

        if missing_cols:
            print(f"⚠️  Missing required columns: {missing_cols}")
            all_good = False
        else:
            print(f"✅ All required columns present ({len(flights_df.columns)} total columns)")
    except Exception as e:
        print(f"❌ Column check failed: {e}")
        all_good = False

    print("=" * 50)
    if all_good:
        print("🎉 All tests passed! Dashboard should work properly.")
        print("\n🚀 To run the dashboard:")
        print("   streamlit run dashboard.py")
        print("   # or double-click run_dashboard.bat")
        print("   # or python run_dashboard.py")
    else:
        print("⚠️  Some issues found. Please check the data files.")

    return all_good

if __name__ == "__main__":
    test_data_loading()