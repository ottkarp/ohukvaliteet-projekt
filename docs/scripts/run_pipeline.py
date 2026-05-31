import urllib.request
import json
import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        port=os.environ.get("DB_PORT", "5432"),
        user=os.environ.get("DB_USER", "praktikum"),
        password=os.environ.get("DB_PASSWORD", "praktikum"),
        dbname=os.environ.get("DB_NAME", "praktikum"),
    )

def ingest_data():
    print("Tõmban andmed API-st...")
    # Tallinna koordinaadid, küsime PM2.5 andmeid
    url = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=59.437&longitude=24.7536&hourly=pm2_5"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
    
    times = data["hourly"]["time"]
    pm25_values = data["hourly"]["pm2_5"]
    
    conn = get_connection()
    cur = conn.cursor()
    
    print("Salvestan andmebaasi (staging)...")
    for i in range(len(times)):
        if pm25_values[i] is not None:
            cur.execute("""
                INSERT INTO staging.air_quality_raw (location_name, forecast_time, pm2_5)
                VALUES (%s, %s, %s)
                ON CONFLICT (location_name, forecast_time) DO UPDATE 
                SET pm2_5 = EXCLUDED.pm2_5
            """, ("Tallinn", times[i], pm25_values[i]))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Andmed salvestatud!")

def transform_data():
    print("Arvutan mõõdikuid (transform)...")
    conn = get_connection()
    cur = conn.cursor()
    
    # Kustutame vana info ja arvutame uue: mitu tundi oli PM2.5 üle 15 (WHO piir)
    cur.execute("""
        TRUNCATE TABLE mart.daily_air_quality;
        
        INSERT INTO mart.daily_air_quality (location_name, forecast_date, max_pm2_5, bad_air_hours)
        SELECT 
            location_name,
            forecast_time::date AS forecast_date,
            MAX(pm2_5) AS max_pm2_5,
            SUM(CASE WHEN pm2_5 > 15 THEN 1 ELSE 0 END) AS bad_air_hours
        FROM staging.air_quality_raw
        GROUP BY location_name, forecast_time::date;
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("Mõõdikud arvutatud!")

if __name__ == "__main__":
    ingest_data()
    transform_data()
    print("Kogu toru töötas edukalt!")
