#!/usr/bin/env python3
"""
🚀 EARNINGS SCRAPER - YAHOO FINANCE
Scrapes earnings calendar data using Yahoo Finance with multiple fallback methods
Author: AI Assistant
"""

import yfinance as yf
import pandas as pd
import logging
from datetime import datetime, timedelta
import time
import os
import requests
import json

# ===============================================================================
# 🔧 CONFIGURATION
# ===============================================================================

TICKERS = ["NVDA", "MSFT", "AAPL", "GOOGL", "META", "NFLX", "SPOT", "PLTR", "AVGO", "HOOD", "RKLB", "ORCL", "TSLA", "AEVA"]
print(f"📊 Total tickers to process: {len(TICKERS)}\n\n")
OUTPUT_DIR = "output"
OUTPUT_FILE = f"{OUTPUT_DIR}/earnings_calendar.xlsx"
RATE_LIMIT_DELAY = 1  # seconds between API calls

# ===============================================================================
# 🔧 LOGGING SETUP
# ===============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('earnings_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ===============================================================================
# 📊 EARNINGS SCRAPER CLASS
# ===============================================================================

class EarningsScraper:
    """Comprehensive earnings scraper using Yahoo Finance with multiple fallback methods."""
    
    def __init__(self):
        logger.info("Earnings scraper initialized")
    
    def get_earnings_api_data(self, symbol: str) -> dict:
        """
        Get detailed earnings information using Yahoo Finance API directly.
        This method gets quarters and estimates.
        """
        try:
            # Yahoo Finance earnings calendar endpoint
            url = f"https://query1.finance.yahoo.com/v7/finance/calendar/earnings"
            params = {
                'symbol': symbol,
                'formatted': 'true',
                'crumb': 'dummy',
                'lang': 'en-US',
                'region': 'US',
                'corsDomain': 'finance.yahoo.com'
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Parse earnings calendar data
                if 'earnings' in data and 'result' in data['earnings']:
                    results = data['earnings']['result']
                    
                    for result in results:
                        if result.get('ticker') == symbol:
                            earnings_info = {
                                'eps_estimate': result.get('epsEstimate', {}).get('raw', 'N/A'),
                                'quarter': result.get('quarter', 'N/A'),
                                'year': result.get('year', 'N/A'),
                                'earnings_date': result.get('earningsDate', 'N/A')
                            }
                            
                            logger.info(f"Found API earnings info for {symbol}: {earnings_info}")
                            return earnings_info
                            
        except Exception as e:
            logger.debug(f"API earnings info failed for {symbol}: {e}")
            
        return {
            'eps_estimate': 'N/A',
            'quarter': 'N/A',
            'year': 'N/A',
            'earnings_date': 'N/A'
        }

    def get_earnings_data(self, symbol: str) -> dict:
        """
        Get comprehensive earnings data for a single ticker using multiple methods.
        """
        logger.info(f"Fetching data for {symbol}")
        
        try:
            ticker = yf.Ticker(symbol)
            
            # Initialize with default values
            earnings_data = {
                'next_earnings_date': None,
                'last_reported_eps': 'N/A',
                'eps_estimate': 'N/A',
                'fiscal_quarter': 'N/A'
            }
            
            # 1. Get detailed earnings info from Yahoo Finance API
            api_data = self.get_earnings_api_data(symbol)
            if api_data['eps_estimate'] != 'N/A':
                earnings_data['eps_estimate'] = f"{float(api_data['eps_estimate']):.2f}"
            if api_data['quarter'] != 'N/A' and api_data['year'] != 'N/A':
                earnings_data['fiscal_quarter'] = f"Q{api_data['quarter']} {api_data['year']}"
            
            # 2. Get earnings date from calendar with robust handling
            try:
                calendar = ticker.calendar
                if calendar is not None:
                    # Try to get earnings date from calendar (both dict and DataFrame formats)
                    try:
                        # Handle dictionary format
                        if isinstance(calendar, dict) and 'Earnings Date' in calendar:
                            earnings_date_list = calendar['Earnings Date']
                            if isinstance(earnings_date_list, list) and len(earnings_date_list) > 0:
                                earnings_data['next_earnings_date'] = earnings_date_list[0].strftime('%Y-%m-%d')
                                logger.info(f"✅ Found earnings date from calendar dict: {earnings_data['next_earnings_date']}")
                        # Handle DataFrame format (wrapped in try/except to avoid type issues)
                        elif hasattr(calendar, 'index'):
                            first_index = calendar.index[0]
                            earnings_data['next_earnings_date'] = first_index.strftime('%Y-%m-%d')
                            logger.info(f"✅ Found earnings date from calendar DataFrame: {earnings_data['next_earnings_date']}")
                    except:
                        pass
            except Exception as e:
                logger.debug(f"Calendar method failed for {symbol}: {e}")
                
            # 3. Fallback: Get earnings date from info object
            if not earnings_data['next_earnings_date']:
                try:
                    info = ticker.info
                    if info and 'earningsDate' in info:
                        earnings_date_info = info['earningsDate']
                        if isinstance(earnings_date_info, list) and len(earnings_date_info) > 0:
                            earnings_data['next_earnings_date'] = earnings_date_info[0].strftime('%Y-%m-%d')
                            logger.info(f"✅ Found earnings date from info: {earnings_data['next_earnings_date']}")
                except Exception as e:
                    logger.debug(f"Info earnings date method failed for {symbol}: {e}")
            
            # 4. Get comprehensive company info for additional data
            try:
                info = ticker.info
                if info:
                    # Get EPS estimates with multiple fallbacks
                    if earnings_data['eps_estimate'] == 'N/A':
                        if 'forwardEps' in info and info['forwardEps']:
                            earnings_data['eps_estimate'] = f"{float(info['forwardEps']):.2f}"
                        elif 'epsForward' in info and info['epsForward']:
                            earnings_data['eps_estimate'] = f"{float(info['epsForward']):.2f}"
                    
                    # Get trailing EPS (last reported)
                    if 'trailingEps' in info and info['trailingEps']:
                        earnings_data['last_reported_eps'] = f"{float(info['trailingEps']):.2f}"
                    elif 'epsTrailingTwelveMonths' in info and info['epsTrailingTwelveMonths']:
                        earnings_data['last_reported_eps'] = f"{float(info['epsTrailingTwelveMonths']):.2f}"
                    
                    # Get fiscal quarter info if not already found
                    if earnings_data['fiscal_quarter'] == 'N/A':
                        if 'mostRecentQuarter' in info and info['mostRecentQuarter']:
                            most_recent_quarter = datetime.fromtimestamp(info['mostRecentQuarter'])
                            # Calculate next quarter
                            next_quarter_date = most_recent_quarter + timedelta(days=90)
                            quarter_num = ((next_quarter_date.month - 1) // 3) + 1
                            earnings_data['fiscal_quarter'] = f"Q{quarter_num} {next_quarter_date.year}"
                        
            except Exception as e:
                logger.debug(f"Info method failed for {symbol}: {e}")
            
            # 5. Get quarterly earnings for better EPS data
            try:
                quarterly_earnings = ticker.quarterly_earnings
                if quarterly_earnings is not None and not quarterly_earnings.empty:
                    # Get most recent EPS if not already found
                    if earnings_data['last_reported_eps'] == 'N/A':
                        most_recent_eps = quarterly_earnings.iloc[0]['Earnings']
                        if pd.notna(most_recent_eps):
                            earnings_data['last_reported_eps'] = f"{float(most_recent_eps):.2f}"
                    
                    # Determine fiscal quarter if not already found
                    if earnings_data['fiscal_quarter'] == 'N/A' and earnings_data['next_earnings_date']:
                        next_date = datetime.strptime(earnings_data['next_earnings_date'], '%Y-%m-%d')
                        quarter_num = ((next_date.month - 1) // 3) + 1
                        earnings_data['fiscal_quarter'] = f"Q{quarter_num} {next_date.year}"
                        
            except Exception as e:
                logger.debug(f"Quarterly earnings failed for {symbol}: {e}")
            
            return earnings_data
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return {
                'next_earnings_date': 'Error',
                'last_reported_eps': 'N/A',
                'eps_estimate': 'N/A',
                'fiscal_quarter': 'N/A'
            }
    
    def calculate_days_until_earnings(self, earnings_date: str) -> str:
        """Calculate days until earnings date."""
        try:
            if not earnings_date or earnings_date in ['N/A', 'Error', 'TBD']:
                return 'N/A'
            
            earnings_dt = datetime.strptime(earnings_date, '%Y-%m-%d')
            days_diff = (earnings_dt - datetime.now()).days
            
            if days_diff > 0:
                return f"{days_diff} days"
            elif days_diff == 0:
                return "Today"
            else:
                return f"{abs(days_diff)} days ago"
        except:
            return "Unknown"
    
    def scrape_all_tickers(self, tickers: list) -> list:
        """Scrape earnings data for all tickers."""
        logger.info(f"Scraping {len(tickers)} tickers")
        results = []
        
        for i, ticker in enumerate(tickers, 1):
            logger.info(f"Processing {i}/{len(tickers)}: {ticker}")
            
            # Get earnings data
            earnings_data = self.get_earnings_data(ticker)
            
            # Create final record
            record = {
                'Ticker': ticker,
                'Earnings_Date': earnings_data['next_earnings_date'] or 'TBD',
                'Fiscal_Quarter': earnings_data['fiscal_quarter'],
                'Last_Reported_EPS': earnings_data['last_reported_eps'],
                'EPS_Estimate': earnings_data['eps_estimate'],
                'Days_Until_Earnings': self.calculate_days_until_earnings(earnings_data['next_earnings_date'])
            }
            
            results.append(record)
            
            # Rate limiting
            if i < len(tickers):
                time.sleep(RATE_LIMIT_DELAY)
        
        # Sort results by earnings date (ascending order)
        results = self.sort_by_earnings_date(results)
        
        return results
    
    def sort_by_earnings_date(self, data: list) -> list:
        """
        Sort earnings data by earnings date in ascending order.
        Handles special cases like 'TBD', 'Error', 'N/A' by putting them at the end.
        """
        def sort_key(record):
            earnings_date = record['Earnings_Date']
            
            # Handle special cases - put them at the end
            if earnings_date in ['TBD', 'Error', 'N/A', None]:
                return datetime(9999, 12, 31)  # Far future date to sort last
            
            try:
                # Parse the date and return it for sorting
                return datetime.strptime(earnings_date, '%Y-%m-%d')
            except:
                # If parsing fails, put at the end
                return datetime(9999, 12, 31)
        
        # Sort by earnings date (earliest first)
        sorted_data = sorted(data, key=sort_key)
        
        logger.info("✅ Sorted earnings data by date (earliest first)")
        return sorted_data
    
    def export_to_excel(self, data: list, filename: str) -> bool:
        """Export data to Excel file."""
        try:
            if not data:
                logger.warning("No data to export")
                return False
            
            # Create DataFrame and export
            df = pd.DataFrame(data)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Earnings Calendar', index=False)
                
                # Auto-adjust column widths
                worksheet = writer.sheets['Earnings Calendar']
                for column in worksheet.columns:
                    max_length = max(len(str(cell.value)) for cell in column)
                    worksheet.column_dimensions[column[0].column_letter].width = max_length + 2
            
            logger.info(f"✅ Exported {len(data)} records to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Export failed: {e}")
            return False

# ===============================================================================
# 🚀 MAIN EXECUTION
# ===============================================================================

def main():
    """Main function to run the earnings scraper."""
    print("🚀 Starting Earnings Scraper...")
    print(f"📊 Processing tickers: {', '.join(TICKERS)}")
    
    # Initialize scraper
    scraper = EarningsScraper()
    
    # Scrape data
    earnings_data = scraper.scrape_all_tickers(TICKERS)
    
    # Export results
    if earnings_data:
        success = scraper.export_to_excel(earnings_data, OUTPUT_FILE)
        if success:
            print(f"✅ Data exported to {OUTPUT_FILE}")
            
            # Print summary
            print("\n" + "="*50)
            print("📊 EARNINGS SUMMARY")
            print("="*50)
            for record in earnings_data:
                print(f"{record['Ticker']}: {record['Earnings_Date']} | "
                      f"Quarter: {record['Fiscal_Quarter']} | "
                      f"Days: {record['Days_Until_Earnings']}")
            print("="*50)
        else:
            print("❌ Export failed")
    else:
        print("❌ No data found")
    
    print("🏁 Scraping completed!")

if __name__ == "__main__":
    main() 