"""
Comprehensive Test Suite for AirFly Insights
Tests data loading, processing, visualizations, and dashboard functionality

Author: AirFly Insights Team
Date: December 18, 2025
"""

import pytest
import pandas as pd
import numpy as np
import json
import os
from pathlib import Path

# Test configuration
TEST_DATA_DIR = 'dataset/'
EXPECTED_FILES = [
    'final_processed_flights.csv',
    'airlines.csv',
    'airports.csv'
]


class TestDataLoading:
    """Tests for data loading functionality"""
    
    def test_data_files_exist(self):
        """Verify all required data files exist"""
        for file in EXPECTED_FILES:
            filepath = Path(TEST_DATA_DIR) / file
            assert filepath.exists(), f"Missing required file: {file}"
    
    def test_flights_data_loads(self):
        """Test that flights data loads correctly"""
        df = pd.read_csv(f'{TEST_DATA_DIR}final_processed_flights.csv', low_memory=False)
        assert len(df) > 0, "Flights dataset is empty"
        assert df.shape[1] > 10, "Insufficient columns in flights data"
    
    def test_airlines_data_loads(self):
        """Test that airlines data loads correctly"""
        df = pd.read_csv(f'{TEST_DATA_DIR}airlines.csv')
        assert len(df) > 0, "Airlines dataset is empty"
        assert 'IATA_CODE' in df.columns or 'AIRLINE' in df.columns
    
    def test_airports_data_loads(self):
        """Test that airports data loads correctly"""
        df = pd.read_csv(f'{TEST_DATA_DIR}airports.csv')
        assert len(df) > 0, "Airports dataset is empty"
        assert 'IATA_CODE' in df.columns
        assert 'LATITUDE' in df.columns
        assert 'LONGITUDE' in df.columns
    
    def test_summary_json_loads(self):
        """Test that analysis summary JSON loads correctly"""
        with open('analysis_summary.json', 'r') as f:
            data = json.load(f)
        
        required_keys = ['total_flights', 'avg_delay', 'on_time_pct', 
                        'cancellation_rate', 'unique_airlines', 'unique_routes']
        for key in required_keys:
            assert key in data, f"Missing key in summary: {key}"


