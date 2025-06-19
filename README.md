# Clock Weather Display

A small Flask application that shows the current time and weather forecast.
The display updates automatically every minute using data from the server so
the clock stays accurate even if the device time drifts.

## Setup

1. Create a `.env` file in the project root with your Pirate Weather API key:

```
PIRATE_WEATHER_API_KEY=your_api_key_here
```

2. Install dependencies:

```
pip install flask python-dotenv requests pytz
```

3. Run the application:

```
python app.py
```

The app will be available on `http://localhost:5000`.
