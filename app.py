from flask import Flask, render_template, jsonify
import requests
import datetime
import pytz
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("PIRATE_WEATHER_API_KEY")

app = Flask(__name__)

# Config
LAT = "38.6582"  # Woodbridge, VA
LON = "-77.2497"
TZ = pytz.timezone("America/New_York")

# Cache weather to avoid excessive API calls
_cache = {
    "timestamp": None,
    "data": None,
}


def _fetch_weather():
    """Fetch full weather data including hourly information."""
    url = (
        f"https://api.pirateweather.net/forecast/{API_KEY}/{LAT},{LON}?exclude=minutely,alerts,flags&units=us"
    )
    response = requests.get(url)
    return response.json()

def get_weather():
    """Return current weather and time information.

    Weather data is cached for 10 minutes, but the time and theme mode are
    recalculated on every call so the clock stays accurate.
    """
    now_dt = datetime.datetime.now(TZ)
    try:
        if (
            _cache["data"]
            and _cache["timestamp"]
            and (now_dt - _cache["timestamp"]).total_seconds() < 600
        ):
            data = _cache["data"]
        else:
            data = _fetch_weather()
            _cache["timestamp"] = now_dt
            _cache["data"] = data

        current = data['currently']
        daily = data['daily']['data'][:4]  # Next 4 days

        now = datetime.datetime.now(TZ).time()

        # Theme logic
        if datetime.time(23, 0) <= now or now < datetime.time(8, 30):
            mode = "darker"
        elif datetime.time(8, 30) <= now <= datetime.time(18, 30):
            mode = "light"
        else:
            mode = "dark"
            

        now_ts = datetime.datetime.now(TZ)
        return {
            "time": now_ts.strftime("%-I:%M %p"),
            "timestamp": int(now_ts.timestamp()),
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


def get_hourly_forecast(day_index: int):
    """Return hourly forecast data for the given day index."""
    now_dt = datetime.datetime.now(TZ)
    if (
        _cache["data"]
        and _cache["timestamp"]
        and (now_dt - _cache["timestamp"]).total_seconds() < 600
    ):
        data = _cache["data"]
    else:
        data = _fetch_weather()
        _cache["timestamp"] = now_dt
        _cache["data"] = data

    start_date = now_dt.date() + datetime.timedelta(days=day_index)
    hourly_data = []
    for hour in data.get("hourly", {}).get("data", []):
        dt = datetime.datetime.fromtimestamp(hour["time"], TZ)
        if dt.date() == start_date:
            hourly_data.append(
                {
                    "time": dt.strftime("%-I %p"),
                    "temperature": round(hour["temperature"]),
                    "icon": hour.get("icon", "clear-day"),
                    "summary": hour.get("summary", ""),
                }
            )
    return {
        "day": start_date.strftime("%A %B %-d"),
        "hourly": hourly_data,
    }

@app.route("/")
def home():
    weather = get_weather()
    if not weather:
        return render_template("index.html", weather=None)
    return render_template("index.html", weather=weather)


@app.route("/api")
def api():
    """Return current data in JSON for AJAX updates."""
    weather = get_weather()
    if not weather:
        return jsonify({"error": "Weather data unavailable"}), 500
    return jsonify(weather)


@app.route("/day/<int:idx>")
def day_detail(idx):
    """Show hourly forecast and radar for the selected day."""
    forecast = get_hourly_forecast(idx)
    radar_url = (
        "https://embed.windy.com/embed2.html?lat="
        f"{LAT}&lon={LON}&detailLat={LAT}&detailLon={LON}&width=650&height=450&zoom=5"
        "&level=surface&overlay=radar&menu=&message=true&marker=&calendar=&pressure="
        "&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default"
    )
    return render_template("detail.html", forecast=forecast, radar_url=radar_url)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
