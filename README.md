# 🌍 Real-Time Disaster Alert System for India

## 📌 Overview
The **Real-Time Disaster Alert System for India** is a web-based application that provides real-time updates on natural disasters, including **Earthquakes, Floods, Cyclones, and Wildfires** in India. The system integrates **GDACS API** to fetch live disaster data and visualizes historical disaster trends using an interactive dashboard.

## 🚀 Features
- **📊 Dynamic Dashboard**: Displays disaster trends, statistics, and key insights.
- **🌍 Interactive Map**: Uses **Folium & Geopandas** to visualize disaster-prone areas in India.
- **📅 Historical Data Analysis**: Filters and analyzes past disaster events.
- **🔴 Live Disaster Alerts**: Fetches real-time data from **GDACS API**.
- **📉 Time-Series Analysis**: Disaster trends over time using **Plotly**.
- **📨 Notification System**: Sends **SMS & Email Alerts** using **Twilio** and **SMTP**.
- **📥 Data Export**: Allows users to download filtered disaster data in CSV format.

## 📦 Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python
- **APIs**: GDACS API, Twilio API
- **Libraries**: Pandas, Plotly, Folium, Geopandas, Requests, SMTP
- **Data Storage**: CSV-based historical disaster dataset

## 🛠️ Installation & Setup
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/real-time-disaster-alert.git
cd real-time-disaster-alert
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables
Create a `.env` file and add the following details:
```ini
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
SMTP_SERVER=your_smtp_server
SMTP_PORT=your_smtp_port
SMTP_USERNAME=your_smtp_username
SMTP_PASSWORD=your_smtp_password
```

### 4️⃣ Run the Application
```sh
streamlit run app.py
```

## 📍 Usage
1. Select the disaster type and date range using sidebar filters.
2. View disaster trends using **line charts, bar charts, and key metrics**.
3. Explore live disaster data on an **interactive Folium map**.
4. Enable alerts by entering **phone number or email**.
5. Download filtered data in CSV format.


## 🤝 Acknowledgments
- **[GDACS API](https://www.gdacs.org/)** for real-time disaster data.
- **[Streamlit](https://streamlit.io/)** for UI development.
- **[Folium & Geopandas](https://geopandas.org/)** for geospatial visualization.
- **[Twilio API](https://www.twilio.com/)** for SMS notifications.

💡 *Feel free to contribute, report issues, or suggest enhancements!* 🚀

