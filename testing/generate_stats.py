import pandas as pd
import json
import numpy as np

# Load data
print("Loading data...")
df = pd.read_csv('dataset/final_processed_flights.csv', low_memory=False)

# Calculate comprehensive statistics
stats = {}

# Basic stats
stats['total_flights'] = int(len(df))
stats['avg_delay'] = round(float(df['ARRIVAL_DELAY'].mean()), 2)
stats['on_time_pct'] = round(float((df['ARRIVAL_DELAY'] <= 15).mean() * 100), 2)
stats['cancellation_rate'] = round(float(df['CANCELLED'].mean() * 100), 2)
stats['unique_airlines'] = int(df['AIRLINE'].nunique())
stats['unique_routes'] = int(df['ROUTE'].nunique())
stats['avg_dep_delay'] = round(float(df['DEPARTURE_DELAY'].mean()), 2)
stats['avg_distance'] = round(float(df['DISTANCE'].mean()), 2)
stats['diverted_pct'] = round(float(df['DIVERTED'].mean() * 100), 2)

# Delay components
delay_cols = ['AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY']
stats['delay_components'] = {}
for col in delay_cols:
    if col in df.columns:
        val = df[col].mean()
        if not pd.isna(val):
            stats['delay_components'][col] = round(float(val), 2)

# Top airlines by volume
stats['top_airlines'] = df['AIRLINE'].value_counts().head(10).to_dict()

# Best/worst airlines by delay
airline_delays = df.groupby('AIRLINE')['ARRIVAL_DELAY'].mean().sort_values()
stats['best_airline'] = {
    'code': str(airline_delays.index[0]),
    'avg_delay': round(float(airline_delays.iloc[0]), 2)
}
stats['worst_airline'] = {
    'code': str(airline_delays.index[-1]),
    'avg_delay': round(float(airline_delays.iloc[-1]), 2)
}

# Top routes
stats['top_routes'] = df['ROUTE'].value_counts().head(10).to_dict()

# Busiest airports
origin_counts = df['ORIGIN_AIRPORT'].value_counts()
dest_counts = df['DESTINATION_AIRPORT'].value_counts()
total_traffic = origin_counts.add(dest_counts, fill_value=0).sort_values(ascending=False)
stats['busiest_airports'] = total_traffic.head(10).to_dict()

# Temporal patterns
stats['hourly_delays'] = df.groupby('DEP_HOUR')['ARRIVAL_DELAY'].mean().to_dict()
stats['best_hour'] = int(df.groupby('DEP_HOUR')['ARRIVAL_DELAY'].mean().idxmin())
stats['worst_hour'] = int(df.groupby('DEP_HOUR')['ARRIVAL_DELAY'].mean().idxmax())

stats['daily_delays'] = df.groupby('DAY_NAME')['ARRIVAL_DELAY'].mean().to_dict()
stats['seasonal_delays'] = df.groupby('SEASON')['ARRIVAL_DELAY'].mean().to_dict()

# Monthly stats
stats['monthly_flights'] = df.groupby('MONTH').size().to_dict()

# Delay categories
stats['delay_categories'] = df['DELAY_CATEGORY'].value_counts().to_dict()

# Cancellation reasons (if any)
if 'CANCELLATION_REASON' in df.columns:
    cancel_df = df[df['CANCELLED'] == 1]
    if len(cancel_df) > 0:
        stats['cancellation_reasons'] = cancel_df['CANCELLATION_REASON'].value_counts().to_dict()

# Distance categories
stats['distance_categories'] = df['DISTANCE_CATEGORY'].value_counts().to_dict()

# Save to JSON
with open('configuration/analysis_summary.json', 'w') as f:
    json.dump(stats, f, indent=2)

print("Statistics saved to configuration/analysis_summary.json")
print("\nKey Stats:")
print(f"Total Flights: {stats['total_flights']:,}")
print(f"On-Time %: {stats['on_time_pct']}%")
print(f"Avg Delay: {stats['avg_delay']} min")
print(f"Cancellation Rate: {stats['cancellation_rate']}%")
print(f"Best Airline: {stats['best_airline']['code']} ({stats['best_airline']['avg_delay']} min)")
print(f"Worst Airline: {stats['worst_airline']['code']} ({stats['worst_airline']['avg_delay']} min)")
