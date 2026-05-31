CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS mart;

-- Toorandmete tabel
CREATE TABLE IF NOT EXISTS staging.air_quality_raw (
    location_name text,
    forecast_time timestamp,
    pm2_5 numeric(6, 2),
    PRIMARY KEY (location_name, forecast_time)
);

-- Arvutatud andmete tabel (mitu tundi oli õhk halb)
CREATE TABLE IF NOT EXISTS mart.daily_air_quality (
    location_name text,
    forecast_date date,
    max_pm2_5 numeric(6, 2),
    bad_air_hours integer,
    PRIMARY KEY (location_name, forecast_date)
);
