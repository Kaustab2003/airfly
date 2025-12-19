# AirFly Insights - Streamlit Dashboard

A comprehensive interactive dashboard for airline operations analysis built with Streamlit.

## 🚀 Features

- **Overview Dashboard**: Key performance metrics and summary statistics
- **Airline Performance**: Detailed analysis of airline punctuality and reliability
- **Route Analysis**: Busiest routes, delay patterns, and airport performance
- **Temporal Patterns**: Hourly, daily, and seasonal flight patterns
- **Delay Analysis**: Component breakdown and distribution analysis
- **Recommendations**: Data-driven insights and actionable recommendations

## 📊 Key Metrics

- **Total Flights Analyzed**: 100,000
- **On-Time Performance**: 82.3%
- **Average Delay**: 4.34 minutes
- **Cancellation Rate**: 1.55%
- **Unique Airlines**: 14
- **Unique Routes**: 6,980

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone or download the project files**
   ```bash
   cd airfly-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure data files are available**
   - The dashboard expects the following files in the `dataset/` folder:
     - `final_processed_flights.csv` (processed flight data)
     - `airlines.csv` (airline information)
     - `airports.csv` (airport information)
     - `analysis_summary.json` (summary statistics)

## 🎯 Running the Dashboard

1. **Navigate to the project directory**
   ```bash
   cd /path/to/airfly-project
   ```

2. **Run the Streamlit app**
   ```bash
   streamlit run dashboard.py
   ```

3. **Access the dashboard**
   - Open your web browser and go to: `http://localhost:8501`
   - The dashboard will automatically load and display the analysis

## 📁 Project Structure

```
airfly-project/
├── dashboard.py              # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── run_dashboard.bat         # Windows launcher
├── run_dashboard.py          # Python launcher
├── dataset/                  # Data files
│   ├── final_processed_flights.csv
│   ├── airlines.csv
│   ├── airports.csv
│   ├── analysis_summary.json
│   └── ... (other data files)
└── AirFly_Insights_Comprehensive.ipynb  # Original analysis notebook
```

## 🎨 Dashboard Sections

### 🏠 Overview
- Key performance indicators
- Monthly flight distribution
- Top airlines by volume
- Delay category breakdown

### 🛩️ Airline Performance
- Average delay by airline
- On-time performance comparison
- Cancellation rates analysis

### 🛤️ Route Analysis
- Top routes by flight volume
- Route delay analysis
- Airport performance metrics

### ⏰ Temporal Patterns
- Hourly flight and delay patterns
- Day-of-week analysis
- Seasonal trends and cancellations

### 📊 Delay Analysis
- Delay component breakdown
- Delay distribution histograms
- Cancellation reason analysis

### 🎯 Recommendations
- Key findings summary
- Actionable recommendations for airlines, airports, and passengers
- Methodology documentation

## 🔧 Customization

### Modifying Data Sources
- Update file paths in the `load_data()` function
- Ensure CSV files have the expected column names
- Update the `analysis_summary.json` with new metrics

### Adding New Visualizations
- Add new functions in the respective page sections
- Use Plotly for interactive charts
- Follow the existing styling patterns

### Styling Changes
- Modify the CSS in the `st.markdown()` section at the top
- Update color schemes and layouts as needed

## 📈 Data Insights

### Top Performers
- **Most Punctual Airline**: Alaska Airlines (AS) - -1.1 min average delay
- **Best Departure Hour**: 3:00 AM - -9.1 min average delay
- **Best Season**: Fall - 0.0 min average delay
- **Busiest Route**: LAX-SFO

### Key Challenges
- **Highest Delays**: Frontier Airlines (F9) - 13.1 min average delay
- **Worst Hour**: 7:00 PM - 9.6 min average delay
- **Worst Season**: Summer - 6.9 min average delay

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and analytical purposes. Please ensure compliance with data usage terms and privacy regulations.

## 📞 Support

For questions or issues:
- Check the data files are in the correct location
- Ensure all dependencies are installed
- Verify Python version compatibility

---

**AirFly Insights** | Comprehensive Airline Operations Analysis | Built with Streamlit