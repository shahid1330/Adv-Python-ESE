import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
from datetime import datetime
import requests
import smtplib
from twilio.rest import Client
import geopandas as gpd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# Page Configuration
st.set_page_config(page_title="Real-Time Disaster Alert System for India", layout="wide")

# Title and Header
st.title("🌍 Real-Time Disaster Alert System for India")
st.header("Track Earthquakes, Floods, Cyclones, and Wildfires")
st.markdown("""
    This app provides real-time updates on natural disasters in India. 
    Data is sourced from **GDACS API**.
""")

# Load Dataset
@st.cache_data
def load_data():
    # Replace this with your dataset file path or URL
    data = pd.read_csv("E:/Christ University/Trimester 3/Advanced Python/Code/ETE Assignment/Natural_Disasters_in_India .csv")  # Update with your dataset file name
    
    # Clean the Date column
    data['Date'] = data['Date'].str.replace('–', '-')  # Replace en dash with hyphen
    data['Date'] = data['Date'].str.strip()  # Remove extra spaces
    
    # Convert to datetime, coercing invalid dates to NaT
    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d', errors='coerce')
    
    # Drop rows with invalid dates
    data = data.dropna(subset=['Date'])
    
    # Clean the Duration column
    # Convert text-based durations to numeric values (e.g., "4 May" -> 4)
    data['Duration'] = pd.to_numeric(data['Duration'].str.extract(r'(\d+)')[0], errors='coerce')
    
    return data

data = load_data()

# Fetch Live Disaster Data from GDACS API
def fetch_live_disaster_data():
    try:
        # GDACS API endpoint for global disaster data
        response = requests.get("https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH")
        disaster_data = response.json()
        return disaster_data
    except Exception as e:
        st.error(f"Failed to fetch live disaster data: {e}")
        return None

live_disaster_data = fetch_live_disaster_data()

# Filter disaster data for India
if live_disaster_data:
    india_disasters = [
        event for event in live_disaster_data['features']
        if event['properties']['country'] == 'India'  # Filter for India
    ]
else:
    india_disasters = []

# Sidebar Filters
st.sidebar.header("Filters")
disaster_type = st.sidebar.selectbox("Select Disaster Type", ["All", "Earthquake", "Flood", "Cyclone", "Wildfire"])
start_date = st.sidebar.date_input("Start Date", data['Date'].min())
end_date = st.sidebar.date_input("End Date", data['Date'].max())

# Filter Data
filtered_data = data[
    (data['Date'] >= pd.to_datetime(start_date)) &
    (data['Date'] <= pd.to_datetime(end_date))
]

# Filter by Disaster Type
if disaster_type != "All":
    filtered_data = filtered_data[filtered_data['Disaster_Info'].str.contains(disaster_type, case=False)]

# Display Metrics
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Disasters", len(filtered_data))
col2.metric("Most Recent Disaster", filtered_data['Date'].max().strftime('%Y-%m-%d'))
col3.metric("Longest Duration", f"{filtered_data['Duration'].max()} days")
col4.metric("Average Duration", f"{filtered_data['Duration'].mean():.2f} days")

# Dynamic Dashboard - Time-Series Visualization
st.subheader("Disaster Frequency Over Time")
time_series_data = filtered_data.resample('D', on='Date').size().reset_index(name='count')
fig = px.line(time_series_data, x='Date', y='count', title="Daily Disaster Frequency")
st.plotly_chart(fig)

# Disaster Type Distribution
st.subheader("Disaster Type Distribution")
disaster_type_counts = filtered_data['Disaster_Info'].value_counts().reset_index()
disaster_type_counts.columns = ['Disaster Type', 'Count']
fig2 = px.bar(disaster_type_counts, x='Disaster Type', y='Count', title="Disaster Type Distribution")
st.plotly_chart(fig2)

# Map of India with Live Disaster Data
st.subheader("Live Disaster Map of India")
st.markdown("Visualize natural disasters on the map of India.")

# Create Folium Map of India
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)  # Centered on India

# Add live disaster markers to the map
if india_disasters:
    for event in india_disasters:
        if 'geometry' in event and len(event['geometry']['coordinates']) > 0:
            latitude = event['geometry']['coordinates'][1]
            longitude = event['geometry']['coordinates'][0]
            folium.Marker(
                location=[latitude, longitude],
                popup=f"{event['properties']['name']} - {event['properties']['fromdate']}",
                icon=folium.Icon(color='red')
            ).add_to(m)

# Add Heatmap
from folium.plugins import HeatMap
heat_data = [
    [event['geometry']['coordinates'][1], event['geometry']['coordinates'][0]]
    for event in india_disasters
    if 'geometry' in event and len(event['geometry']['coordinates']) > 0
]
if heat_data:
    HeatMap(heat_data).add_to(m)

# Display Map
folium_static(m)

# Geospatial Analysis with Geopandas
st.subheader("Geospatial Analysis")
if india_disasters:
    # Create a GeoDataFrame from the live disaster data
    gdf = gpd.GeoDataFrame(
        [
            {
                "name": event['properties']['name'],
                "date": event['properties']['fromdate'],
                "geometry": gpd.points_from_xy(
                    [event['geometry']['coordinates'][0]],
                    [event['geometry']['coordinates'][1]]
                )[0]
            }
            for event in india_disasters
            if 'geometry' in event and len(event['geometry']['coordinates']) > 0
        ]
    )
    st.write(gdf.head())  # Display Geospatial Data

else:
    st.warning("No live disaster data available for India.")

# Download Button
st.sidebar.markdown("### Download Filtered Data")
st.sidebar.download_button(
    label="Download CSV",
    data=filtered_data.to_csv(index=False).encode('utf-8'),
    file_name="filtered_disaster_data.csv",
    mime="text/csv"
)

# Notification System (SMS/Email)
st.sidebar.header("Notification System")
st.sidebar.markdown("Enter your contact details to receive alerts:")
phone_number = st.sidebar.text_input("Phone Number (with country code, e.g., +91)")
email = st.sidebar.text_input("Email Address")

load_dotenv()

# Twilio Configuration for SMS
TWILIO_ACCOUNT_SID =  os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# SMTP Configuration for Email
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_sms(phone_number, message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return True
    except Exception as e:
        st.error(f"Failed to send SMS: {e}")
        return False

def send_email(email, subject, message):
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            email_message = f"Subject: {subject}\n\n{message}"
            server.sendmail(SMTP_USERNAME, email, email_message)
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

if st.sidebar.button("Send Test Alert"):
    if phone_number or email:
        message = "This is a test alert from the Real-Time Disaster Alert System for India."
        if phone_number:
            if send_sms(phone_number, message):
                st.sidebar.success(f"Test SMS Alert sent to {phone_number}!")
        if email:
            if send_email(email, "Test Alert", message):
                st.sidebar.success(f"Test Email Alert sent to {email}!")
    else:
        st.sidebar.error("Please enter a phone number or email address.")

# Dataset Table at the End
st.subheader("Dataset Table")
st.dataframe(data)  # Display the entire dataset in a table

# About Section
with st.expander("About This App"):
    st.markdown("""
        This app is built using **Streamlit** and integrates real-time disaster data from **GDACS API**.
        - **Libraries Used**: Streamlit, Pandas, Plotly, Folium, Geopandas, Twilio, SMTP.
        - **Features**: Time-series visualizations, dynamic filtering, and key metrics.
    """)

# Spinner for Loading
with st.spinner("Loading real-time data..."):
    st.success("Data loaded successfully!")