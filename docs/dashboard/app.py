import streamlit as st
import pandas as pd
import psycopg2
import os
import altair as alt

st.title("Õhukvaliteedi näidikulaud (Tallinn)")
st.write("Näitab, mitu tundi päevas ületab PM2.5 tase WHO soovitust (15 µg/m³).")

def get_data():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        port=os.environ.get("DB_PORT", "5432"),
        user=os.environ.get("DB_USER", "praktikum"),
        password=os.environ.get("DB_PASSWORD", "praktikum"),
        dbname=os.environ.get("DB_NAME", "praktikum"),
    )
    df = pd.read_sql_query("SELECT * FROM mart.daily_air_quality ORDER BY forecast_date", conn)
    conn.close()
    return df

try:
    df = get_data()
    if not df.empty:
        # Teeme lihtsa tulpdiagrammi
        chart = alt.Chart(df).mark_bar(color='red').encode(
            x=alt.X('forecast_date:T', title='Kuupäev'),
            y=alt.Y('bad_air_hours:Q', title='Halva õhu tunde päevas'),
            tooltip=['forecast_date', 'bad_air_hours', 'max_pm2_5']
        ).properties(height=400)
        
        st.altair_chart(chart, use_container_width=True)
        
        st.subheader("Andmetabel")
        st.dataframe(df)
    else:
        st.warning("Andmebaas on tühi. Palun käivita andmetoru skript!")
except Exception as e:
    st.error(f"Viga andmebaasiga ühendumisel: {e}")
