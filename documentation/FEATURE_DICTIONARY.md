# AirFly Insights - Feature Dictionary

**Document Version**: 1.0  
**Last Updated**: December 18, 2025  
**Dataset**: Airlines Flights Data (2015)

---

## 📋 Table of Contents

1. [Original Features](#original-features)
2. [Engineered Features](#engineered-features)
3. [Derived Metrics](#derived-metrics)
4. [Feature Categories](#feature-categories)

---

## 🔤 Original Features

### Flight Identification
| Feature | Type | Description | Example | Null Handling |
|---------|------|-------------|---------|---------------|
| `FL_DATE` | datetime | Flight date | 2015-01-01 | Required |
| `TAIL_NUMBER` | string | Aircraft tail number | N12345 | Allow null |
| `FL_NUMBER` | integer | Flight number | 1234 | Required |

### Airline & Route Information
| Feature | Type | Description | Example | Null Handling |
|---------|------|-------------|---------|---------------|
| `AIRLINE` | categorical | Airline carrier code (2-letter) | AA, DL, UA | Required |
| `ORIGIN_AIRPORT` | categorical | Departure airport code (3-letter IATA) | ATL, ORD, DFW | Required |
| `DESTINATION_AIRPORT` | categorical | Arrival airport code (3-letter IATA) | LAX, JFK, MIA | Required |

### Timing Information
| Feature | Type | Description | Example | Null Handling |
|---------|------|-------------|---------|---------------|
| `SCHEDULED_DEPARTURE` | integer | Scheduled departure time (HHMM format) | 1530 (3:30 PM) | Required |
| `DEPARTURE_TIME` | integer | Actual departure time (HHMM format) | 1545 (3:45 PM) | Null if cancelled |
| `SCHEDULED_ARRIVAL` | integer | Scheduled arrival time (HHMM format) | 1830 (6:30 PM) | Required |
| `ARRIVAL_TIME` | integer | Actual arrival time (HHMM format) | 1855 (6:55 PM) | Null if cancelled |

### Delay Information
| Feature | Type | Description | Example | Unit | Null Handling |
|---------|------|-------------|---------|------|---------------|
| `DEPARTURE_DELAY` | float | Departure delay (negative = early) | 15 | minutes | Fill 0 |
| `ARRIVAL_DELAY` | float | Arrival delay (negative = early) | 25 | minutes | Fill 0 |
| `CARRIER_DELAY` | float | Delay due to airline operations | 10 | minutes | Fill 0 |
| `WEATHER_DELAY` | float | Delay due to weather conditions | 5 | minutes | Fill 0 |
| `NAS_DELAY` | float | Delay due to National Aviation System | 8 | minutes | Fill 0 |
| `SECURITY_DELAY` | float | Delay due to security issues | 2 | minutes | Fill 0 |
| `LATE_AIRCRAFT_DELAY` | float | Delay due to late arriving aircraft | 12 | minutes | Fill 0 |

### Distance & Duration
| Feature | Type | Description | Example | Unit |
|---------|------|-------------|---------|------|
| `DISTANCE` | integer | Flight distance | 1500 | miles |
| `SCHEDULED_TIME` | integer | Scheduled flight duration | 180 | minutes |
| `ELAPSED_TIME` | integer | Actual flight duration | 195 | minutes |
| `AIR_TIME` | integer | Time in the air | 165 | minutes |
| `TAXI_OUT` | integer | Taxi-out time | 15 | minutes |
| `TAXI_IN` | integer | Taxi-in time | 10 | minutes |

### Operational Flags
| Feature | Type | Description | Values | Null Handling |
|---------|------|-------------|--------|---------------|
| `CANCELLED` | binary | Flight cancellation flag | 0, 1 | Fill 0 |
| `CANCELLATION_REASON` | categorical | Reason for cancellation | A, B, C, D, No Cancellation | Fill "No Cancellation" |
| `DIVERTED` | binary | Flight diversion flag | 0, 1 | Fill 0 |

### Cancellation Reason Codes
- **A**: Carrier/Airline fault
- **B**: Weather
- **C**: National Aviation System (NAS)
- **D**: Security

---

## ⚙️ Engineered Features

### Temporal Features
| Feature | Type | Description | Derivation | Example |
|---------|------|-------------|------------|---------|
| `YEAR` | integer | Flight year | Extracted from FL_DATE | 2015 |
| `MONTH` | integer | Flight month | Extracted from FL_DATE | 6 (June) |
| `DAY` | integer | Flight day | Extracted from FL_DATE | 15 |
| `DAY_OF_WEEK` | integer | Day of week (0=Monday) | Extracted from FL_DATE | 2 (Wednesday) |
| `DAY_NAME` | categorical | Day name | Derived from DAY_OF_WEEK | "Wednesday" |
| `DEP_HOUR` | integer | Departure hour (24-hour) | SCHEDULED_DEPARTURE // 100 | 15 (3 PM) |
| `DEP_MINUTE` | integer | Departure minute | SCHEDULED_DEPARTURE % 100 | 30 |
| `SEASON` | categorical | Season of flight | Based on MONTH | "Summer" |

**Season Mapping:**
- **Winter**: December, January, February
- **Spring**: March, April, May
- **Summer**: June, July, August
- **Fall**: September, October, November

### Route Features
| Feature | Type | Description | Derivation | Example |
|---------|------|-------------|------------|---------|
| `ROUTE` | categorical | Origin-Destination pair | ORIGIN + "-" + DESTINATION | "ATL-LAX" |

### Delay Category Features
| Feature | Type | Description | Derivation | Categories |
|---------|------|-------------|------------|-----------|
| `DELAY_CATEGORY` | categorical | Delay severity classification | Binned ARRIVAL_DELAY | Early, On Time, Minor Delay, Major Delay |

**Delay Category Bins:**
- **Early**: ARRIVAL_DELAY < -15 minutes
- **On Time**: -15 ≤ ARRIVAL_DELAY ≤ 15 minutes
- **Minor Delay**: 15 < ARRIVAL_DELAY ≤ 60 minutes
- **Major Delay**: ARRIVAL_DELAY > 60 minutes

### Aggregate Delay Features
| Feature | Type | Description | Derivation | Unit |
|---------|------|-------------|------------|------|
| `TOTAL_DELAY` | float | Sum of all delay components | Sum of all *_DELAY columns | minutes |

**Formula:**
```
TOTAL_DELAY = CARRIER_DELAY + WEATHER_DELAY + NAS_DELAY + SECURITY_DELAY + LATE_AIRCRAFT_DELAY
```

---

## 📊 Derived Metrics

### Performance Metrics
| Metric | Type | Description | Calculation | Target/Benchmark |
|--------|------|-------------|-------------|------------------|
| `On-Time Performance (OTP)` | percentage | % of flights on-time | (On-Time Flights / Total Flights) × 100 | 80-85% |
| `Cancellation Rate` | percentage | % of cancelled flights | (Cancelled Flights / Total Flights) × 100 | <3% |
| `Average Delay` | float | Mean arrival delay | Mean(ARRIVAL_DELAY) | <15 minutes |
| `Median Delay` | float | Median arrival delay | Median(ARRIVAL_DELAY) | <5 minutes |
| `Delay Standard Deviation` | float | Variability in delays | StdDev(ARRIVAL_DELAY) | Lower is better |

### Route-Level Metrics
| Metric | Type | Description | Calculation |
|--------|------|-------------|-------------|
| `Route Volume` | integer | Number of flights per route | Count(flights) per ROUTE |
| `Route Average Delay` | float | Average delay per route | Mean(ARRIVAL_DELAY) per ROUTE |
| `Route Cancellation Rate` | percentage | Cancellation rate per route | (Cancelled / Total) per ROUTE |

### Airline-Level Metrics
| Metric | Type | Description | Calculation |
|--------|------|-------------|-------------|
| `Airline OTP` | percentage | On-time performance per airline | OTP per AIRLINE |
| `Airline Average Delay` | float | Average delay per airline | Mean(ARRIVAL_DELAY) per AIRLINE |
| `Airline Reliability Score` | float | Combined performance metric | Weighted: 0.5×OTP + 0.3×(1-AvgDelay/60) + 0.2×(1-CancelRate) |

### Airport-Level Metrics
| Metric | Type | Description | Calculation |
|--------|------|-------------|-------------|
| `Airport Traffic Volume` | integer | Total flights (origin + destination) | Count per airport |
| `Airport Average Departure Delay` | float | Avg departure delay | Mean(DEPARTURE_DELAY) per ORIGIN_AIRPORT |
| `Airport Average Arrival Delay` | float | Avg arrival delay | Mean(ARRIVAL_DELAY) per DESTINATION_AIRPORT |

### Temporal Metrics
| Metric | Type | Description | Calculation |
|--------|------|-------------|-------------|
| `Hourly Delay Pattern` | float | Average delay by hour | Mean(ARRIVAL_DELAY) per DEP_HOUR |
| `Daily Delay Pattern` | float | Average delay by day of week | Mean(ARRIVAL_DELAY) per DAY_OF_WEEK |
| `Monthly Delay Trend` | float | Average delay by month | Mean(ARRIVAL_DELAY) per MONTH |
| `Seasonal Performance` | float | Average delay by season | Mean(ARRIVAL_DELAY) per SEASON |

---

## 🏷️ Feature Categories

### 1. Temporal Features
Used for time-based analysis and trend identification.

**Features:**
- `FL_DATE`, `YEAR`, `MONTH`, `DAY`
- `DAY_OF_WEEK`, `DAY_NAME`
- `DEP_HOUR`, `DEP_MINUTE`
- `SEASON`
- `SCHEDULED_DEPARTURE`, `DEPARTURE_TIME`
- `SCHEDULED_ARRIVAL`, `ARRIVAL_TIME`

**Use Cases:**
- Identifying peak delay hours
- Seasonal trend analysis
- Day-of-week patterns
- Time series forecasting

### 2. Route Features
Used for geographic and route-level analysis.

**Features:**
- `ORIGIN_AIRPORT`
- `DESTINATION_AIRPORT`
- `ROUTE`
- `DISTANCE`

**Use Cases:**
- Route performance comparison
- Hub analysis
- Distance-delay correlation
- Geographic visualization

### 3. Delay Features
Used for delay analysis and root cause identification.

**Features:**
- `DEPARTURE_DELAY`
- `ARRIVAL_DELAY`
- `CARRIER_DELAY`
- `WEATHER_DELAY`
- `NAS_DELAY`
- `SECURITY_DELAY`
- `LATE_AIRCRAFT_DELAY`
- `TOTAL_DELAY`
- `DELAY_CATEGORY`

**Use Cases:**
- Delay attribution analysis
- Performance benchmarking
- Improvement opportunity identification
- Predictive modeling

### 4. Operational Features
Used for understanding flight operations and issues.

**Features:**
- `CANCELLED`
- `CANCELLATION_REASON`
- `DIVERTED`
- `SCHEDULED_TIME`
- `ELAPSED_TIME`
- `AIR_TIME`
- `TAXI_OUT`, `TAXI_IN`

**Use Cases:**
- Cancellation pattern analysis
- Operational efficiency assessment
- Ground operation optimization
- Reliability metrics

### 5. Identification Features
Used for tracking and joining datasets.

**Features:**
- `AIRLINE`
- `TAIL_NUMBER`
- `FL_NUMBER`
- `FL_DATE`

**Use Cases:**
- Data joining/merging
- Unique flight identification
- Airline-specific analysis
- Aircraft tracking

---

## 🔍 Data Quality Notes

### Missing Value Treatment
1. **Delay columns**: Filled with 0 (indicates no delay)
2. **Cancellation reason**: Filled with "No Cancellation"
3. **Actual times**: Kept as null if flight cancelled (valid missing)
4. **Tail number**: Allowed to be null (not critical for analysis)

### Data Type Conversions
1. **Categorical optimization**: Low-cardinality strings → category type
2. **Numeric downcast**: int64 → int32, float64 → float32 (where appropriate)
3. **Date parsing**: String dates → datetime64
4. **Memory optimization**: 95% reduction achieved (2.1GB → 88.8MB)

### Feature Validation Rules
1. **Delay consistency**: ARRIVAL_DELAY should approximately equal DEPARTURE_DELAY + adjustment
2. **Time logic**: ARRIVAL_TIME > DEPARTURE_TIME (accounting for timezone/date changes)
3. **Distance validation**: DISTANCE > 0 for all flights
4. **Binary flags**: CANCELLED and DIVERTED ∈ {0, 1}

---

## 📈 Feature Importance (Analysis Results)

### Top Delay Predictors
1. **LATE_AIRCRAFT_DELAY** (45.2%) - Most significant delay contributor
2. **CARRIER_DELAY** (28.7%) - Second major factor
3. **DEP_HOUR** - Strong correlation with delays (peak: 19:00-21:00)
4. **SEASON** - Summer shows higher delays
5. **AIRLINE** - Varies significantly by carrier

### Key Performance Indicators
1. **ARRIVAL_DELAY** - Primary target variable for analysis
2. **DELAY_CATEGORY** - Simplified classification for reporting
3. **CANCELLED** - Critical operational metric
4. **ROUTE** - Geographic performance variation

---

## 🔗 Related Documentation

- [README.md](README.md) - Project overview and setup
- [PROJECT_ASSESSMENT.md](PROJECT_ASSESSMENT.md) - Comprehensive project review
- [presentation_slides.md](presentation_slides.md) - Presentation materials
- [AirFly_Insights_Comprehensive.ipynb](AirFly_Insights_Comprehensive.ipynb) - Analysis notebook

---

## 📞 Support

For questions about feature definitions or data quality:
- Review the analysis notebook for implementation details
- Check the dashboard code for feature usage examples
- Refer to the original Kaggle dataset documentation

---

*Feature Dictionary Version 1.0*  
*Last Updated: December 18, 2025*  
*AirFly Insights Project*
