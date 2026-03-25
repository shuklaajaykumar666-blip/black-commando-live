import streamlit as st
import requests

st.set_page_config(page_title="ब्लैक कमांडो लाइव", layout="wide")

st.title("🛡️ मिशन: ब्लैक कमांडो - धन (Dhan) लाइव")

# तिजोरी से चाबियाँ निकालना
client_id = st.secrets["dhan_client_id"]
access_token = st.secrets["dhan_access_token"]

# धन से असली भाव मंगाने का फंक्शन
def get_live_price(security_id, exchange_segment):
    url = "https://api.dhan.co/marketfeed/ltp"
    headers = {
        'access-token': access_token,
        'Content-Type': 'application/json'
    }
    data = {
        "instruments": [{"exchangeSegment": exchange_segment, "securityId": security_id}]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()['data'][0]['lastPrice']
    except:
        return "0.00"

# डैशबोर्ड लेआउट
st.success(f"राजा साहब, धन (ID: {client_id}) से लाइव डेटा आ रहा है!")

col1, col2 = st.columns(2)

# Nifty 50 (ID: 13) और Bank Nifty (ID: 25) के भाव
with col1:
    nifty_price = get_live_price("13", "IDX_I")
    st.metric(label="NIFTY 50", value=nifty_price, delta="LIVE")

with col2:
    bn_price = get_live_price("25", "IDX_I")
    st.metric(label="BANK NIFTY", value=bn_price, delta="LIVE")

# पेज को हर 5 सेकंड में खुद अपडेट करने के लिए
st.button("डाटा रिफ्रेश करें")