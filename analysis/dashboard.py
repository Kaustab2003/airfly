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
        with open('analysis_summary.json', 'r') as f:
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
    ["🏠 Overview", "🛩️ Airline Performance", "🛤️ Route Analysis", "⏰ Temporal Patterns", "📊 Delay Analysis", "🎯 Recommendations"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Key Metrics")
if summary_stats:
    st.sidebar.metric("Total Flights", f"{summary_stats['total_flights']:,}")
    st.sidebar.metric("On-Time Rate", f"{summary_stats['on_time_pct']:.1f}%")
    st.sidebar.metric("Avg Delay", f"{summary_stats['avg_delay']} min")

# Main content
if page == "🏠 Overview":
    st.markdown('<div class="main-header">AirFly Insights Dashboard</div>', unsafe_allow_html=True)
    st.markdown("### Comprehensive Airline Operations Analysis")

    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)

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
        st.metric("Cancellation Rate", f"{summary_stats['cancellation_rate']:.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Overview visualizations
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📅 Monthly Flight Distribution")
        monthly_flights = flights_df.groupby('MONTH').size()
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        fig = px.bar(x=month_names, y=monthly_flights.values,
                    title="Monthly Flight Volume",
                    labels={'x': 'Month', 'y': 'Number of Flights'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🛩️ Top Airlines by Volume")
        airline_counts = flights_df['AIRLINE'].value_counts().head(10)

        fig = px.bar(x=airline_counts.values, y=airline_counts.index,
                    title="Top 10 Airlines by Flight Volume",
                    labels={'x': 'Flights', 'y': 'Airline'},
                    orientation='h')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Delay categories
    st.subheader("⏱️ Flight Delay Categories")
    delay_cat = flights_df['DELAY_CATEGORY'].value_counts()

    fig = px.pie(values=delay_cat.values, names=delay_cat.index,
                title="Distribution of Flight Delays",
                color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

elif page == "🛩️ Airline Performance":
    st.header("🛩️ Airline Performance Analysis")

    # Airline delay comparison
    st.subheader("Average Delay by Airline")
    airline_delays = flights_df.groupby('AIRLINE')['ARRIVAL_DELAY'].mean().sort_values(ascending=False)

    fig = px.bar(x=airline_delays.values, y=airline_delays.index,
                title="Average Arrival Delay by Airline",
                labels={'x': 'Average Delay (minutes)', 'y': 'Airline'},
                orientation='h',
                color=airline_delays.values,
                color_continuous_scale='RdYlGn_r')
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

    # Airline on-time performance
    st.subheader("On-Time Performance by Airline")
    airline_ontime = flights_df.groupby('AIRLINE').apply(
        lambda x: (x['ARRIVAL_DELAY'] <= 15).mean() * 100
    ).sort_values(ascending=False)

    fig = px.bar(x=airline_ontime.values, y=airline_ontime.index,
                title="On-Time Performance by Airline (%)",
                labels={'x': 'On-Time Rate (%)', 'y': 'Airline'},
                orientation='h',
                color=airline_ontime.values,
                color_continuous_scale='RdYlGn')
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

    # Airline cancellation rates
    st.subheader("Cancellation Rates by Airline")
    airline_cancel = flights_df.groupby('AIRLINE')['CANCELLED'].mean() * 100
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
        st.info("No cancellations found in the dataset.")

elif page == "🛤️ Route Analysis":
    st.header("🛤️ Route and Airport Analysis")

    # Top routes by volume
    st.subheader("Top Routes by Flight Volume")
    route_counts = flights_df['ROUTE'].value_counts().head(15)

    fig = px.bar(x=route_counts.values, y=route_counts.index,
                title="Top 15 Busiest Routes",
                labels={'x': 'Number of Flights', 'y': 'Route'},
                orientation='h',
                color=route_counts.values,
                color_continuous_scale='Blues')
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

    # Route delay analysis
    st.subheader("Route Delay Analysis")
    route_delays = flights_df.groupby('ROUTE').agg({
        'ARRIVAL_DELAY': 'mean',
        'ROUTE': 'count'
    }).rename(columns={'ROUTE': 'count'})

    # Filter routes with sufficient flights
    significant_routes = route_delays[route_delays['count'] >= 50].sort_values('ARRIVAL_DELAY', ascending=False).head(15)

    fig = px.bar(x=significant_routes['ARRIVAL_DELAY'].values, y=significant_routes.index,
                title="Top 15 Routes by Average Delay (Min 50 flights)",
                labels={'x': 'Average Delay (minutes)', 'y': 'Route'},
                orientation='h',
                color=significant_routes['ARRIVAL_DELAY'].values,
                color_continuous_scale='RdYlGn_r')
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

    # Airport performance
    st.subheader("Airport Performance Analysis")
    origin_counts = flights_df['ORIGIN_AIRPORT'].value_counts()
    dest_counts = flights_df['DESTINATION_AIRPORT'].value_counts()
    total_airport_traffic = origin_counts.add(dest_counts, fill_value=0).sort_values(ascending=False).head(15)

    airport_delays = flights_df.groupby('ORIGIN_AIRPORT')['ARRIVAL_DELAY'].mean()
    top_airport_delays = airport_delays.loc[total_airport_traffic.index]

    fig = px.bar(x=top_airport_delays.values, y=top_airport_delays.index,
                title="Average Departure Delay by Top 15 Airports",
                labels={'x': 'Average Delay (minutes)', 'y': 'Airport'},
                orientation='h',
                color=top_airport_delays.values,
                color_continuous_scale='RdYlGn_r')
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

elif page == "⏰ Temporal Patterns":
    st.header("⏰ Temporal Patterns Analysis")

    # Hourly patterns
    st.subheader("Flight Patterns by Hour")
    col1, col2 = st.columns(2)

    with col1:
        hourly_flights = flights_df['DEP_HOUR'].value_counts().sort_index()

        fig = px.bar(x=hourly_flights.index, y=hourly_flights.values,
                    title="Flight Distribution by Hour",
                    labels={'x': 'Hour of Day', 'y': 'Number of Flights'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        hourly_delays = flights_df.groupby('DEP_HOUR')['ARRIVAL_DELAY'].mean()

        fig = px.line(x=hourly_delays.index, y=hourly_delays.values,
                     title="Average Delay by Departure Hour",
                     labels={'x': 'Hour of Day', 'y': 'Average Delay (minutes)'},
                     markers=True)
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Daily patterns
    st.subheader("Flight Patterns by Day of Week")
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_flights = flights_df['DAY_NAME'].value_counts().reindex(day_order)
    daily_delays = flights_df.groupby('DAY_NAME')['ARRIVAL_DELAY'].mean().reindex(day_order)

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
    seasonal_delays = flights_df.groupby('SEASON')['ARRIVAL_DELAY'].mean()
    season_order = ['Winter', 'Spring', 'Summer', 'Fall']
    seasonal_delays = seasonal_delays.reindex(season_order)

    seasonal_cancellations = flights_df.groupby('SEASON')['CANCELLED'].mean() * 100
    seasonal_cancellations = seasonal_cancellations.reindex(season_order)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(x=season_order, y=seasonal_delays.values,
                    title="Average Delay by Season",
                    labels={'x': 'Season', 'y': 'Average Delay (minutes)'},
                    color=seasonal_delays.values,
                    color_continuous_scale='RdYlGn_r')
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(x=season_order, y=seasonal_cancellations.values,
                    title="Cancellation Rate by Season (%)",
                    labels={'x': 'Season', 'y': 'Cancellation Rate (%)'},
                    color=seasonal_cancellations.values,
                    color_continuous_scale='Reds')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

elif page == "📊 Delay Analysis":
    st.header("📊 Delay Analysis")

    # Delay components breakdown
    st.subheader("Delay Components Analysis")
    delay_components = ['CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY']
    existing_components = [col for col in delay_components if col in flights_df.columns]

    if existing_components:
        delay_means = flights_df[existing_components].mean()

        fig = px.bar(x=delay_means.index, y=delay_means.values,
                    title="Average Delay by Component (minutes)",
                    labels={'x': 'Delay Component', 'y': 'Average Delay (minutes)'},
                    color=delay_means.values,
                    color_continuous_scale='Oranges')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Pie chart of delay components
        fig = px.pie(values=delay_means.values, names=delay_means.index,
                    title="Delay Components Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Delay component data not available in the current dataset.")

    # Delay distribution
    st.subheader("Delay Distribution Analysis")
    delay_data = flights_df['ARRIVAL_DELAY'].dropna()
    delay_data = delay_data[(delay_data >= -60) & (delay_data <= 180)]  # Reasonable range

    fig = px.histogram(delay_data, nbins=50,
                      title="Arrival Delay Distribution",
                      labels={'value': 'Delay (minutes)', 'count': 'Frequency'})
    fig.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="On Time")
    fig.add_vline(x=15, line_dash="dash", line_color="orange", annotation_text="Minor Delay")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Cancellation reasons
    st.subheader("Cancellation Analysis")
    if 'CANCELLATION_REASON' in flights_df.columns:
        cancel_reasons = flights_df[flights_df['CANCELLED'] == 1]['CANCELLATION_REASON'].value_counts()

        if len(cancel_reasons) > 0:
            fig = px.pie(values=cancel_reasons.values, names=cancel_reasons.index,
                        title="Cancellation Reasons Distribution",
                        color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No cancellations found in the sample data.")
    else:
        st.info("Cancellation reason data not available.")

elif page == "🎯 Recommendations":
    st.header("🎯 Key Findings & Recommendations")

    # Key findings
    st.subheader("📈 Key Findings")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### Operational Performance
        - **On-time Performance**: 82.3% of flights arrive within 15 minutes
        - **Average Delay**: 4.34 minutes across all flights
        - **Cancellation Rate**: 1.55% of scheduled flights

        ### Airline Performance
        - **Best Airline**: Alaska Airlines (AS) with -1.1 min avg delay
        - **Most Challenging**: Frontier (F9) with 13.1 min avg delay
        """)

    with col2:
        st.markdown("""
        ### Temporal Patterns
        - **Best Hour**: 3:00 AM departures (-9.1 min avg delay)
        - **Worst Hour**: 7:00 PM departures (9.6 min avg delay)
        - **Best Season**: Fall (0.0 min avg delay)

        ### Route Insights
        - **Busiest Route**: LAX-SFO
        - **Route Analysis**: 6,980 unique routes analyzed
        """)

    st.markdown("---")

    # Recommendations
    st.subheader("🎯 Recommendations")

    tab1, tab2, tab3 = st.tabs(["For Airlines", "For Airports", "For Passengers"])

    with tab1:
        st.markdown("""
        ### For Airlines:
        1. **Schedule Optimization**: Avoid peak delay hours (19:00-21:00) for new routes
        2. **Weather Preparedness**: Enhanced contingency planning for winter operations
        3. **Carrier Delay Reduction**: Focus on turnaround times and crew scheduling
        4. **Route Performance**: Prioritize high-traffic routes like LAX-SFO for reliability improvements
        5. **Seasonal Planning**: Increase capacity during summer months when delays are highest
        """)

    with tab2:
        st.markdown("""
        ### For Airports:
        1. **Capacity Management**: Address congestion at high-traffic airports during peak hours
        2. **NAS Coordination**: Improve air traffic management systems, especially during delays
        3. **Weather Response**: Better ground delay programs during adverse weather conditions
        4. **Peak Hour Management**: Implement slot controls during high-delay periods (19:00-21:00)
        5. **Infrastructure Investment**: Upgrade facilities at consistently delay-prone airports
        """)

    with tab3:
        st.markdown("""
        ### For Passengers:
        1. **Airline Selection**: Choose Alaska Airlines (AS) for most reliable service
        2. **Timing Strategy**: Opt for early morning departures (3:00-6:00) when possible
        3. **Seasonal Planning**: Travel during Fall for best punctuality rates
        4. **Route Selection**: Consider alternative routes if primary routes show consistent delays
        5. **Buffer Time**: Allow extra time for flights departing between 19:00-21:00
        """)

    st.markdown("---")

    # Methodology
    st.subheader("📊 Methodology")
    st.markdown("""
    - **Data Source**: Kaggle Airlines Flights Dataset (2015)
    - **Analysis Period**: January 1, 2015 - December 31, 2015
    - **Sample Size**: 100,000 flights analyzed (optimized from 5.8M+ records)
    - **Key Metrics**: On-time performance, delay causes, cancellation rates, route efficiency
    - **Tools Used**: Python (pandas, matplotlib, seaborn, plotly, streamlit)
    - **Analysis Type**: Comprehensive exploratory data analysis with statistical insights
    """)

# Footer
st.markdown("---")
st.markdown("**AirFly Insights Dashboard** | Built with Streamlit | Data: Kaggle Airlines Dataset | Generated: December 18, 2025")