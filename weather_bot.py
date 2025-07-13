import requests
import schedule
import time
from datetime import datetime

def get_weather(city="San Jose"):
    api_key = "1a7d88723d851ab7c7e3e5e14d4891cd"  # Enter API key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        return {
            'city': city,  
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'weather': data['weather'][0]['description'],
            'rain_chance': data.get('rain', {}).get('1h', 0)
        }
    except Exception as e:
        print(f"Weather data loading failed: {e}")
        return None

def clothing_recommendation(temp):
    if temp < 5: return "🧥 It's essential to wear a coat!"
    elif temp < 15: return "🧥 Wear a thick coat"
    elif temp < 25: return "👕 Wear a moderate outfit"
    else: return "👕 Wear light clothing"

def format_weather_message(weather_data):
    if not weather_data:
        return "Weather information cannot be obtained."
    
    city = weather_data['city']  # Dynamic city name
    temp = weather_data['temp']
    feels_like = weather_data['feels_like']
    humidity = weather_data['humidity']
    weather = weather_data['weather']
    
    message = f"""🌤️ Today's weather alert
📍 {city}
🌡️ Temperature: {temp}°C (Feels like: {feels_like}°C)
💧 Humidity: {humidity}%
☁️ Weather: {weather}
{clothing_recommendation(temp)}"""  # Clothing recommendation
    
    # Umbrella alert logic
    if weather_data['rain_chance'] > 0 or any(word in weather for word in ['rain', 'snow', 'thunder']):
        message += "\n☔ Don't forget to bring an umbrella!"
    
    return message

def save_weather_alert(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = "weather_alerts.txt"
    
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]\n{message}\n{'='*50}\n\n")
    
    print(f"Weather alert saved: {filename}")

def daily_weather_alert():
    print("Weather alert running...")
    weather_data = get_weather()
    message = format_weather_message(weather_data)
    save_weather_alert(message)
    print("Completed!")

# Scheduling: every day at 9am
schedule.every().day.at("09:00").do(daily_weather_alert)

# Test: run immediately
print("Test run:")
daily_weather_alert()

# Main loop
print("Weather alert bot started! (runs every day at 9am)")
while True:
    schedule.run_pending()
    time.sleep(60)