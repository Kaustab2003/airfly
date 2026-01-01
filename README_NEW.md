# AirFly Insights - Comprehensive Flight Delay Analysis

A comprehensive flight delay analysis project featuring interactive dashboards, detailed visualizations, and data-driven insights built with Python, Streamlit, and Jupyter notebooks.

## 🚀 Project Overview

AirFly Insights is a data science project that analyzes over **5.8 million flight records** from the U.S. aviation industry. The project combines exploratory data analysis, feature engineering, and interactive visualizations to understand flight delay patterns, airline performance, and operational insights.

## 📊 Key Features

- **Comprehensive Data Analysis**: Analysis of 5,819,079 flight records with 40 features
- **Interactive Dashboard**: Streamlit-powered web application with real-time filtering and 7 interactive pages
- **Advanced Visualizations**: 50+ visualizations including heatmaps, route maps, and temporal patterns
- **Feature Engineering**: Custom features including delay categories, seasons, routes, time-based metrics, and distance categories
- **Geographic Analysis**: Interactive airport traffic analysis and route flow visualization
- **Statistical Insights**: Correlation analysis, distribution analysis, delay component breakdown, and trend detection
- **Smart Filtering**: Filter by airlines and months to customize analysis

## 📈 Dataset Statistics

- **Total Flights**: 5,819,079 records
- **On-Time Performance**: 82.41% of flights arrive within 15 minutes
- **Average Delay**: 4.33 minutes
- **Cancellation Rate**: 1.54%
- **Diversion Rate**: 0.26%
- **Airlines Covered**: 14 major U.S. carriers
- **Unique Routes**: 8,609 routes analyzed
- **Airports**: 300+ origin and destination airports
- **Time Period**: Full year of operations (2015)
- **Features**: 40 columns including delays, cancellations, diversions, and engineered features

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip package manager
- 4GB+ RAM (for processing large datasets)
- Virtual environment (recommended)

### Installation Steps

1. **Navigate to the project directory**
   ```bash
   cd airfly
   ```

2. **Create and activate a virtual environment (recommended)**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # Linux/Mac
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify dataset files**
   The following files should be in the `dataset/` folder:
   - `final_processed_flights.csv` (1.2GB, 5.8M records with engineered features)
   - `flights.csv` (main raw dataset - 565MB, 5.8M records)
   - `airlines.csv` (airline information)
   - `airports.csv` (airport information)
   - `Airline_Delay_Cause.csv` (aggregated delay causes)
   - `global_holidays.csv`, `GlobalWeatherRepository.csv`, etc.

## 🎯 Running the Project

### Option 1: Interactive Dashboard (Recommended)

1. **Run the Streamlit dashboard**
   ```bash
   streamlit run dashboard.py
   ```

2. **Access the dashboard**
   - Open your browser to: `http://localhost:8501`
   - Explore 7 interactive pages:
     - 🏠 **Overview**: Key metrics and summary statistics
     - 🛩️ **Airline Performance**: Carrier-wise analysis and rankings
     - 🛤️ **Route Analysis**: Route performance and airport insights
     - ⏰ **Temporal Patterns**: Time-based patterns and heatmaps
     - 📊 **Delay Analysis**: Detailed delay component breakdown
     - 🌍 **Geographic Insights**: Airport traffic and route flow analysis
     - 🎯 **Recommendations**: Data-driven insights and actionable recommendations

3. **Use Interactive Filters**
   - Select specific airlines to compare
   - Filter by months to analyze seasonal patterns
   - View real-time updates based on your selections

### Option 2: Jupyter Notebook Analysis

1. **Open the comprehensive analysis notebook**
   ```bash
   jupyter notebook analysis/AirFly_Insights_Comprehensive.ipynb
   ```

2. **Run cells sequentially** to perform:
   - Data loading and exploration
   - Data quality assessment
   - Feature engineering and preprocessing
   - Comprehensive visualizations
   - Statistical analysis and insights

