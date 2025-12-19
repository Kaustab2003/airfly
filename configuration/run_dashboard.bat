@echo off
echo Starting AirFly Insights Streamlit Dashboard...
echo.
cd /d "%~dp0"
streamlit run dashboard.py
pause