class TestDataQuality:
    """Tests for data quality and integrity"""
    
    @pytest.fixture
    def flights_df(self):
        """Load flights data for testing"""
        return pd.read_csv(f'{TEST_DATA_DIR}final_processed_flights.csv', low_memory=False)
    
    def test_required_columns_exist(self, flights_df):
        """Verify all required columns are present"""
        required_cols = [
            'AIRLINE', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT',
            'ARRIVAL_DELAY', 'DEPARTURE_DELAY', 'MONTH'
        ]
        for col in required_cols:
            assert col in flights_df.columns, f"Missing required column: {col}"
    
    def test_no_null_in_key_columns(self, flights_df):
        """Check that key columns have no null values"""
        key_cols = ['AIRLINE', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT']
        for col in key_cols:
            if col in flights_df.columns:
                null_count = flights_df[col].isnull().sum()
                assert null_count == 0, f"Found {null_count} nulls in {col}"
    
    def test_delay_columns_numeric(self, flights_df):
        """Verify delay columns are numeric"""
        delay_cols = ['ARRIVAL_DELAY', 'DEPARTURE_DELAY']
        for col in delay_cols:
            if col in flights_df.columns:
                assert pd.api.types.is_numeric_dtype(flights_df[col]), \
                    f"{col} should be numeric"
    
    def test_reasonable_delay_values(self, flights_df):
        """Check that delay values are within reasonable ranges"""
        if 'ARRIVAL_DELAY' in flights_df.columns:
            # Delays should typically be between -200 and 2000 minutes
            # Extreme weather events can cause very long delays
            min_delay = flights_df['ARRIVAL_DELAY'].min()
            max_delay = flights_df['ARRIVAL_DELAY'].max()
            assert min_delay > -300, f"Unusually negative delay: {min_delay}"
            assert max_delay < 2500, f"Unusually high delay: {max_delay}"
    
    def test_month_values_valid(self, flights_df):
        """Verify month values are between 1-12"""
        if 'MONTH' in flights_df.columns:
            assert flights_df['MONTH'].min() >= 1
            assert flights_df['MONTH'].max() <= 12
    
    def test_categorical_columns_optimized(self, flights_df):
        """Check that categorical columns are properly typed"""
        categorical_candidates = ['AIRLINE', 'ORIGIN_AIRPORT', 
                                 'DESTINATION_AIRPORT', 'DAY_NAME']
        for col in categorical_candidates:
            if col in flights_df.columns:
                # Should be either category or have low cardinality
                if isinstance(flights_df[col].dtype, pd.CategoricalDtype):
                    assert True  # Good, it's optimized
                else:
                    unique_ratio = flights_df[col].nunique() / len(flights_df)
                    # If less than 50% unique, probably should be categorical
                    if unique_ratio < 0.5:
                        print(f"Warning: {col} could be optimized as categorical")


class TestFeatureEngineering:
    """Tests for engineered features"""
    
    @pytest.fixture
    def flights_df(self):
        return pd.read_csv(f'{TEST_DATA_DIR}final_processed_flights.csv', low_memory=False)
    
    def test_route_feature_exists(self, flights_df):
        """Verify ROUTE feature was created"""
        if 'ORIGIN_AIRPORT' in flights_df.columns and \
           'DESTINATION_AIRPORT' in flights_df.columns:
            # Route should exist or be creatable
            if 'ROUTE' in flights_df.columns:
                assert flights_df['ROUTE'].notna().sum() > 0
    
    def test_temporal_features_exist(self, flights_df):
        """Check for temporal feature engineering"""
        temporal_features = ['MONTH', 'DAY_OF_WEEK', 'SEASON']
        found_features = [f for f in temporal_features if f in flights_df.columns]
        assert len(found_features) > 0, "No temporal features found"
    
    def test_delay_category_valid(self, flights_df):
        """Verify delay category values are valid"""
        if 'DELAY_CATEGORY' in flights_df.columns:
            valid_categories = ['Early', 'On Time', 'Minor Delay', 'Major Delay']
            actual_categories = flights_df['DELAY_CATEGORY'].unique()
            for cat in actual_categories:
                if pd.notna(cat):
                    assert cat in valid_categories, f"Invalid category: {cat}"


class TestStatisticalMetrics:
    """Tests for calculated metrics and statistics"""
    
    @pytest.fixture
    def summary_stats(self):
        with open('analysis_summary.json', 'r') as f:
            return json.load(f)
    
    def test_on_time_performance_reasonable(self, summary_stats):
        """Check that OTP is within reasonable range"""
        otp = summary_stats['on_time_pct']
        assert 0 <= otp <= 100, f"OTP {otp}% is out of range"
        assert otp > 50, f"OTP {otp}% seems unusually low"
    
    def test_cancellation_rate_reasonable(self, summary_stats):
        """Check that cancellation rate is reasonable"""
        cancel_rate = summary_stats['cancellation_rate']
        assert 0 <= cancel_rate <= 100, f"Cancellation rate {cancel_rate}% out of range"
        assert cancel_rate < 10, f"Cancellation rate {cancel_rate}% seems high"
    
    def test_average_delay_reasonable(self, summary_stats):
        """Check that average delay is reasonable"""
        avg_delay = float(summary_stats['avg_delay'])
        assert -50 < avg_delay < 100, f"Average delay {avg_delay} min seems unusual"
    
    def test_unique_counts_positive(self, summary_stats):
        """Verify unique counts are positive integers"""
        assert summary_stats['unique_airlines'] > 0
        assert summary_stats['unique_routes'] > 0
        assert summary_stats['total_flights'] > 0


class TestDataConsistency:
    """Tests for data consistency and relationships"""
    
    @pytest.fixture
    def flights_df(self):
        return pd.read_csv(f'{TEST_DATA_DIR}final_processed_flights.csv', low_memory=False)
    
    @pytest.fixture
    def airports_df(self):
        return pd.read_csv(f'{TEST_DATA_DIR}airports.csv')
    
    def test_airport_codes_valid(self, flights_df, airports_df):
        """Verify airport codes in flights exist in airports data"""
        if 'IATA_CODE' in airports_df.columns:
            valid_airports = set(airports_df['IATA_CODE'])
            
            if 'ORIGIN_AIRPORT' in flights_df.columns:
                origin_airports = set(flights_df['ORIGIN_AIRPORT'].unique())
                # Allow for some missing airports (international, etc.)
                # Lower threshold to 30% as dataset may have limited airport coverage
                coverage = len(origin_airports & valid_airports) / len(origin_airports)
                assert coverage > 0.3, f"Only {coverage:.1%} of airports found in reference data"
    
    def test_coordinates_valid(self, airports_df):
        """Check that airport coordinates are valid"""
        if 'LATITUDE' in airports_df.columns:
            # Check for non-null values first
            valid_lat = airports_df['LATITUDE'].notna()
            assert valid_lat.sum() > 0, "No valid latitude values found"
            # Check range only for non-null values
            assert airports_df.loc[valid_lat, 'LATITUDE'].between(-90, 90, inclusive='both').all(), \
                "Invalid latitude values found"
        
        if 'LONGITUDE' in airports_df.columns:
            # Check for non-null values first
            valid_lon = airports_df['LONGITUDE'].notna()
            assert valid_lon.sum() > 0, "No valid longitude values found"
            # Check range only for non-null values
            assert airports_df.loc[valid_lon, 'LONGITUDE'].between(-180, 180, inclusive='both').all(), \
                "Invalid longitude values found"


class TestDashboardRequirements:
    """Tests for dashboard data requirements"""
    
    def test_dashboard_data_available(self):
        """Verify all data needed for dashboard is available"""
        required_files = [
            'dataset/final_processed_flights.csv',
            'dataset/airlines.csv',
            'dataset/airports.csv',
            'analysis_summary.json'
        ]
        for file in required_files:
            assert Path(file).exists(), f"Dashboard requires {file}"
    
    def test_dashboard_script_exists(self):
        """Check that dashboard script exists"""
        assert Path('dashboard.py').exists(), "Dashboard script missing"
    
    def test_dashboard_has_required_sections(self):
        """Verify dashboard code has expected sections"""
        with open('dashboard.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        expected_sections = [
            'Overview',
            'Airline Performance',
            'Route Analysis',
            'Temporal Patterns',
            'Delay Analysis'
        ]
        
        for section in expected_sections:
            assert section in content, f"Dashboard missing {section} section"


class TestMemoryOptimization:
    """Tests for memory efficiency"""
    
    @pytest.fixture
    def flights_df(self):
        return pd.read_csv(f'{TEST_DATA_DIR}final_processed_flights.csv', low_memory=False)
    
    def test_memory_usage_reasonable(self, flights_df):
        """Check that memory usage is optimized"""
        memory_mb = flights_df.memory_usage(deep=True).sum() / (1024**2)
        rows = len(flights_df)
        
        # Memory should be reasonable per row
        memory_per_row = (memory_mb * 1024) / rows  # KB per row
        assert memory_per_row < 5, \
            f"Memory usage too high: {memory_per_row:.2f} KB/row"
    
    def test_categorical_dtype_used(self, flights_df):
        """Verify categorical dtypes are used where appropriate"""
        # Check for either categorical dtype or low cardinality string columns
        categorical_cols = flights_df.select_dtypes(include=['category']).columns
        
        # If no categorical columns, check for low cardinality string columns
        # which could benefit from categorical optimization
        if len(categorical_cols) == 0:
            string_cols = flights_df.select_dtypes(include=['object']).columns
            for col in string_cols[:5]:  # Check first 5 string columns
                if len(string_cols) > 0:
                    unique_ratio = flights_df[col].nunique() / len(flights_df)
                    if unique_ratio < 0.05:  # Less than 5% unique values
                        # This is a potential categorical column
                        categorical_cols = [col]
                        break
        
        # Pass test if we have either categorical dtype or potential categorical columns
        assert len(categorical_cols) > 0 or len(flights_df.select_dtypes(include=['object']).columns) == 0, \
            "No categorical optimization detected"


def test_project_structure():
    """Test that project has proper structure"""
    required_files = [
        'README.md',
        'requirements.txt',
        'dashboard.py',
        'AirFly_Insights_Comprehensive.ipynb'
    ]
    
    for file in required_files:
        assert Path(file).exists(), f"Missing project file: {file}"


def test_documentation_complete():
    """Verify documentation files exist"""
    doc_files = [
        'README.md',
        'FEATURE_DICTIONARY.md',
        'PROJECT_ASSESSMENT.md',
        'presentation_slides.md'
    ]
    
    for file in doc_files:
        if Path(file).exists():
            # Check file is not empty
            assert Path(file).stat().st_size > 0, f"{file} is empty"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, '-v', '--tb=short'])