### Option 3: Generate Statistics

Run the statistics generator to update analysis summary:
```bash
python generate_stats.py
```

This will create/update `configuration/analysis_summary.json` with comprehensive statistics.

## 📁 Project Structure

```
airfly/
├── README.md                                    # Project overview and documentation
├── dashboard.py                                 # Streamlit interactive dashboard (main app)
├── generate_stats.py                            # Statistics generator script
├── create_presentation.py                       # Presentation generator
├── analysis_summary.json                        # Quick access to summary stats
├── requirements.txt                             # Python dependencies
├── analysis/
│   ├── AirFly_Insights_Comprehensive.ipynb     # Main analysis notebook
│   └── geographic_analysis.py                  # Geographic visualization utilities
├── dataset/
│   ├── final_processed_flights.csv             # Processed data (1.2GB, 5.8M records, 40 features)
│   ├── flights.csv                             # Raw dataset (565MB, 5.8M records)
│   ├── flights_processed.csv                   # Intermediate processed file
│   ├── airlines.csv                            # Airline reference data
│   ├── airports.csv                            # Airport reference data
│   ├── Airline_Delay_Cause.csv                 # Aggregated delay causes
│   ├── airlines_flights_data.csv               # Combined airline-flight data
│   ├── monthly_passengers.csv                  # Monthly passenger statistics
│   ├── global_holidays.csv                     # Holiday calendar data
│   └── GlobalWeatherRepository.csv             # Weather data
├── maps/
│   ├── airport_delay_map.html                  # Interactive airport delay map
│   ├── route_flow_map.html                     # Flight route visualization
│   └── traffic_heatmap.html                    # Traffic density heatmap
├── configuration/
│   ├── analysis_summary.json                   # Comprehensive analysis statistics
│   └── markdown_to_pdf.py                      # Documentation utilities
├── documentation/                               # Project documentation (if available)
└── testing/
    ├── test_dashboard.py                       # Dashboard unit tests
    └── test_suite.py                           # Comprehensive test suite
```

## 🎨 Dashboard Features

### 📊 Interactive Pages

#### 1. 🏠 Overview
- **Key Performance Indicators**: Total flights, on-time %, avg delay, cancellation rate, unique routes
- **Monthly Flight Distribution**: Bar chart showing flight volume by month
- **Top Airlines by Volume**: Horizontal bar chart of busiest carriers
- **Delay Categories**: Pie chart showing distribution (On Time, Minor, Moderate, Major, Severe, Early)
- **Distance Categories**: Distribution by flight distance ranges

#### 2. 🛩️ Airline Performance
- **Average Delay Ranking**: All airlines ranked by average arrival delay
- **On-Time Performance**: Percentage of flights arriving within 15 minutes
- **Flight Volume**: Total flights operated by each airline
- **Cancellation Rates**: Carrier-wise cancellation analysis
- **Departure vs Arrival Delays**: Comparative analysis of delay recovery

#### 3. 🛤️ Route Analysis
- **Top 20 Busiest Routes**: Routes with highest flight volumes
- **Most Delayed Routes**: Routes with worst average delays (min 50 flights)
- **Best Performing Routes**: Routes with best on-time performance
- **Top Airports by Departures**: Busiest origin airports
- **Top Airports by Arrivals**: Busiest destination airports
- **Airport Delay Performance**: Average departure delays by airport

#### 4. ⏰ Temporal Patterns
- **Hourly Flight Distribution**: Flight volume throughout the day
- **Hourly Delay Patterns**: Average delays by departure hour
- **Daily Patterns**: Flight volume and delays by day of week
- **Seasonal Analysis**: Flight volume, delays, and cancellations by season
- **Interactive Heatmap**: Hour vs Day of Week delay patterns

