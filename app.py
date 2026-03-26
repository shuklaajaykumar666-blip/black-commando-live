import streamlit as st
import pandas as pd
import time

# --- पेज सेटिंग और थीम ---
st.set_page_config(page_title="🛡️ मिशन: ब्लैक कमांडो", layout="wide", initial_sidebar_state="expanded")

# --- कस्टम CSS (ब्लैक कमांडो डार्क थीम) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1a1c24; padding: 15px; border-radius: 10px; border: 1px solid #4B5563; }
    </style>
    """, unsafe_allow_name_with_display=True)

st.title("🛡️ मिशन: ब्लैक कमांडो - द नर्व सेंटर (V1.0)")

# --- साइडबार: API और रिस्क कंट्रोल ---
st.sidebar.header("🔐 कंट्रोल टॉवर")
broker = st.sidebar.selectbox("API सोर्स चुनें", ["Dhan HQ", "Fyers (Coming Soon)"])
vix_level = st.sidebar.number_input("India VIX", value=14.50, step=0.01)

if vix_level > 18:
    st.sidebar.error("⚠️ HIGH VOLATILITY ALERT: रिस्क कम करें!")
else:
    st.sidebar.success("✅ MARKET STABLE: ट्रेडिंग ज़ोन")

# --- LAYER 1: MULTI-INDEX INTEL (Core Indices) ---
st.subheader("🏛️ कोर इंडेक्स (Spot + Future + OI)")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("NIFTY 50", "22,450.20", "+0.45%", help="Spot Price")
    st.caption("OI: Long Build-up 🟢")
with c2:
    st.metric("BANK NIFTY", "47,850.10", "-0.12%", help="Spot Price")
    st.caption("OI: Short Covering 🟡")
with c3:
    st.metric("NIFTY IT", "36,200.55", "+1.20%", help="Spot Price")
    st.caption("OI: Strong Long 🟢")

st.divider()

# --- LAYER 2: GLOBAL RADAR & HEAVYWEIGHTS ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🌐 ग्लोबल रडार (Futures)")
    g1, g2 = st.columns(2)
    g1.metric("NASDAQ 100 FUT", "18,250.00", "+0.80%")
    g2.metric("DOW JONES FUT", "39,120.50", "+0.15%")
    
    st.subheader("⚖️ कोरिलेशन लॉजिक (Correlation)")
    # यहाँ आपका दिया गया लॉजिक काम करेगा
    nasdaq_status = "Green" # उदाहरण के लिए
    nifty_it_status = "Green"
    if nasdaq_status == "Red" and nifty_it_status == "Red":
        st.error("📉 BEARISH SENTIMENT: Nasdaq और IT दोनों दबाव में हैं।")
    else:
        st.info("🔄 SENTIMENT: ग्लोबल मार्केट से सपोर्ट मिल रहा है।")

with col_right:
    st.subheader("🐘 द पावर पिलर्स (Weights)")
    stocks = {
        "RELIANCE": "2,950.00 (+1.1%)",
        "HDFC BANK": "1,450.50 (-0.5%)",
        "ICICI BANK": "1,080.20 (+0.3%)",
        "INFOSYS": "1,520.00 (+2.1%)",
        "TCS": "3,950.40 (+1.4%)"
    }
    for stock, price in stocks.items():
        st.write(f"**{stock}:** `{price}`")

# --- LAYER 3: BUYER-SELLER PRESSURE (OI DATA) ---
st.divider()
st.subheader("🔥 बायर-सेलर दबाव (Sentiment Meter)")
pressure = st.slider("Market Pressure (Bearish to Bullish)", 0, 100, 65)
if pressure > 60:
    st.success(f"BULLS ARE IN CONTROL ({pressure}%)")
else:
    st.warning(f"BEARS ARE FIGHTING BACK ({100-pressure}%)")

st.info("📢 राजा साहब, डेटा हर 1 सेकंड में रिफ्रेश होने के लिए तैयार है। API कनेक्ट होते ही ये नंबर्स लाइव नाचेंगे।")