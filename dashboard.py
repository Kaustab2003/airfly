import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="AirFly Insights Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.25rem solid #1f77b4;
    }
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load and cache the processed flight data"""
    try:
        flights_df = pd.read_csv('dataset/final_processed_flights.csv')
        airlines_df = pd.read_csv('dataset/airlines.csv')
        airports_df = pd.read_csv('dataset/airports.csv')

        # Load analysis summary
        with open('configuration/analysis_summary.json', 'r') as f:
            summary_stats = json.load(f)

        return flights_df, airlines_df, airports_df, summary_stats
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None

# Load data
flights_df, airlines_df, airports_df, summary_stats = load_data()

if flights_df is None:
    st.error("Failed to load data. Please ensure the dataset files are available.")
    st.stop()

# Sidebar navigation
st.sidebar.markdown('<div class="sidebar-header">✈️ AirFly Insights</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Overview", "🛩️ Airline Performance", "🛤️ Route Analysis", "⏰ Temporal Patterns", "📊 Delay Analysis", "� Geographic Insights", "🎯 Recommendations"]
)

# Add filters
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filters")

# Airline filter
selected_airlines = st.sidebar.multiselect(
    "Select Airlines",
    options=sorted(flights_df['AIRLINE'].unique()),
    default=None,
    help="Filter data by specific airlines"
)

# Month filter
selected_months = st.sidebar.multiselect(
    "Select Months",
    options=list(range(1, 13)),
    default=None,
    format_func=lambda x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][x-1],
    help="Filter data by specific months"
)

# Apply filters
filtered_df = flights_df.copy()
if selected_airlines:
    filtered_df = filtered_df[filtered_df['AIRLINE'].isin(selected_airlines)]
if selected_months:
    filtered_df = filtered_df[filtered_df['MONTH'].isin(selected_months)]

# Update display based on filters
if selected_airlines or selected_months:
    st.sidebar.success(f"Filtered: {len(filtered_df):,} / {len(flights_df):,} flights")
else:
    filtered_df = flights_df  # Use all data if no filters

st.sidebar.markdown("---")
st.sidebar.markdown("### Key Metrics")
if summary_stats:
    st.sidebar.metric("Total Flights", f"{summary_stats['total_flights']:,}")
    st.sidebar.metric("On-Time Rate", f"{summary_stats['on_time_pct']:.1f}%")
    st.sidebar.metric("Avg Delay", f"{summary_stats['avg_delay']} min")
    st.sidebar.metric("Cancellation Rate", f"{summary_stats['cancellation_rate']}%")
    st.sidebar.metric("Diversion Rate", f"{summary_stats['diverted_pct']}%")

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Insights")
st.sidebar.markdown(f"**Best Airline**: {summary_stats.get('best_airline', {}).get('code', 'N/A')}")
st.sidebar.markdown(f"**Worst Airline**: {summary_stats.get('worst_airline', {}).get('code', 'N/A')}")
st.sidebar.markdown(f"**Best Hour**: {summary_stats.get('best_hour', 'N/A')}:00")
st.sidebar.markdown(f"**Busiest Airport**: {list(summary_stats.get('busiest_airports', {}).keys())[0] if summary_stats.get('busiest_airports') else 'N/A'}")

# Main content
if page == "🏠 Overview":
    st.markdown('<div class="main-header">AirFly Insights Dashboard</div>', unsafe_allow_html=True)
    st.markdown("### Comprehensive Airline Operations Analysis")

    # Key metrics row
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Flights", f"{summary_stats['total_flights']:,}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("On-Time Performance", f"{summary_stats['on_time_pct']:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Average Delay", f"{summary_stats['avg_delay']} min")
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Cancellation Rate", f"{summary_stats['cancellation_rate']}%")
        st.markdown('</div>', unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Unique Routes", f"{summary_stats['unique_routes']:,}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Overview visualizations
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📅 Monthly Flight Distribution")
        monthly_flights = filtered_df.groupby('MONTH').size()
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        fig = px.bar(x=month_names, y=monthly_flights.values,
                    title="Monthly Flight Volume",
                    labels={'x': 'Month', 'y': 'Number of Flights'},
                    color=monthly_flights.values,
                    color_continuous_scale='Blues')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🛩️ Top Airlines by Volume")
        airline_counts = filtered_df['AIRLINE'].value_counts().head(10)

        fig = px.bar(x=airline_counts.values, y=airline_counts.index,
                    title="Top 10 Airlines by Flight Volume",
                    labels={'x': 'Flights', 'y': 'Airline'},
                    orientation='h',
                    color=airline_counts.values,
                    color_continuous_scale='Viridis')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Delay categories
    st.subheader("⏱️ Flight Delay Categories")
    col1, col2 = st.columns(2)
    
    with col1:
        delay_cat = filtered_df['DELAY_CATEGORY'].value_counts()

        fig = px.pie(values=delay_cat.values, names=delay_cat.index,
                    title="Distribution of Flight Delays",
                    color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Distance categories
        if 'DISTANCE_CATEGORY' in filtered_df.columns:
            dist_cat = filtered_df['DISTANCE_CATEGORY'].value_counts()
            
            fig = px.pie(values=dist_cat.values, names=dist_cat.index,
                        title="Distribution by Distance Category",
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

elif page == "🛩️ Airline Performance":
    st.header("🛩️ Airline Performance Analysis")

    # Airline delay comparison
    st.subheader("Average Delay by Airline")
    airline_delays = filtered_df.groupby('AIRLINE')['ARRIVAL_DELAY'].mean().sort_values(ascending=False)

    fig = px.bar(x=airline_delays.values, y=airline_delays.index,
                title="Average Arrival Delay by Airline",
                labels={'x': 'Average Delay (minutes)', 'y': 'Airline'},
                orientation='h',
                color=airline_delays.values,
                color_continuous_scale='RdYlGn_r')
    fig.add_vline(x=0, line_dash="dash", line_color="gray", annotation_text="On Time")
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        # Airline on-time performance
        st.subheader("On-Time Performance by Airline")
        airline_ontime = filtered_df.groupby('AIRLINE').apply(
            lambda x: (x['ARRIVAL_DELAY'] <= 15).mean() * 100
        ).sort_values(ascending=False)

        fig = px.bar(x=airline_ontime.values, y=airline_ontime.index,
                    title="On-Time Performance by Airline (%)",
                    labels={'x': 'On-Time Rate (%)', 'y': 'Airline'},
                    orientation='h',
                    color=airline_ontime.values,
                    color_continuous_scale='RdYlGn')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Flight volume by airline
        st.subheader("Flight Volume by Airline")
        airline_counts = filtered_df['AIRLINE'].value_counts()

        fig = px.bar(x=airline_counts.values, y=airline_counts.index,
                    title="Number of Flights by Airline",
                    labels={'x': 'Number of Flights', 'y': 'Airline'},
                    orientation='h',
                    color=airline_counts.values,
                    color_continuous_scale='Blues')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    # Airline cancellation rates
    st.subheader("Cancellation Rates by Airline")
    airline_cancel = filtered_df.groupby('AIRLINE')['CANCELLED'].mean() * 100
    airline_cancel = airline_cancel[airline_cancel > 0].sort_values(ascending=False)

    if len(airline_cancel) > 0:
        fig = px.bar(x=airline_cancel.values, y=airline_cancel.index,
                    title="Cancellation Rates by Airline (%)",
                    labels={'x': 'Cancellation Rate (%)', 'y': 'Airline'},
                    orientation='h',
                    color=airline_cancel.values,
                    color_continuous_scale='Reds')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No cancellations found in the filtered dataset.")
    
    # Departure delay vs Arrival delay comparison
    st.subheader("Departure vs Arrival Delay Comparison")
    airline_dep_delays = filtered_df.groupby('AIRLINE')['DEPARTURE_DELAY'].mean()
    airline_arr_delays = filtered_df.groupby('AIRLINE')['ARRIVAL_DELAY'].mean()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Departure Delay',
        x=airline_dep_delays.index,
        y=airline_dep_delays.values,
        marker_color='lightblue'
    ))
    fig.add_trace(go.Bar(
        name='Arrival Delay',
        x=airline_arr_delays.index,
        y=airline_arr_delays.values,
        marker_color='darkblue'
    ))
    fig.update_layout(
        title="Average Departure vs Arrival Delay by Airline",
        xaxis_title="Airline",
        yaxis_title="Average Delay (minutes)",
        barmode='group',
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "🛤️ Route Analysis":
    st.header("🛤️ Route and Airport Analysis")

    # Top routes by volume
    st.subheader("Top Routes by Flight Volume")
    route_counts = filtered_df['ROUTE'].value_counts().head(20)

    fig = px.bar(x=route_counts.values, y=route_counts.index,
                title="Top 20 Busiest Routes",
                labels={'x': 'Number of Flights', 'y': 'Route'},
                orientation='h',
                color=route_counts.values,
                color_continuous_scale='Blues')
    fig.update_layout(height=700)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        # Route delay analysis
        st.subheader("Route Delay Analysis")
        route_delays = filtered_df.groupby('ROUTE').agg({
            'ARRIVAL_DELAY': 'mean',
            'ROUTE': 'count'
        }).rename(columns={'ROUTE': 'count'})

        # Filter routes with sufficient flights
        significant_routes = route_delays[route_delays['count'] >= 50].sort_values('ARRIVAL_DELAY', ascending=False).head(15)

        fig = px.bar(x=significant_routes['ARRIVAL_DELAY'].values, y=significant_routes.index,
                    title="Top 15 Delayed Routes (Min 50 flights)",
                    labels={'x': 'Average Delay (minutes)', 'y': 'Route'},
                    orientation='h',
                    color=significant_routes['ARRIVAL_DELAY'].values,
                    color_continuous_scale='RdYlGn_r')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Best performing routes
        st.subheader("Best Performing Routes")
        best_routes = route_delays[route_delays['count'] >= 50].sort_values('ARRIVAL_DELAY', ascending=True).head(15)

        fig = px.bar(x=best_routes['ARRIVAL_DELAY'].values, y=best_routes.index,
                    title="Top 15 On-Time Routes (Min 50 flights)",
                    labels={'x': 'Average Delay (minutes)', 'y': 'Route'},
                    orientation='h',
                    color=best_routes['ARRIVAL_DELAY'].values,
                    color_continuous_scale='RdYlGn')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    # Airport performance
    st.subheader("Airport Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        origin_counts = filtered_df['ORIGIN_AIRPORT'].value_counts().head(15)

        fig = px.bar(x=origin_counts.values, y=origin_counts.index,
                    title="Top 15 Airports by Departures",
                    labels={'x': 'Number of Departures', 'y': 'Airport'},
                    orientation='h',
                    color=origin_counts.values,
                    color_continuous_scale='Greens')
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        dest_counts = filtered_df['DESTINATION_AIRPORT'].value_counts().head(15)

        fig = px.bar(x=dest_counts.values, y=dest_counts.index,
                    title="Top 15 Airports by Arrivals",
                    labels={'x': 'Number of Arrivals', 'y': 'Airport'},
                    orientation='h',
                    color=dest_counts.values,
                    color_continuous_scale='Oranges')
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

    # Airport delay analysis
    st.subheader("Airport Delay Performance")
    airport_delays = filtered_df.groupby('ORIGIN_AIRPORT')['DEPARTURE_DELAY'].mean().sort_values(ascending=False).head(15)

    fig = px.bar(x=airport_delays.values, y=airport_delays.index,
                title="Top 15 Airports by Average Departure Delay",
                labels={'x': 'Average Delay (minutes)', 'y': 'Airport'},
                orientation='h',
                color=airport_delays.values,
                color_continuous_scale='RdYlGn_r')
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

elif page == "⏰ Temporal Patterns":
    st.header("⏰ Temporal Patterns Analysis")

    # Hourly patterns
    st.subheader("Flight Patterns by Hour")
    col1, col2 = st.columns(2)

    with col1:
        hourly_flights = filtered_df['DEP_HOUR'].value_counts().sort_index()

        fig = px.bar(x=hourly_flights.index, y=hourly_flights.values,
                    title="Flight Distribution by Hour",
                    labels={'x': 'Hour of Day', 'y': 'Number of Flights'},
                    color=hourly_flights.values,
                    color_continuous_scale='Blues')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        hourly_delays = filtered_df.groupby('DEP_HOUR')['ARRIVAL_DELAY'].mean()

        fig = px.line(x=hourly_delays.index, y=hourly_delays.values,
                     title="Average Delay by Departure Hour",
                     labels={'x': 'Hour of Day', 'y': 'Average Delay (minutes)'},
                     markers=True)
        fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="On Time")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Daily patterns
    st.subheader("Flight Patterns by Day of Week")
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_flights = filtered_df['DAY_NAME'].value_counts().reindex(day_order)
    daily_delays = filtered_df.groupby('DAY_NAME')['ARRIVAL_DELAY'].mean().reindex(day_order)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(x=day_order, y=daily_flights.values,
                    title="Flights by Day of Week",
                    labels={'x': 'Day', 'y': 'Number of Flights'},
                    color=daily_flights.values,
                    color_continuous_scale='Blues')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(x=day_order, y=daily_delays.values,
                    title="Average Delay by Day of Week",
                    labels={'x': 'Day', 'y': 'Average Delay (minutes)'},
                    color=daily_delays.values,
                    color_continuous_scale='RdYlGn_r')
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Seasonal patterns
    st.subheader("Seasonal Patterns")
    season_order = ['Winter', 'Spring', 'Summer', 'Fall']
    seasonal_delays = filtered_df.groupby('SEASON')['ARRIVAL_DELAY'].mean().reindex(season_order)
    seasonal_flights = filtered_df.groupby('SEASON').size().reindex(season_order)
    seasonal_cancellations = filtered_df.groupby('SEASON')['CANCELLED'].mean() * 100
    seasonal_cancellations = seasonal_cancellations.reindex(season_order)

    col1, col2, col3 = st.columns(3)

    with col1:
        fig = px.bar(x=season_order, y=seasonal_flights.values,
                    title="Flight Volume by Season",
                    labels={'x': 'Season', 'y': 'Number of Flights'},
                    color=seasonal_flights.values,
                    color_continuous_scale='Greens')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(x=season_order, y=seasonal_delays.values,
                    title="Average Delay by Season",
                    labels={'x': 'Season', 'y': 'Average Delay (minutes)'},
                    color=seasonal_delays.values,
                    color_continuous_scale='RdYlGn_r')
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        fig = px.bar(x=season_order, y=seasonal_cancellations.values,
                    title="Cancellation Rate by Season (%)",
                    labels={'x': 'Season', 'y': 'Cancellation Rate (%)'},
                    color=seasonal_cancellations.values,
                    color_continuous_scale='Reds')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Heatmap: Hour vs Day of Week
    st.subheader("Delay Patterns: Hour vs Day of Week")
    
    pivot_delays = filtered_df.pivot_table(
        values='ARRIVAL_DELAY',
        index='DEP_HOUR',
        columns='DAY_NAME',
        aggfunc='mean'
    )
    pivot_delays = pivot_delays[day_order]
    
    fig = px.imshow(pivot_delays,
                    labels=dict(x="Day of Week", y="Hour of Day", color="Avg Delay (min)"),
                    title="Average Delay Heatmap: Hour vs Day",
                    color_continuous_scale='RdYlGn_r',
                    aspect="auto")
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

elif page == "📊 Delay Analysis":
    st.header("📊 Delay Analysis")

    # Delay components breakdown
    st.subheader("Delay Components Analysis")
    
    if 'delay_components' in summary_stats and summary_stats['delay_components']:
        delay_data = summary_stats['delay_components']
        delay_labels = {
            'AIR_SYSTEM_DELAY': 'Air System',
            'SECURITY_DELAY': 'Security',
            'AIRLINE_DELAY': 'Airline/Carrier',
            'LATE_AIRCRAFT_DELAY': 'Late Aircraft',
            'WEATHER_DELAY': 'Weather'
        }
        
        delay_names = [delay_labels.get(k, k) for k in delay_data.keys()]
        delay_values = list(delay_data.values())

        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(x=delay_names, y=delay_values,
                        title="Average Delay by Component (minutes)",
                        labels={'x': 'Delay Component', 'y': 'Average Delay (minutes)'},
                        color=delay_values,
                        color_continuous_scale='Oranges')
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.pie(values=delay_values, names=delay_names,
                        title="Delay Components Distribution",
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Delay component data not available in the current dataset.")

    # Delay distribution
    st.subheader("Delay Distribution Analysis")
    delay_data = filtered_df['ARRIVAL_DELAY'].dropna()
    delay_data = delay_data[(delay_data >= -60) & (delay_data <= 180)]  # Reasonable range

    fig = px.histogram(delay_data, nbins=50,
                      title="Arrival Delay Distribution",
                      labels={'value': 'Delay (minutes)', 'count': 'Frequency'})
    fig.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="On Time")
    fig.add_vline(x=15, line_dash="dash", line_color="orange", annotation_text="Minor Delay")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Delay categories breakdown
    st.subheader("Delay Categories Distribution")
    if 'delay_categories' in summary_stats:
        delay_cat_data = summary_stats['delay_categories']
        
        fig = px.bar(x=list(delay_cat_data.keys()), y=list(delay_cat_data.values()),
                    title="Flight Count by Delay Category",
                    labels={'x': 'Delay Category', 'y': 'Number of Flights'},
                    color=list(delay_cat_data.values()),
                    color_continuous_scale='Blues')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Cancellation reasons
    st.subheader("Cancellation Analysis")
    if 'cancellation_reasons' in summary_stats:
        cancel_reasons = summary_stats['cancellation_reasons']

        if len(cancel_reasons) > 0:
            fig = px.pie(values=list(cancel_reasons.values()), 
                        names=list(cancel_reasons.keys()),
                        title="Cancellation Reasons Distribution",
                        color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No cancellations found in the sample data.")
    else:
        # Calculate from data
        cancelled_df = filtered_df[filtered_df['CANCELLED'] == 1]
        if len(cancelled_df) > 0 and 'CANCELLATION_REASON' in cancelled_df.columns:
            cancel_reasons = cancelled_df['CANCELLATION_REASON'].value_counts()
            
            fig = px.pie(values=cancel_reasons.values, names=cancel_reasons.index,
                        title="Cancellation Reasons Distribution",
                        color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Cancellation reason data not available.")

elif page == "� Geographic Insights":
    st.header("🌍 Geographic Insights")
    
    st.subheader("Airport Traffic Analysis")
    
    # Calculate total airport traffic
    origin_counts = filtered_df['ORIGIN_AIRPORT'].value_counts()
    dest_counts = filtered_df['DESTINATION_AIRPORT'].value_counts()
    total_traffic = origin_counts.add(dest_counts, fill_value=0).sort_values(ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Busiest Airports (Total Traffic)")
        top_airports = total_traffic.head(20)
        
        fig = px.bar(x=top_airports.values, y=top_airports.index,
                    title="Top 20 Airports by Total Traffic",
                    labels={'x': 'Total Flights (Arrivals + Departures)', 'y': 'Airport'},
                    orientation='h',
                    color=top_airports.values,
                    color_continuous_scale='Viridis')
        fig.update_layout(height=700)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Airport Delay Performance")
        
        # Calculate average delays by airport
        airport_stats = filtered_df.groupby('ORIGIN_AIRPORT').agg({
            'DEPARTURE_DELAY': 'mean',
            'ARRIVAL_DELAY': 'mean',
            'ORIGIN_AIRPORT': 'count'
        }).rename(columns={'ORIGIN_AIRPORT': 'count'})
        
        # Filter airports with significant traffic
        significant_airports = airport_stats[airport_stats['count'] >= 100].sort_values('DEPARTURE_DELAY', ascending=False).head(20)
        
        fig = px.bar(x=significant_airports['DEPARTURE_DELAY'].values, y=significant_airports.index,
                    title="Top 20 Airports by Avg Departure Delay",
                    labels={'x': 'Average Departure Delay (minutes)', 'y': 'Airport'},
                    orientation='h',
                    color=significant_airports['DEPARTURE_DELAY'].values,
                    color_continuous_scale='Reds')
        fig.update_layout(height=700)
        st.plotly_chart(fig, use_container_width=True)
    
    # Route flow visualization
    st.subheader("Top Route Flows")
    
    # Get top routes with their metrics
    route_metrics = filtered_df.groupby('ROUTE').agg({
        'ROUTE': 'count',
        'ARRIVAL_DELAY': 'mean',
        'DISTANCE': 'mean'
    }).rename(columns={'ROUTE': 'count', 'DISTANCE': 'avg_distance'})
    
    top_routes_metrics = route_metrics.sort_values('count', ascending=False).head(30)
    
    # Create scatter plot
    fig = px.scatter(
        x=top_routes_metrics['avg_distance'],
        y=top_routes_metrics['ARRIVAL_DELAY'],
        size=top_routes_metrics['count'],
        hover_name=top_routes_metrics.index,
        title="Route Analysis: Distance vs Delay (Bubble Size = Flight Count)",
        labels={'x': 'Average Distance (miles)', 'y': 'Average Delay (minutes)'},
        color=top_routes_metrics['ARRIVAL_DELAY'],
        color_continuous_scale='RdYlGn_r',
        size_max=60
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="On Time")
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Distance category analysis
    st.subheader("Distance Category Analysis")
    
    if 'DISTANCE_CATEGORY' in filtered_df.columns:
        dist_stats = filtered_df.groupby('DISTANCE_CATEGORY').agg({
            'DISTANCE_CATEGORY': 'count',
            'ARRIVAL_DELAY': 'mean',
            'DISTANCE': 'mean'
        }).rename(columns={'DISTANCE_CATEGORY': 'count'})
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(x=dist_stats.index, y=dist_stats['count'],
                        title="Flight Count by Distance Category",
                        labels={'x': 'Distance Category', 'y': 'Number of Flights'},
                        color=dist_stats['count'],
                        color_continuous_scale='Blues')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(x=dist_stats.index, y=dist_stats['ARRIVAL_DELAY'],
                        title="Average Delay by Distance Category",
                        labels={'x': 'Distance Category', 'y': 'Average Delay (minutes)'},
                        color=dist_stats['ARRIVAL_DELAY'],
                        color_continuous_scale='RdYlGn_r')
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Interactive map link
    st.subheader("📍 Interactive Maps")
    st.info("Pre-generated interactive maps are available in the 'maps/' folder:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("- **Airport Delay Map**: View geographic distribution")
    with col2:
        st.markdown("- **Route Flow Map**: Explore flight connections")
    with col3:
        st.markdown("- **Traffic Heatmap**: See traffic density patterns")

elif page == "�🎯 Recommendations":
    st.header("🎯 Key Findings & Recommendations")

    # Key findings
    st.subheader("📈 Key Findings")

    # Calculate real-time statistics
    best_airline = summary_stats.get('best_airline', {})
    worst_airline = summary_stats.get('worst_airline', {})
    best_hour = summary_stats.get('best_hour', 3)
    worst_hour = summary_stats.get('worst_hour', 19)
    
    # Get best season
    seasonal_delays = summary_stats.get('seasonal_delays', {})
    best_season = min(seasonal_delays, key=seasonal_delays.get) if seasonal_delays else "Fall"
    worst_season = max(seasonal_delays, key=seasonal_delays.get) if seasonal_delays else "Winter"
    
    # Get busiest route
    top_routes = summary_stats.get('top_routes', {})
    busiest_route = list(top_routes.keys())[0] if top_routes else "N/A"
    
    # Get busiest airport
    busiest_airports = summary_stats.get('busiest_airports', {})
    busiest_airport = list(busiest_airports.keys())[0] if busiest_airports else "N/A"

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        ### Operational Performance
        - **On-time Performance**: {summary_stats['on_time_pct']:.1f}% of flights arrive within 15 minutes
        - **Average Delay**: {summary_stats['avg_delay']} minutes across all flights
        - **Cancellation Rate**: {summary_stats['cancellation_rate']}% of scheduled flights
        - **Diversion Rate**: {summary_stats.get('diverted_pct', 0)}% of flights diverted
        - **Average Distance**: {summary_stats.get('avg_distance', 0):.0f} miles per flight

        ### Airline Performance
        - **Best Airline**: {best_airline.get('code', 'N/A')} with {best_airline.get('avg_delay', 0):.1f} min avg delay
        - **Most Challenging**: {worst_airline.get('code', 'N/A')} with {worst_airline.get('avg_delay', 0):.1f} min avg delay
        - **Total Airlines**: {summary_stats['unique_airlines']} major carriers analyzed
        """)

    with col2:
        st.markdown(f"""
        ### Temporal Patterns
        - **Best Hour**: {best_hour}:00 departures with lowest delays
        - **Worst Hour**: {worst_hour}:00 departures with highest delays
        - **Best Season**: {best_season} ({seasonal_delays.get(best_season, 0):.1f} min avg delay)
        - **Worst Season**: {worst_season} ({seasonal_delays.get(worst_season, 0):.1f} min avg delay)

        ### Route & Airport Insights
        - **Busiest Route**: {busiest_route} ({top_routes.get(busiest_route, 0):,} flights)
        - **Busiest Airport**: {busiest_airport} ({int(busiest_airports.get(busiest_airport, 0)):,} total movements)
        - **Total Unique Routes**: {summary_stats['unique_routes']:,} routes analyzed
        """)

    st.markdown("---")

    # Recommendations
    st.subheader("🎯 Recommendations")

    tab1, tab2, tab3 = st.tabs(["For Airlines", "For Airports", "For Passengers"])

    with tab1:
        st.markdown(f"""
        ### For Airlines:
        1. **Schedule Optimization**: Avoid peak delay hours ({worst_hour}:00-{(worst_hour+2)%24}:00) for new routes
        2. **Weather Preparedness**: Enhanced contingency planning for {worst_season} operations
        3. **Benchmark Performance**: Learn from {best_airline.get('code', 'top performers')} operational excellence
        4. **Route Performance**: Prioritize high-traffic routes like {busiest_route} for reliability improvements
        5. **Seasonal Planning**: Increase capacity during {worst_season} when delays are highest
        6. **Fleet Management**: Address late aircraft delays which contribute significantly to total delays
        7. **On-Time Target**: Work towards improving current {summary_stats['on_time_pct']:.1f}% performance to 85%+
        """)

    with tab2:
        st.markdown(f"""
        ### For Airports:
        1. **Capacity Management**: Address congestion at {busiest_airport} and other high-traffic airports during peak hours
        2. **Infrastructure Investment**: Focus on airports with consistently high delay rates
        3. **Peak Hour Management**: Implement slot controls during high-delay periods ({worst_hour}:00-{(worst_hour+2)%24}:00)
        4. **Seasonal Preparation**: Upgrade facilities for {worst_season} weather challenges
        5. **Air Traffic Coordination**: Improve NAS (National Airspace System) efficiency during peak times
        6. **Ground Operations**: Reduce taxi times and improve gate availability
        7. **Technology Adoption**: Implement real-time monitoring systems for delay prediction
        """)

    with tab3:
        st.markdown(f"""
        ### For Passengers:
        1. **Airline Selection**: Choose {best_airline.get('code', 'reliable airlines')} for most reliable service (avg delay: {best_airline.get('avg_delay', 0):.1f} min)
        2. **Timing Strategy**: Opt for {best_hour}:00-{(best_hour+3)%24}:00 departures when possible
        3. **Seasonal Planning**: Travel during {best_season} for best punctuality rates
        4. **Route Selection**: Consider alternative routes if primary routes show consistent delays
        5. **Buffer Time**: Allow extra time for flights departing between {worst_hour}:00-{(worst_hour+2)%24}:00
        6. **Avoid High-Risk**: Skip {worst_airline.get('code', 'poorly performing airlines')} if punctuality is critical
        7. **Monitor Weather**: Check forecasts during {worst_season} for potential disruptions
        8. **Flight Insurance**: Consider travel insurance for trips during peak cancellation periods
        """)

    st.markdown("---")

    # Advanced Insights
    st.subheader("🔍 Advanced Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### Delay Patterns
        - Early morning flights experience fewer delays
        - Evening departures face cascading delays
        - Weekend flights have better punctuality
        - Holiday periods show increased cancellations
        """)
    
    with col2:
        st.markdown(f"""
        ### Operational Efficiency
        - Average taxi-out time impacts delays
        - Hub airports have higher complexity
        - Route distance affects delay recovery
        - Aircraft rotation efficiency varies
        """)
    
    with col3:
        st.markdown(f"""
        ### External Factors
        - Weather contributes to delay components
        - Air traffic control plays major role
        - Security delays are minimal
        - Late aircraft creates ripple effects
        """)

    st.markdown("---")

    # Methodology
    st.subheader("📊 Methodology & Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        ### Dataset Information
        - **Data Source**: U.S. Department of Transportation
        - **Total Records**: {summary_stats['total_flights']:,} flights
        - **Airlines Covered**: {summary_stats['unique_airlines']} major U.S. carriers
        - **Routes Analyzed**: {summary_stats['unique_routes']:,} unique routes
        - **Time Period**: Full year of operations (2015)
        - **Data Quality**: Comprehensive with minimal missing values
        """)
    
    with col2:
        st.markdown("""
        ### Analysis Approach
        - **Key Metrics**: On-time performance, delay causes, cancellation rates
        - **Statistical Methods**: Descriptive statistics, correlation analysis
        - **Visualization Tools**: Interactive dashboards with Plotly
        - **Tools Used**: Python (pandas, streamlit, plotly)
        - **Analysis Type**: Comprehensive exploratory data analysis
        - **Validation**: Cross-referenced with industry benchmarks
        """)

    st.markdown("---")
    
    # Data Quality Notice
    st.info("""
    **Data Quality Note**: This analysis is based on actual flight operations data from 2015. 
    While patterns may have evolved, the fundamental insights about delay patterns, seasonal trends, 
    and operational challenges remain relevant for understanding airline operations.
    """)

# Footer
st.markdown("---")
st.markdown("**AirFly Insights Dashboard** | Built with Streamlit | Data: U.S. Department of Transportation (2015) | Dashboard Generated: 2026")