#### 5. 📊 Delay Analysis
- **Delay Component Breakdown**: Air System, Security, Airline, Late Aircraft, Weather
- **Delay Distribution**: Histogram of arrival delays with markers
- **Delay Categories**: Bar chart of flight counts by delay severity
- **Cancellation Reasons**: Pie chart showing reasons for cancellations

#### 6. 🌍 Geographic Insights
- **Busiest Airports**: Top 20 airports by total traffic (arrivals + departures)
- **Airport Delay Performance**: Airports ranked by average departure delay
- **Route Flow Analysis**: Scatter plot of distance vs delay (bubble size = flight count)
- **Distance Category Analysis**: Flight counts and delays by distance ranges
- **Interactive Map Links**: References to pre-generated geographic visualizations

#### 7. 🎯 Recommendations
- **Key Findings**: Operational performance, airline rankings, temporal patterns
- **Best/Worst Performers**: Data-driven identification of best airlines, hours, seasons
- **Actionable Recommendations**: 
  - For Airlines: Schedule optimization, weather prep, benchmarking
  - For Airports: Capacity management, infrastructure investment
  - For Passengers: Airline selection, timing strategies, seasonal planning
- **Advanced Insights**: Delay patterns, efficiency metrics, external factors
- **Methodology**: Dataset information and analysis approach

### 🔍 Smart Filters
- **Airline Filter**: Multi-select dropdown to analyze specific carriers
- **Month Filter**: Select specific months for seasonal analysis
- **Real-time Updates**: All visualizations update based on filter selections
- **Filter Indicator**: Shows filtered count vs total flights

### 📈 Visualizations
- **Interactive Charts**: Plotly-powered with zoom, pan, hover details
- **Color Coding**: Green-yellow-red scales for performance metrics
- **Reference Lines**: On-time markers, zero-delay indicators
- **Responsive Design**: Adapts to different screen sizes
- **Export Capability**: Download charts as PNG images

## 📊 Key Insights & Findings

### Overall Performance Metrics
- **On-Time Performance**: 82.41% of flights arrive within 15 minutes of schedule
- **Average Delay**: 4.33 minutes (overall arrival delay)
- **Average Departure Delay**: 9.23 minutes
- **Cancellation Rate**: 1.54% of all scheduled flights
- **Diversion Rate**: 0.26% of flights diverted to alternate airports
- **Average Distance**: 822 miles per flight

### Airline Performance
- **Best Performer**: Alaska Airlines (AS) with -0.97 min average delay
- **Most Challenging**: Spirit Airlines (NK) with 14.2 min average delay
- **Range**: Wide variation in airline performance from -1 to +14 minutes
- **On-Time Leaders**: Airlines with >85% on-time performance
- **Cancellation Patterns**: Varies significantly by carrier

### Temporal Patterns
- **Best Hour for Departure**: Early morning flights (3:00-6:00 AM) have lowest delays
- **Peak Delay Hours**: Evening departures (7:00-9:00 PM) experience highest delays
- **Day of Week**: Weekday patterns differ from weekends
- **Seasonal Variations**: 
  - Summer and Winter show higher delay rates
  - Fall typically has best on-time performance
  - Spring shows moderate delays

### Route & Airport Insights
- **Total Unique Routes**: 8,609 routes analyzed
- **Busiest Routes**: High-volume corridors between major hubs
- **Airport Congestion**: Major hubs show higher delay rates
- **Distance Impact**: Medium-haul flights (500-1500 miles) most common
- **Geographic Patterns**: Regional variations in delay patterns

### Delay Component Breakdown
When delays occur, they are primarily caused by:
- **Air System Delays**: National Airspace System issues
- **Carrier Delays**: Airline operational issues
- **Late Aircraft**: Ripple effects from previous delays
- **Weather Delays**: Meteorological conditions
- **Security Delays**: Security screening issues (minimal)

### Cancellation Analysis
- **Primary Reasons**: Weather, airline operations, NAS issues
- **Seasonal Peaks**: Higher cancellation rates during winter
- **Airline Variation**: Some carriers have higher cancellation rates
- **Recovery Patterns**: Most cancellations occur during adverse conditions

