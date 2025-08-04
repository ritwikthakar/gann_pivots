import streamlit as st
import yfinance as yf
import math
from datetime import date, timedelta

st.title("🧮 Gann Square of 9 Calculator")

# Input
ticker = st.text_input("Enter stock symbol (e.g., SPX, AAPL):", value="QQQ")
selected_date = st.date_input("Pick date for OHLC data:", value=date.today() - timedelta(days=1))
price_type = st.selectbox("Choose price type for base:", ["Close", "High", "Low"])

# Degrees mapped to sqrt steps
angle_steps = {
    "45°": 0.125,
    "90°": 0.25,
    "135°": 0.375,
    "180°": 0.5,
    "225°": 0.625,
    "270°": 0.75,
    "315°": 0.875,
    "360°": 1.0,
}

@st.cache_data
def fetch_ohlc(ticker, selected_date):
    data = yf.download(ticker, start=selected_date - timedelta(days=5), end=selected_date + timedelta(days=1))
    if selected_date.strftime("%Y-%m-%d") in data.index.strftime("%Y-%m-%d"):
        row = data.loc[selected_date.strftime("%Y-%m-%d")]
        return row['High'], row['Low'], row['Close']
    else:
        return None, None, None

def gann_square_of_9(base_price):
    base_sqrt = math.sqrt(base_price)
    levels = {}
    for deg, step in angle_steps.items():
        r_level = round((base_sqrt + step)**2, 2)
        s_level = round((base_sqrt - step)**2, 2)
        levels[f"R {deg}"] = r_level
        levels[f"S {deg}"] = s_level
    return levels

# Logic
if ticker and selected_date:
    high, low, close = fetch_ohlc(ticker, selected_date)

    if high and low and close:
        price = {"Close": close, "High": high, "Low": low}[price_type]
        st.subheader(f"{price_type} Price on {selected_date}: {price:.2f}")
        
        levels = gann_square_of_9(price)

        st.subheader("📊 Gann Square of 9 Levels")
        st.table(levels)
    else:
        st.warning("No trading data found for the selected date.")
