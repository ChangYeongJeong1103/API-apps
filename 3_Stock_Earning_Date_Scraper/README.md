# 📊 Stock Earnings Calendar Scraper

A Python tool that automatically scrapes earnings calendar data from Yahoo Finance for a predefined list of stock tickers. The scraper collects comprehensive earnings information and exports it to Excel format for easy analysis.

## 🚀 Features

- **Multi-source data collection**: Uses Yahoo Finance API with multiple fallback methods for reliability
- **Comprehensive earnings data**: Collects earnings dates, fiscal quarters, EPS estimates, and historical data
- **Smart sorting**: Automatically sorts results by earnings date (earliest first)
- **Excel export**: Generates a formatted Excel file with auto-adjusted column widths
- **Rate limiting**: Built-in delays to respect API limits
- **Robust error handling**: Gracefully handles missing data and API failures

## 📋 Requirements

- Python 3.7+
- Required packages:
  - `yfinance` - Yahoo Finance API wrapper
  - `pandas` - Data manipulation and Excel export
  - `openpyxl` - Excel file writing
  - `requests` - HTTP requests for API calls

## 🛠️ Installation

1. **Clone or download** the project files
2. **Install required packages**:
   ```bash
   pip install yfinance pandas openpyxl requests
   ```

## 💻 Usage

1. **Configure tickers** (optional): Edit the `TICKERS` list in `earnings_scraper.py` to customize which stocks to track
2. **Run the scraper**:
   ```bash
   python earnings_scraper.py
   ```
3. **Check results**: The output will be saved to `output/earnings_calendar.xlsx`

## 📊 Output Format

The Excel file contains the following columns:

| Column | Description |
|--------|-------------|
| **Ticker** | Stock symbol |
| **Earnings_Date** | Next earnings announcement date |
| **Fiscal_Quarter** | Fiscal quarter (e.g., Q1 2024) |
| **Last_Reported_EPS** | Most recent earnings per share |
| **EPS_Estimate** | Analyst EPS estimate for next earnings |
| **Days_Until_Earnings** | Days until next earnings (or "Today"/"X days ago") |

## 🎯 Default Tickers

The scraper is pre-configured to track these stocks:
- **Tech Giants**: NVDA, MSFT, AAPL, GOOGL, META
- **Streaming**: NFLX, SPOT
- **Growth Stocks**: PLTR, AVGO, HOOD, RKLB
- **Enterprise**: ORCL
- **Electric Vehicles**: TSLA
- **Emerging Tech**: AEVA

## 🔧 Customization

- **Change tickers**: Modify the `TICKERS` list in the configuration section
- **Adjust rate limiting**: Change `RATE_LIMIT_DELAY` value (default: 1 second)
- **Custom output location**: Modify `OUTPUT_FILE` path

## 📝 Logging

The scraper generates detailed logs in `earnings_scraper.log` for troubleshooting and monitoring data collection progress.

## ⚠️ Important Notes

- **Market hours**: Best results when run during market hours or shortly after
- **Data accuracy**: Uses multiple data sources with fallbacks for reliability
- **Rate limiting**: Includes built-in delays to respect Yahoo Finance API limits
- **Error handling**: Gracefully handles missing or unavailable data

## 🚨 Disclaimer

This tool is for educational and informational purposes only. Always verify earnings dates and financial data from official company sources before making investment decisions. 