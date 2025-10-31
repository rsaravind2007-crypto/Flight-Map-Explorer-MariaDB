import streamlit as st
import mysql.connector
import pandas as pd
import pydeck as pdk
from io import StringIO
from math import radians, cos, sin, asin, sqrt

# -------------------------------
#  Database Connection
# -------------------------------
db_user = st.secrets["db_user"]          
db_password = st.secrets["db_password"]  
db_host = st.secrets["db_host"]          
db_port = int(st.secrets["db_port"])     


def create_connection():
    try:
        conn = mysql.connector.connect(
            user=st.secrets["db_user"],
            password=st.secrets["db_password"],
            host=st.secrets["db_host"],
            port=st.secrets["db_port"],
            database="openflights4"
        )
        return conn

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# -------------------------------
# Create airports table (new structure)
# -------------------------------
def create_airports_table():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS airports (
            airport_id INT PRIMARY KEY,
            name VARCHAR(200),
            city VARCHAR(100),
            country VARCHAR(100),
            iata VARCHAR(10),
            icao VARCHAR(10),
            latitude DOUBLE,
            longitude DOUBLE,
            altitude INT,
            timezone DOUBLE,
            dst CHAR(1),
            tz_database_time_zone VARCHAR(50),
            type VARCHAR(20),
            source VARCHAR(50),
            location POINT NOT NULL,
            SPATIAL INDEX(location)
        );
        """)
    except mysql.connector.Error as e:
        st.error(f"Error creating airports table: {e}")
    finally:
        cursor.close()
        conn.close()

# -------------------------------
#    Insert single airport
# -------------------------------
def insert_airport(airport_id, name, city, country, lat, lon):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        point_wkt = f"POINT({lon} {lat})"
        cursor.execute("""
            INSERT INTO airports (airport_id, name, city, country, iata, icao, latitude, longitude, altitude, timezone, dst, tz_database_time_zone, type, source, location)
            VALUES (%s, %s, %s, %s, NULL, NULL, %s, %s, NULL, NULL, NULL, NULL, 'airport', 'manual', ST_GeomFromText(%s, 4326))
        """, (airport_id, name, city, country, lat, lon, point_wkt))
    except mysql.connector.Error:
        cursor.execute("""
            INSERT INTO airports (airport_id, name, city, country, iata, icao, latitude, longitude, altitude, timezone, dst, tz_database_time_zone, type, source, location)
            VALUES (%s, %s, %s, %s, NULL, NULL, %s, %s, NULL, NULL, NULL, NULL, 'airport', 'manual', ST_GeomFromText(%s))
        """, (airport_id, name, city, country, lat, lon, point_wkt))
    conn.commit()
    cursor.close()
    conn.close()



# -------------------------------
#  Spatial Query For Nearby Airports
# -------------------------------
def airports_within_radius(airport_id, radius_meters):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch source(origin) airport
    cursor.execute("SELECT * FROM airports WHERE airport_id = %s", (airport_id,))
    origin = cursor.fetchone()

    if not origin:
        cursor.close()
        conn.close()
        return None, []

    point = f"POINT({origin['longitude']} {origin['latitude']})"

    try:
        # Try query with SRID
        q = """
        SELECT airport_id, name, city, country, latitude, longitude,
               ST_Distance_Sphere(location, ST_GeomFromText(%s, 4326)) AS distance_m
        FROM airports
        WHERE ST_Distance_Sphere(location, ST_GeomFromText(%s, 4326)) <= %s
          AND airport_id != %s
        ORDER BY distance_m ASC
        """
        cursor.execute(q, (point, point, radius_meters, airport_id))
    except mysql.connector.Error:
        # Fallback for older MariaDB (if no SRID arg)
        q = """
        SELECT airport_id, name, city, country, latitude, longitude,
               ST_Distance_Sphere(location, ST_GeomFromText(%s)) AS distance_m
        FROM airports
        WHERE ST_Distance_Sphere(location, ST_GeomFromText(%s)) <= %s
          AND airport_id != %s
        ORDER BY distance_m ASC
        """
        cursor.execute(q, (point, point, radius_meters, airport_id))

    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return origin, results

# -------------------------------
# ️ Haversine fallback
# -------------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * asin(sqrt(a))

# -------------------------------
#   Streamlit UI
# -------------------------------
st.set_page_config(page_title="Smart Flight Map (MariaDB GIS)", layout="wide", page_icon="✈️")
st.title("🌍 Smart Flight Map — Powered by MariaDB Spatial/GIS Features")
st.markdown("Upload airport data or add manually, then explore the real-time routes using MariaDB’s spatial queries")

create_airports_table()

col1, col2 = st.columns([2, 1])

# Left column: Data load 
col1, col2 = st.columns(2)

with col1:
    st.header("Manage Airport Data")

    st.subheader("Insert Single Airport ✈️ ")
    with st.form("single_insert"):
        s_airport_id = st.number_input("Airport ID", value=1001)
        s_name = st.text_input("Name", value="")
        s_city = st.text_input("City", value="")
        s_country = st.text_input("Country", value="")
        s_lat = st.number_input("Latitude", format="%.6f")
        s_lon = st.number_input("Longitude", format="%.6f")

        submitted = st.form_submit_button("Insert Airport")
        if submitted:
            insert_airport(s_airport_id, s_name, s_city, s_country, s_lat, s_lon)
            st.success(f"✅ Inserted {s_name} successfully!")


# Right column: Explore spatial query 
with col2:
    st.header("Explore Nearby Airports 🔍")
    origin_id = st.number_input("Origin airport_id", min_value=1, value=1001)
    radius_km = st.slider("Radius (km)", 50, 5000, 500, step=50)

    if st.button("Find Nearby Airports"):
        origin, nearby = airports_within_radius(origin_id, radius_km * 1000)
        if not origin:
            st.error("Origin airport not found.")
        else:
            st.success(f"Found {len(nearby)} airports within {radius_km} km of {origin['name']}")
            df = pd.DataFrame(nearby)
            df["distance_km"] = (df["distance_m"] / 1000).round(2)
            st.dataframe(df[["airport_id", "name", "city", "country", "distance_km"]])

            origin_point = [origin["longitude"], origin["latitude"]]
            arcs = [{"from_lon": origin_point[0], "from_lat": origin_point[1],
                     "to_lon": row["longitude"], "to_lat": row["latitude"],
                     "name": row["name"], "airport_id": row["airport_id"]} for row in nearby]

            deck = pdk.Deck(
                initial_view_state=pdk.ViewState(latitude=origin_point[1], longitude=origin_point[0], zoom=3),
                layers=[
                    pdk.Layer("ScatterplotLayer", data=arcs,
                              get_position=["to_lon", "to_lat"], get_color=[255, 140, 0], get_radius=30000),
                    pdk.Layer("ArcLayer", data=arcs,
                              get_source_position=["from_lon", "from_lat"],
                              get_target_position=["to_lon", "to_lat"],
                              get_width=2, get_source_color=[0, 128, 255], get_target_color=[255, 0, 128]),
                    pdk.Layer("ScatterplotLayer", data=[{"lon": origin_point[0], "lat": origin_point[1]}],
                              get_position=["lon", "lat"], get_color=[0, 255, 0], get_radius=40000)
                ],
                tooltip={"text": "{name} (ID: {airport_id})"}
            )
            st.pydeck_chart(deck)

# -------------------------------
#   Footer
# -------------------------------
st.markdown("---")
st.markdown("**Author** — ARAVIND R S , Presented For MariaDB hackathon")






