# Weather Alert Bot

A Python bot that fetches daily weather data and provides clothing recommendations with umbrella alerts.

## Features

- Daily weather alerts at 9:00 AM
- Temperature-based clothing recommendations
- Umbrella alerts for rainy weather
- Saves weather history to text file

## Setup

1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your API key to `weather_bot.py`:
   ```python
   api_key = "your_api_key_here"
   ```
4. Run the bot:
   ```bash
   python weather_bot.py
   ```

## Output Example in weather_alarts.txt

## Customization

- Change city: Edit the `city` parameter in `get_weather()` function
- Change schedule time: Modify `schedule.every().day.at("09:00")`
- Adjust temperature thresholds: Edit `clothing_recommendation()` function

