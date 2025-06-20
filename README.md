# Clock Weather Display

This project is a small Flask application that shows the current time and weather forecast. It is designed to run full-screen on a device such as a Raspberry Pi, turning it into a simple dashboard.

The server retrieves data from the Pirate Weather API and caches the response for ten minutes. JavaScript on the client polls the server once per minute so the clock stays accurate even if the device time drifts.

## Setup

1. Create a `.env` file in the project root with your Pirate Weather API key:

```
PIRATE_WEATHER_API_KEY=your_api_key_here
```

2. Install the required dependencies:

```
pip install flask python-dotenv requests pytz
```

3. Launch the application:

```
python app.py
```

Visit `http://localhost:5000` in your browser.

## Architecture

```
clock-weather-display/
├── app.py                # Flask server
├── templates/
│   └── index.html        # HTML page served to the client
├── static/
│   ├── css/style.css     # Styles for light/dark/darker themes
│   ├── js/theme.js       # Manual theme toggle logic
│   ├── js/update.js      # Polls the `/api` endpoint every minute
│   └── icons/            # Weather icons used in the UI
└── README.md
```

### Server

`app.py` exposes two routes:

- `/` – renders `index.html` with current weather data embedded in the page.
- `/api` – returns the same data in JSON format so the client can refresh without reloading.

The `get_weather()` helper fetches forecast information from Pirate Weather. Results are cached for 10 minutes in the `_cache` dictionary to avoid unnecessary API calls. Each request recalculates the theme mode based on the current time of day:

- **light** – 8:30 AM to 6:30 PM
- **dark** – 7:00 PM to 10:59 PM
- **darker** – 11:00 PM through 8:29 AM

### Client

The client page (template `index.html`) loads two JavaScript files:

- `theme.js` handles clicking the moon icon to cycle between modes. When manually toggled, it suppresses automatic theme updates until the page reloads.
- `update.js` calls `/api` once per minute and updates the time, temperature, weather summary and 4‑day forecast. If manual mode isn’t active it also updates the theme class on the `<body>` element.

The CSS uses flexbox and large font sizes so the display looks good on small screens. Forecast information is shown in cards with simple hover effects.

## Adding an API Key

The application requires a free [Pirate Weather](https://pirateweather.net/) API key. Place the key in a `.env` file as shown above. When the server starts it loads this file via `python-dotenv`.

## Running on a Raspberry Pi

On a Raspberry Pi you can install the dependencies using the same `pip` command. Run the server with `python app.py` and open the device’s browser to `http://localhost:5000`. Set the browser to full screen (usually `F11`) for the best effect.

