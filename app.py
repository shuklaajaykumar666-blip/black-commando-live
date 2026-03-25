import streamlit as st
import requests
import json

st.set_page_config(page_title="ब्लैक कमांडो लाइव", layout="wide")
st.title("🛡️ मिशन: ब्लैक कमांडो - धन (Dhan) लाइव")

# तिजोरी से चाबियाँ
access_token = st.secrets["dhan_access_token"]

def get_real_data():
    url = "https://api.dhan.co/marketfeed/ltp"
    headers = {
        'access-token': access_token,
        'Content-Type': 'application/json'
    }
    # Nifty 50 (13) और Bank Nifty (25) के लिए डेटा रिक्वेस्ट
    payload = {
        "instruments": [
            {"exchangeSegment": "IDX_I", "securityId": "13"},
            {"exchangeSegment": "IDX_I", "securityId": "25"}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        res_data = response.json()
        
        # अगर डेटा मिल गया तो भाव निकालो, वरना 0 दिखाओ
        if res_data.get('status') == 'success':
            prices = {item['securityId']: item['lastPrice'] for item in res_data['data']}
            return prices.get('13', "Error"), prices.get('25', "Error")
        else:
            return "Token Expired", "Check API"
    except Exception as e:
        return "Offline", "Offline"

# स्क्रीन पर दिखाना
nifty, banknifty = get_real_data()

col1, col2 = st.columns(2)
with col1:
    st.metric(label="NIFTY 50", value=nifty, delta="LIVE")
with col2:
    st.metric(label="BANK NIFTY", value=banknifty, delta="LIVE")

if st.button("डाटा रिफ्रेश करें"):
    st.rerun()

st.info("नोट: अगर 'Token Expired' दिख रहा है, तो नया Access Token जनरेट करके Secrets में अपडेट करें।")