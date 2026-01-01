"""
Geographic Analysis Module for AirFly Insights
Adds interactive map visualizations using folium

Author: AirFly Insights Team
Date: December 18, 2025
"""

import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
import json

def create_airport_delay_map(flights_df, airports_df, output_file='airport_delay_map.html'):
    """
    Create an interactive map showing airports colored by average delay
    
    Parameters:
    -----------
    flights_df : DataFrame
        Processed flights data with delay information
    airports_df : DataFrame
        Airport data with lat/lon coordinates
    output_file : str
        Output HTML file path
    
    Returns:
    --------
    folium.Map : The created map object
    """
    
    # Calculate average delay by airport (destination)
    airport_delays = flights_df.groupby('DESTINATION_AIRPORT').agg({
        'ARRIVAL_DELAY': ['mean', 'count']
    }).reset_index()
    airport_delays.columns = ['IATA_CODE', 'avg_delay', 'flight_count']
    
    # Merge with airport coordinates
    airport_data = airport_delays.merge(
        airports_df[['IATA_CODE', 'LATITUDE', 'LONGITUDE', 'AIRPORT', 'CITY']], 
        on='IATA_CODE', 
        how='inner'
    )
    
    # Remove rows with missing coordinates
    airport_data = airport_data.dropna(subset=['LATITUDE', 'LONGITUDE'])
    
    # Create base map centered on US
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4, 
                   tiles='OpenStreetMap')
    
    # Define color scheme based on delay
    def get_color(delay):
        if delay < 0:
            return 'green'  # Early
        elif delay < 10:
            return 'lightgreen'  # Minimal delay
        elif delay < 20:
            return 'orange'  # Moderate delay
        else:
            return 'red'  # Significant delay
    
    # Add markers for each airport
    for idx, row in airport_data.iterrows():
        folium.CircleMarker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            radius=min(row['flight_count'] / 500, 15),  # Size by traffic
            popup=f"""
                <b>{row['AIRPORT']}</b><br>
                {row['CITY']}<br>
                Code: {row['IATA_CODE']}<br>
                Avg Delay: {row['avg_delay']:.1f} min<br>
                Flights: {row['flight_count']:,}
            """,
            color=get_color(row['avg_delay']),
            fill=True,
            fillColor=get_color(row['avg_delay']),
            fillOpacity=0.7,
            weight=2
        ).add_to(m)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: 140px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <p style="margin-bottom: 5px;"><b>Average Delay</b></p>
    <p><span style="color: green;">●</span> Early (< 0 min)</p>
    <p><span style="color: lightgreen;">●</span> Minimal (0-10 min)</p>
    <p><span style="color: orange;">●</span> Moderate (10-20 min)</p>
    <p><span style="color: red;">●</span> Significant (> 20 min)</p>
    <p style="font-size: 11px; margin-top: 10px;">Circle size = traffic volume</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save map
    m.save(output_file)
    print(f"Airport delay map saved to {output_file}")
    
    return m


