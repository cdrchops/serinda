Weather & Pollen Flask Demo

Location: tests/weather

Run:
- python tests\weather\app.py
- App listens on http://localhost:5001/

Usage:
- Enter a US ZIP code and click any command link to view results in the page.
- API endpoints are also available under /api/weather/* and /api/pollen/*.

Weather data source:
- Zippopotam.us (no key) to resolve ZIP -> lat/lon.
- National Weather Service API (api.weather.gov) for forecast & hourly data (no key). Requires US locations.

Derived values:
- High/Low temperatures for today/tomorrow computed from NWS hourly temperatures.
- Heat index (requires humidity) computed from NWS hourly temperature & relative humidity.
- Wind chill computed from NWS hourly temperature & wind.

Pollen data:
- If environment variable AMBEE_API_KEY is set, app will call Ambee pollen API by lat/lon.
- If not set, the app returns a stub message indicating pollen API is not configured.

Notes:
- Some ZIP codes near borders may have limited data. Errors will be shown in the result panel.
- This is a simple demo intended for test purposes.