## 🔧 Technical Details

### Technologies Used
- **Python 3.9+**: Core programming language
- **Pandas 2.1.4**: Data manipulation and analysis
- **NumPy 1.26.2**: Numerical computations
- **Matplotlib 3.8.2**: Statistical visualizations
- **Seaborn 0.13.0**: Enhanced statistical plots
- **Plotly 5.17.0**: Interactive visualizations and dashboards
- **Streamlit 1.28.1**: Web dashboard framework
- **Folium 0.15.0**: Geographic mapping
- **Jupyter Notebook**: Interactive analysis environment

### Key Features Engineered
- **Date Components**: `YEAR`, `MONTH`, `DAY`, `DAY_OF_WEEK`
- **Time Features**: `DAY_NAME` (Monday-Sunday), `DEP_HOUR` (0-23), `DEP_MINUTE`
- **Route Information**: `ROUTE` (ORIGIN-DESTINATION pair)
- **Delay Classification**: `DELAY_CATEGORY` (Early, On Time, Minor, Moderate, Major, Severe)
- **Seasonal Mapping**: `SEASON` (Winter, Spring, Summer, Fall)
- **Aggregate Metrics**: `TOTAL_DELAY` (sum of all delay components)
- **Distance Grouping**: `DISTANCE_CATEGORY` (Short, Medium, Long, Ultra Long)
- **Date Format**: `FL_DATE` (formatted flight date)

### Data Processing Pipeline
1. **Data Loading**: Read CSV files with optimized dtypes
2. **Data Cleaning**: Handle missing values and outliers
3. **Feature Engineering**: Create derived features from raw data
4. **Memory Optimization**: Reduce memory footprint by 40%
5. **Data Validation**: Ensure data quality and consistency
6. **Statistical Summary**: Generate comprehensive statistics
7. **Export**: Save processed data for dashboard consumption

### Dashboard Architecture
- **Single Page App**: Streamlit with multi-page navigation
- **Cached Data Loading**: `@st.cache_data` decorator for performance
- **Dynamic Filtering**: Real-time data filtering without page reload
- **Responsive Layout**: Column-based layouts adapting to screen size
- **State Management**: Session-based filter persistence
- **Error Handling**: Graceful degradation for missing data

### Performance Optimizations
- **Efficient Groupby**: Optimized aggregation operations
- **Vectorized Operations**: NumPy-based computations
- **Data Type Optimization**: Reduced memory usage
- **Lazy Loading**: Load data only when needed
- **Caching**: Cache expensive computations
- **Sampling**: Smart sampling for visualization (when appropriate)

## 📚 Documentation

Comprehensive documentation is available:

- **README.md**: This file - complete project overview and setup guide
- **configuration/analysis_summary.json**: Real-time statistics and comprehensive metrics
- **Dashboard Help**: Built-in tooltips and descriptions throughout the interactive dashboard
- **Code Comments**: Well-documented Python code for easy understanding
- **Inline Documentation**: Each visualization includes clear labels and descriptions

## 🧪 Testing

The project includes testing capabilities:

```bash
# Run dashboard tests (if available)
python testing/test_dashboard.py

# Run full test suite (if available)
python testing/test_suite.py
```

## 🎓 Use Cases

This project is ideal for:

### Education & Learning
- **Data Science Portfolio**: Demonstrates complete data science workflow from raw data to insights
- **Streamlit Development**: Professional example of interactive dashboard creation
- **Data Visualization**: Showcases 50+ different visualization techniques
- **Feature Engineering**: Real-world examples of creating meaningful features
- **Large Dataset Handling**: Techniques for efficiently processing 5.8M+ records
- **Python Best Practices**: Clean, documented, and maintainable code