def create_route_flow_map(flights_df, airports_df, top_n=50, output_file='route_flow_map.html'):
    """
    Create an interactive map showing top flight routes with lines
    
    Parameters:
    -----------
    flights_df : DataFrame
        Processed flights data
    airports_df : DataFrame
        Airport data with coordinates
    top_n : int
        Number of top routes to display
    output_file : str
        Output HTML file path
    
    Returns:
    --------
    folium.Map : The created map object
    """
    
    # Get top routes by volume
    top_routes = flights_df['ROUTE'].value_counts().head(top_n).index.tolist()
    route_data = flights_df[flights_df['ROUTE'].isin(top_routes)].copy()
    
    # Calculate route statistics
    route_stats = route_data.groupby('ROUTE').agg({
        'ARRIVAL_DELAY': ['mean', 'count']
    }).reset_index()
    route_stats.columns = ['ROUTE', 'avg_delay', 'flight_count']
    
    # Split route into origin and destination
    route_stats[['ORIGIN', 'DEST']] = route_stats['ROUTE'].str.split('-', expand=True)
    
    # Merge with airport coordinates
    route_stats = route_stats.merge(
        airports_df[['IATA_CODE', 'LATITUDE', 'LONGITUDE']], 
        left_on='ORIGIN', 
        right_on='IATA_CODE',
        how='left'
    ).rename(columns={'LATITUDE': 'ORIGIN_LAT', 'LONGITUDE': 'ORIGIN_LON'})
    
    route_stats = route_stats.merge(
        airports_df[['IATA_CODE', 'LATITUDE', 'LONGITUDE']], 
        left_on='DEST', 
        right_on='IATA_CODE',
        how='left'
    ).rename(columns={'LATITUDE': 'DEST_LAT', 'LONGITUDE': 'DEST_LON'})
    
    # Remove rows with missing coordinates
    route_stats = route_stats.dropna(subset=['ORIGIN_LAT', 'ORIGIN_LON', 'DEST_LAT', 'DEST_LON'])
    
    # Create base map
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
    
    # Add route lines
    for idx, row in route_stats.iterrows():
        # Determine line color based on delay
        if row['avg_delay'] < 5:
            color = 'green'
        elif row['avg_delay'] < 15:
            color = 'orange'
        else:
            color = 'red'
        
        # Line thickness based on traffic
        weight = min(row['flight_count'] / 200, 8)
        
        folium.PolyLine(
            locations=[
                [row['ORIGIN_LAT'], row['ORIGIN_LON']],
                [row['DEST_LAT'], row['DEST_LON']]
            ],
            color=color,
            weight=weight,
            opacity=0.6,
            popup=f"""
                <b>Route: {row['ROUTE']}</b><br>
                Flights: {row['flight_count']:,}<br>
                Avg Delay: {row['avg_delay']:.1f} min
            """
        ).add_to(m)
    
    # Add airport markers
    unique_airports = pd.concat([
        route_stats[['ORIGIN', 'ORIGIN_LAT', 'ORIGIN_LON']].rename(
            columns={'ORIGIN': 'CODE', 'ORIGIN_LAT': 'LAT', 'ORIGIN_LON': 'LON'}
        ),
        route_stats[['DEST', 'DEST_LAT', 'DEST_LON']].rename(
            columns={'DEST': 'CODE', 'DEST_LAT': 'LAT', 'DEST_LON': 'LON'}
        )
    ]).drop_duplicates()
    
    for idx, row in unique_airports.iterrows():
        folium.CircleMarker(
            location=[row['LAT'], row['LON']],
            radius=5,
            color='blue',
            fill=True,
            fillColor='blue',
            fillOpacity=0.8,
            popup=f"<b>{row['CODE']}</b>"
        ).add_to(m)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: 120px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <p style="margin-bottom: 5px;"><b>Route Performance</b></p>
    <p><span style="color: green;">━━</span> Good (< 5 min delay)</p>
    <p><span style="color: orange;">━━</span> Fair (5-15 min)</p>
    <p><span style="color: red;">━━</span> Poor (> 15 min)</p>
    <p style="font-size: 11px; margin-top: 10px;">Line thickness = volume</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save map
    m.save(output_file)
    print(f"Route flow map saved to {output_file}")
    
    return m


def create_traffic_heatmap(flights_df, airports_df, output_file='traffic_heatmap.html'):
    """
    Create a heatmap showing flight traffic density
    
    Parameters:
    -----------
    flights_df : DataFrame
        Processed flights data
    airports_df : DataFrame
        Airport data with coordinates
    output_file : str
        Output HTML file path
    
    Returns:
    --------
    folium.Map : The created map object
    """
    
    # Count departures by airport
    departures = flights_df.groupby('ORIGIN_AIRPORT').size().reset_index(name='count')
    departures = departures.merge(
        airports_df[['IATA_CODE', 'LATITUDE', 'LONGITUDE']], 
        left_on='ORIGIN_AIRPORT', 
        right_on='IATA_CODE',
        how='left'
    )
    # Remove airports without coordinates
    departures = departures.dropna(subset=['LATITUDE', 'LONGITUDE'])
    
    # Prepare data for heatmap (lat, lon, weight)
    heat_data = [
        [row['LATITUDE'], row['LONGITUDE'], row['count']] 
        for idx, row in departures.iterrows()
    ]
    
    # Create base map
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
    
    # Add heatmap layer
    HeatMap(
        heat_data,
        min_opacity=0.3,
        max_zoom=13,
        radius=25,
        blur=30,
        gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 0.8: 'orange', 1: 'red'}
    ).add_to(m)
    
    # Save map
    m.save(output_file)
    print(f"Traffic heatmap saved to {output_file}")
    
    return m


def create_all_maps(flights_df, airports_df, output_dir='maps/'):
    """
    Generate all geographic visualizations
    
    Parameters:
    -----------
    flights_df : DataFrame
        Processed flights data
    airports_df : DataFrame
        Airport data with coordinates
    output_dir : str
        Output directory for map files
    """
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating geographic visualizations...")
    print("-" * 50)
    
    # Generate all maps
    create_airport_delay_map(flights_df, airports_df, 
                            output_file=f'{output_dir}airport_delay_map.html')
    
    create_route_flow_map(flights_df, airports_df, 
                         top_n=50,
                         output_file=f'{output_dir}route_flow_map.html')
    
    create_traffic_heatmap(flights_df, airports_df, 
                          output_file=f'{output_dir}traffic_heatmap.html')
    
    print("-" * 50)
    print("All maps generated successfully!")
    print(f"Maps saved to: {output_dir}")


if __name__ == "__main__":
    # Example usage
    print("Loading data...")
    flights_df = pd.read_csv('dataset/final_processed_flights.csv', low_memory=False)
    airports_df = pd.read_csv('dataset/airports.csv')
    
    # Generate all maps
    create_all_maps(flights_df, airports_df)
    
    print("\nTo view maps, open the HTML files in a web browser.")
