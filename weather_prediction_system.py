import requests
import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import tkinter as tk
from tkinter import messagebox

# ---------------- GLOBAL VARIABLES ----------------
df_actual = None
future_dates = None
predicted_temps = None
city_global = None

# ---------------- MYSQL CONNECTION ----------------
def connect_db():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="weather_db"
        )
        return db, db.cursor()
    except Exception as e:
        messagebox.showerror("DB Error", str(e))
        return None, None

# ---------------- GET LAT / LON ----------------
def get_lat_lon(city):
    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"
    res = requests.get(url, headers={"User-Agent": "weather-app"}, timeout=10)
    data = res.json()
    if not data:
        return None, None
    return float(data[0]["lat"]), float(data[0]["lon"])

# ---------------- CURRENT WEATHER ----------------
def current_weather():
    city = city_entry.get().strip()
    if city == "":
        messagebox.showerror("Error", "Enter city name")
        return

    lat, lon = get_lat_lon(city)
    if lat is None:
        messagebox.showerror("Error", "City not found")
        return

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current_weather=true"
        "&timezone=auto"
    )

    data = requests.get(url).json()
    temp = data["current_weather"]["temperature"]
    wind = data["current_weather"]["windspeed"]

    messagebox.showinfo(
        "Current Weather",
        f"City: {city.title()}\n"
        f"Date: {datetime.now().strftime('%d %b %Y')}\n"
        f"Temperature: {temp} °C\n"
        f"Wind Speed: {wind} km/h"
    )

# ---------------- FETCH + PREDICT ----------------
def run_prediction():
    global df_actual, future_dates, predicted_temps, city_global

    city = city_entry.get().strip()
    if city == "":
        messagebox.showerror("Error", "Enter city name")
        return

    city_global = city
    db, cursor = connect_db()
    if db is None:
        return

    # -------- CREATE TABLES --------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE,
        temperature FLOAT,
        city VARCHAR(50),
        UNIQUE KEY unique_weather (date, city)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predicted_weather (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE,
        temperature FLOAT,
        city VARCHAR(50)
    )
    """)
    db.commit()

    lat, lon = get_lat_lon(city)
    if lat is None:
        messagebox.showerror("Error", "City not found")
        return

    # -------- API CALL --------
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&daily=temperature_2m_mean"
        "&past_days=10"
        "&forecast_days=5"
        "&timezone=auto"
    )

    res = requests.get(url)
    if res.status_code != 200:
        messagebox.showerror("API Error", "Weather API failed")
        return

    data = res.json()
    dates = pd.to_datetime(data["daily"]["time"])
    temps = data["daily"]["temperature_2m_mean"]

    df_api = pd.DataFrame({"date": dates, "temperature": temps})
    today = datetime.now().date()

    # -------- INSERT ACTUAL DATA --------
    for _, row in df_api.iterrows():
        if row["date"].date() <= today:
            cursor.execute(
                """
                INSERT INTO weather_data (date, temperature, city)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE temperature = VALUES(temperature)
                """,
                (row["date"].date(), float(row["temperature"]), city)
            )
    db.commit()

    # -------- FETCH DATA --------
    cursor.execute("""
        SELECT date, temperature
        FROM weather_data
        WHERE city=%s
        ORDER BY date
    """, (city,))
    records = cursor.fetchall()

    if len(records) < 3:
        messagebox.showerror("Error", "Not enough data")
        return

    df_actual = pd.DataFrame(records, columns=["date", "temperature"])
    df_actual["date"] = pd.to_datetime(df_actual["date"])

    # -------- FILL MISSING DATES --------
    all_dates = pd.date_range(
        start=df_actual["date"].min(),
        end=df_actual["date"].max(),
        freq="D"
    )

    df_actual = df_actual.set_index("date").reindex(all_dates)
    df_actual.index.name = "date"
    df_actual["temperature"] = df_actual["temperature"].interpolate()
    df_actual = df_actual.reset_index()

    #️
    # -------- SIMPLE PREDICTION --------
    base = df_actual["temperature"].tail(3).mean()
    last_date = df_actual["date"].max()

    future_dates = []
    predicted_temps = []

    for i in range(1, 4):
        future_dates.append(last_date + timedelta(days=i))
        predicted_temps.append(round(base + i * 0.3, 2))

    cursor.execute("DELETE FROM predicted_weather WHERE city=%s", (city,))
    for d, t in zip(future_dates, predicted_temps):
        cursor.execute(
            """
            INSERT INTO predicted_weather (date, temperature, city)
            VALUES (%s, %s, %s)
            """,
            (d.date(), t, city)
        )
    db.commit()

    messagebox.showinfo("Success", f"Prediction completed for {city.title()}")

# ---------------- LINE GRAPH ----------------
def line_graph():
    if df_actual is None:
        messagebox.showerror("Error", "Run prediction first")
        return

    plt.figure(figsize=(14, 6))
    plt.plot(df_actual["date"], df_actual["temperature"],
             marker="o", label="Actual")
    plt.plot(future_dates, predicted_temps,
             marker="x", linestyle="--", label="Predicted")

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    ax.set_xlim(df_actual["date"].min(), max(future_dates))

    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.title(f"{city_global.title()} Temperature Trend")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ---------------- BAR GRAPH ----------------
def bar_graph():
    if df_actual is None:
        messagebox.showerror("Error", "Run prediction first")
        return

    plt.figure(figsize=(14, 6))
    plt.bar(df_actual["date"], df_actual["temperature"], label="Actual")
    plt.bar(future_dates, predicted_temps, label="Predicted")

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))

    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.title(f"{city_global.title()} Actual vs Predicted Temperature")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Weather Prediction System")
root.geometry("550x500")

tk.Label(root, text="Weather Prediction System",
         font=("Arial", 16, "bold")).pack(pady=20)

tk.Label(root, text="Enter City Name").pack()
city_entry = tk.Entry(root, width=30)
city_entry.pack(pady=5)

tk.Button(root, text="Current Weather (Today)",
          width=30, command=current_weather).pack(pady=10)

tk.Button(root, text="Fetch & Predict",
          width=30, command=run_prediction).pack(pady=10)

tk.Button(root, text="Line Graph",
          width=30, command=line_graph).pack(pady=5)

tk.Button(root, text="Bar Graph",
          width=30, command=bar_graph).pack(pady=5)

root.mainloop()
