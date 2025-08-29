# https://api-dashboard.getambee.com/#/

import os
import math
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__, template_folder="templates")

# ---------- Helpers ----------
ZIPPO_BASE = "https://api.zippopotam.us/us/"  # no key needed
NWS_POINTS = "https://api.weather.gov/points/{lat},{lon}"
HEADERS = {"User-Agent": "serindaMain-tests-weather (github.com/project)"}


def get_lat_lon(zip_code: str) -> Optional[Dict[str, float]]:
    try:
        r = requests.get(ZIPPO_BASE + zip_code.strip(), timeout=10)
        if r.status_code != 200:
            return None
        data = r.json()
        places = data.get("places") or []
        if not places:
            return None
        lat = float(places[0]["latitude"])  # strings in API
        lon = float(places[0]["longitude"])  # strings in API
        return {"lat": lat, "lon": lon}
    except Exception:
        return None


def nws_endpoints(lat: float, lon: float) -> Optional[Dict[str, str]]:
    try:
        r = requests.get(NWS_POINTS.format(lat=lat, lon=lon), headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return None
        j = r.json()
        props = j.get("properties", {})
        return {
            "forecast": props.get("forecast"),
            "forecastHourly": props.get("forecastHourly"),
            "forecastGridData": props.get("forecastGridData"),
        }
    except Exception:
        return None


def fetch_json(url: str) -> Optional[Dict[str, Any]]:
    if not url:
        return None
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


# Heat index and wind chill calculations (US units)
# T in F, RH in %, V wind mph

def compute_heat_index_f(T: float, RH: float) -> float:
    # Rothfusz regression
    c1 = -42.379
    c2 = 2.04901523
    c3 = 10.14333127
    c4 = -0.22475541
    c5 = -0.00683783
    c6 = -0.05481717
    c7 = 0.00122874
    c8 = 0.00085282
    c9 = -0.00000199
    HI = (
        c1 + c2 * T + c3 * RH + c4 * T * RH + c5 * T * T + c6 * RH * RH + c7 * T * T * RH + c8 * T * RH * RH + c9 * T * T * RH * RH
    )
    return HI


def compute_wind_chill_f(T: float, V: float) -> float:
    if V < 3:
        return T
    return 35.74 + 0.6215 * T - 35.75 * (V ** 0.16) + 0.4275 * T * (V ** 0.16)


# Pollen: provide stub if no API key
# Optionally use Ambee (X-API-Key env AMBEE_API_KEY) if available. Otherwise return simple message.

def get_pollen(zip_code: str, day: str) -> Dict[str, Any]:
    key = "04717b21c6e6503b87417dcad69d515cd6e4d30c66ee7e61883d42826e205252" # os.getenv("AMBEE_API_KEY")
    if not key:
        return {"source": "stub", "message": "Pollen API key not configured. Set AMBEE_API_KEY to enable live pollen data.", "zip": zip_code, "day": day}
    loc = get_lat_lon(zip_code)
    if not loc:
        return {"error": "Invalid ZIP"}
    lat = loc["lat"]
    lon = loc["lon"]
    # Ambee pollen by lat/lon current and forecast
    base = "https://api.ambeedata.com/latest/pollen/by-lat-lng?lat={lat}&lng={lon}"
    headers = {"x-api-key": key}
    try:
        r = requests.get(base.format(lat=lat, lon=lon), headers=headers, timeout=20)
        if r.status_code != 200:
            return {"error": f"Pollen API error {r.status_code}"}
        j = r.json()
        return {"source": "ambee", "data": j}
    except Exception as e:
        return {"error": str(e)}


# ---------- Flask routes ----------

@app.route("/")
def index():
    zip_code = request.args.get("zip", "")
    action = request.args.get("action")
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    if zip_code and action:
        try:
            if action == "today":
                result = weather_today(zip_code)
            elif action == "week":
                result = weather_week(zip_code)
            elif action == "high_today":
                result = temp_extreme(zip_code, when="today", which="high")
            elif action == "high_tomorrow":
                result = temp_extreme(zip_code, when="tomorrow", which="high")
            elif action == "low_today":
                result = temp_extreme(zip_code, when="today", which="low")
            elif action == "low_tomorrow":
                result = temp_extreme(zip_code, when="tomorrow", which="low")
            elif action == "heat_today":
                result = heat_wind_index(zip_code, when="today", which="heat")
            elif action == "heat_tomorrow":
                result = heat_wind_index(zip_code, when="tomorrow", which="heat")
            elif action == "chill_today":
                result = heat_wind_index(zip_code, when="today", which="chill")
            elif action == "chill_tomorrow":
                result = heat_wind_index(zip_code, when="tomorrow", which="chill")
            elif action == "pollen_today":
                result = get_pollen(zip_code, day="today")
            elif action == "pollen_tomorrow":
                result = get_pollen(zip_code, day="tomorrow")
            elif action == "pollen_week":
                result = get_pollen(zip_code, day="week")
            else:
                error = "Unknown action"
        except Exception as e:
            error = str(e)
    return render_template("index.html", zip_code=zip_code, action=action, result=result, error=error)


@app.route("/api/weather/<action>")
def api_weather(action: str):
    zip_code = request.args.get("zip", "")
    if not zip_code:
        return jsonify({"error": "zip required"}), 400
    if action == "today":
        return jsonify(weather_today(zip_code))
    if action == "week":
        return jsonify(weather_week(zip_code))
    if action == "high_today":
        return jsonify(temp_extreme(zip_code, when="today", which="high"))
    if action == "high_tomorrow":
        return jsonify(temp_extreme(zip_code, when="tomorrow", which="high"))
    if action == "low_today":
        return jsonify(temp_extreme(zip_code, when="today", which="low"))
    if action == "low_tomorrow":
        return jsonify(temp_extreme(zip_code, when="tomorrow", which="low"))
    if action == "heat_today":
        return jsonify(heat_wind_index(zip_code, when="today", which="heat"))
    if action == "heat_tomorrow":
        return jsonify(heat_wind_index(zip_code, when="tomorrow", which="heat"))
    if action == "chill_today":
        return jsonify(heat_wind_index(zip_code, when="today", which="chill"))
    if action == "chill_tomorrow":
        return jsonify(heat_wind_index(zip_code, when="tomorrow", which="chill"))
    return jsonify({"error": "unknown action"}), 400


@app.route("/api/pollen/<when>")
def api_pollen(when: str):
    zip_code = request.args.get("zip", "")
    if not zip_code:
        return jsonify({"error": "zip required"}), 400
    return jsonify(get_pollen(zip_code, day=when))


# ---------- Core logic using NWS ----------


def get_grid_and_periods(zip_code: str) -> Optional[Dict[str, Any]]:
    loc = get_lat_lon(zip_code)
    if not loc:
        return None
    eps = nws_endpoints(loc["lat"], loc["lon"]) or {}
    forecast_url = eps.get("forecast")
    hourly_url = eps.get("forecastHourly")
    if not forecast_url or not hourly_url:
        return None
    forecast = fetch_json(forecast_url) or {}
    hourly = fetch_json(hourly_url) or {}
    return {"forecast": forecast, "hourly": hourly, "lat": loc["lat"], "lon": loc["lon"]}


def weather_today(zip_code: str) -> Dict[str, Any]:
    data = get_grid_and_periods(zip_code)
    if not data:
        return {"error": "Unable to resolve weather for ZIP"}
    periods: List[Dict[str, Any]] = (data["forecast"].get("properties", {}).get("periods") or [])
    if not periods:
        return {"error": "No forecast periods"}
    # NWS daily forecast alternates day/night. Find current containing name with today/tonight or closest
    today = datetime.now().date()
    today_entries = [p for p in periods if (p.get("startTime") and datetime.fromisoformat(p["startTime"].replace("Z", "+00:00")).date() == today)]
    show = today_entries[0] if today_entries else periods[0]
    return {
        "zip": zip_code,
        "day": show.get("name"),
        "shortForecast": show.get("shortForecast"),
        "detailedForecast": show.get("detailedForecast"),
        "temperature": f"{show.get('temperature')} {show.get('temperatureUnit')}",
        "wind": show.get("windSpeed"),
    }


def weather_week(zip_code: str) -> Dict[str, Any]:
    data = get_grid_and_periods(zip_code)
    if not data:
        return {"error": "Unable to resolve weather for ZIP"}
    periods: List[Dict[str, Any]] = (data["forecast"].get("properties", {}).get("periods") or [])
    return {
        "zip": zip_code,
        "periods": [
            {
                "name": p.get("name"),
                "shortForecast": p.get("shortForecast"),
                "temperature": f"{p.get('temperature')} {p.get('temperatureUnit')}",
                "wind": p.get("windSpeed"),
            }
            for p in periods
        ],
    }


def temp_extreme(zip_code: str, when: str, which: str) -> Dict[str, Any]:
    data = get_grid_and_periods(zip_code)
    if not data:
        return {"error": "Unable to resolve weather for ZIP"}
    hourly_periods: List[Dict[str, Any]] = (data["hourly"].get("properties", {}).get("periods") or [])
    if not hourly_periods:
        return {"error": "No hourly data"}
    base_date = datetime.now().date()
    target_date = base_date if when == "today" else (base_date + timedelta(days=1))
    temps = []
    for p in hourly_periods:
        ts = datetime.fromisoformat(p["startTime"].replace("Z", "+00:00")).astimezone()
        if ts.date() == target_date and isinstance(p.get("temperature"), (int, float)):
            temps.append(p["temperature"])
    if not temps:
        return {"error": "No temperatures for target day"}
    value = max(temps) if which == "high" else min(temps)
    return {"zip": zip_code, "day": when, "type": which, "temperatureF": value}


def heat_wind_index(zip_code: str, when: str, which: str) -> Dict[str, Any]:
    data = get_grid_and_periods(zip_code)
    if not data:
        return {"error": "Unable to resolve weather for ZIP"}
    hourly_periods: List[Dict[str, Any]] = (data["hourly"].get("properties", {}).get("periods") or [])
    if not hourly_periods:
        return {"error": "No hourly data"}
    base_date = datetime.now().date()
    target_date = base_date if when == "today" else (base_date + timedelta(days=1))
    indices = []
    for p in hourly_periods:
        ts = datetime.fromisoformat(p["startTime"].replace("Z", "+00:00")).astimezone()
        if ts.date() != target_date:
            continue
        T = p.get("temperature")
        unit = p.get("temperatureUnit", "F")
        RH = p.get("relativeHumidity", {}).get("value") if isinstance(p.get("relativeHumidity"), dict) else None
        wind_str = p.get("windSpeed") or "0 mph"
        # Extract wind speed numeric (may be like "7 mph" or "5 to 10 mph")
        v = 0.0
        try:
            first_token = str(wind_str).split(" ")[0]
            if first_token.isdigit():
                v = float(first_token)
            elif first_token.replace(".", "", 1).isdigit():
                v = float(first_token)
        except Exception:
            v = 0.0
        if T is None:
            continue
        Tf = T if unit == "F" else (T * 9/5 + 32)
        if which == "heat":
            if RH is None:
                continue
            idx = compute_heat_index_f(Tf, RH)
        else:
            idx = compute_wind_chill_f(Tf, v)
        indices.append(idx)
    if not indices:
        return {"error": "Insufficient data for index"}
    # Report worst-case (max heat index, min wind chill)
    value = max(indices) if which == "heat" else min(indices)
    return {"zip": zip_code, "day": when, "type": which, "valueF": round(value, 1)}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