### Business & Industry
- **Aviation Analytics**: Deep understanding of flight operations and delay factors
- **Business Intelligence**: Transform raw data into actionable business insights
- **Performance Benchmarking**: Compare airlines, routes, and airports objectively
- **Operational Planning**: Data-driven scheduling and resource allocation decisions
- **Customer Experience**: Understand factors affecting passenger satisfaction
- **Risk Management**: Identify high-risk routes, times, and conditions

### Research & Analysis
- **Statistical Analysis**: Real-world application of statistical methods
- **Temporal Analysis**: Time-series patterns, seasonality, and trends
- **Geographic Analysis**: Spatial patterns and regional variations
- **Correlation Studies**: Relationships between multiple operational variables
- **Predictive Modeling**: Foundation for machine learning model development
- **Causal Analysis**: Understanding root causes of delays and cancellations

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/new-analysis`)
3. **Make your changes** and add tests if applicable
4. **Commit your changes** (`git commit -m 'Add new analysis feature'`)
5. **Push to the branch** (`git push origin feature/new-analysis`)
6. **Submit a pull request**

### Areas for Contribution
- Additional visualizations and insights
- Performance optimizations for large datasets
- New feature engineering techniques
- Enhanced dashboard features
- Machine learning models for delay prediction
- Real-time data integration
- Mobile-responsive design improvements
- Documentation enhancements
- Bug fixes and code quality improvements

## 📄 License

This project is for educational and analytical purposes. The data used is publicly available aviation data from the U.S. Department of Transportation. Please ensure compliance with data usage terms and privacy regulations when using or distributing this project.

## 🙏 Acknowledgments

- **Dataset Source**: U.S. Department of Transportation (2015 Flight Data)
- **Built With**: Python, Pandas, Streamlit, Plotly, and other open-source tools
- **Inspired By**: Real-world aviation analytics needs and data science best practices
- **Community**: Thanks to the open-source community for excellent libraries and tools

## 📞 Support & Contact

For questions, issues, or suggestions:

### Common Issues & Solutions

1. **Dashboard won't start**
   - Verify all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version: Must be 3.9 or higher
   - Ensure virtual environment is activated

2. **Data loading errors**
   - Verify all dataset files are in the `dataset/` folder
   - Check file paths are correct (case-sensitive on Linux/Mac)
   - Ensure sufficient disk space (2GB+ required)

3. **Performance issues**
   - Ensure minimum 4GB RAM available
   - Close other memory-intensive applications
   - Use filters to reduce data volume

4. **Visualization not displaying**
   - Update browser to latest version
   - Clear browser cache
   - Try different browser (Chrome/Firefox recommended)

### Getting Help

- Review the dashboard's built-in help and tooltips
- Check code comments for implementation details
- Examine `configuration/analysis_summary.json` for data structure
- Open an issue on the project repository with detailed error information

## 🚀 Future Enhancements

Potential areas for expansion:

### Short-term
- **Enhanced Filters**: Add date range picker, airport selection
- **Export Features**: CSV/Excel export of filtered data
- **Comparison Mode**: Side-by-side airline/route comparisons
- **Dark Mode**: Theme toggle for better viewing experience

### Medium-term
- **Machine Learning Models**: Predict flight delays using engineered features
- **Anomaly Detection**: Identify unusual delay patterns automatically
- **Advanced Analytics**: Clustering analysis of similar routes/airlines
- **Mobile App**: React Native or Flutter mobile companion

### Long-term
- **Real-time Integration**: Live flight tracking and delay prediction
- **API Development**: RESTful API for programmatic data access
- **Automated Reporting**: Scheduled email reports with insights
- **Multi-year Analysis**: Trend analysis across multiple years
- **Weather Integration**: Real-time weather impact analysis
- **Social Features**: User accounts, saved filters, shared insights

---

**AirFly Insights** | Comprehensive Flight Delay Analysis | Data Science Project

*Version 1.0 | Last Updated: January 2026*

Built with ❤️ using Python, Streamlit, and Plotly
