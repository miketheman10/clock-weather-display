from flask import Flask, render_template
import requests
import datetime
import pytz
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("PIRATE_WEATHER_API_KEY")

app = Flask(__name__)

# Config
API_KEY = os.getenv("PIRATE_WEATHER_API_KEY")
LAT = "38.6582"  # Woodbridge, VA
LON = "-77.2497"
TZ = pytz.timezone("America/New_York")

def get_weather():
    try:
        url = f"https://api.pirateweather.net/forecast/{API_KEY}/{LAT},{LON}?exclude=minutely,hourly,alerts,flags&units=us"
        response = requests.get(url)
        data = response.json()

        current = data['currently']
        daily = data['daily']['data'][:4]  # Next 4 days

        now = datetime.datetime.now(TZ).time()

        if datetime.time(23, 0) <= now or now < datetime.time(8, 30):
            mode = "darker"
        elif datetime.time(19, 0) <= now:
            mode = "dark"
        else:
            mode = "light"

        return {
            "time": datetime.datetime.now(TZ).strftime("%-I:%M %p"),
            "temperature": round(current["temperature"]),
            "summary": current["summary"],
            "icon": current["icon"],
            "forecast": [
                {
                    "day": datetime.datetime.fromtimestamp(day["time"]).strftime("%a"),
                    "high": round(day["temperatureHigh"]),
                    "low": round(day["temperatureLow"]),
                    "icon": day["icon"]
                }
                for day in daily
            ],
            "mode": mode
        }
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None

@app.route("/")
def home():
    weather = get_weather()
    if not weather:
        return render_template("index.html", weather=None)
    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
