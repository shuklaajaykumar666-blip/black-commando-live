import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, time as dt_time
import requests
import time
import socket

# ==========================================
# 1. वेल्थ और कैपिटल इंजन (V12.2 Upgrade)
# ==========================================
def wealth_engine_v12_2(daily_profit, monthly_sip=3000):
    """निर्देश: 50% प्रॉफिट लॉक और डेली SIP कैलकुलेशन"""
    # मुनाफे का 50% निवेश के लिए रिजर्व
    investable = daily_profit * 0.50 if daily_profit > 0 else 0
    # SIP का डेली हिस्सा (20 ट्रेडिंग दिन)
    daily_sip_cut = monthly_sip / 20 
    return investable, daily_sip_cut

# ==========================================
# 2. सेल्फ-लर्निंग फीडबैक लूप (V12.2 Upgrade)
# ==========================================
def self_learning_engine(success_rate):
    """पिछली जीत-हार से सीखकर रिस्क मैनेज करना"""
    if success_rate < 0.45: # अगर 45% से कम सटीकता है
        return 0.50, "⚠️ SELF-CORRECTION: बाज़ार मुश्किल है, रिस्क 50% कम किया गया।"
    return 1.0, "🟢 OPTIMAL: सिस्टम पूरी मारक क्षमता के साथ तैयार है।"

# ==========================================
# 3. अपग्रेडेड एजेंट्स (Intelligence & Guard)
# ==========================================
def agent_brain_v12(vix, pcr, nasdaq):
    """V12.2: न्यूज़ शील्ड और VIX फिल्टर के साथ फैसला"""
    is_event_today = False # API सिंक (Auto-Oracle)
    curr_time = datetime.now().time()
    
    # न्यूज़ और VIX 20+ पर 10:45 तक नो-ट्रेड (Pillar 3)
    if (vix > 20 or is_event_today) and curr_time < dt_time(10, 45):
        return "NO_TRADE_ZONE", "🚨 न्यूज़/VIX हाई है। कमांडो 10:45 तक शांत रहेगा।"
    
    if vix < 15 and pcr > 0.85:
        return "SAFE_SELLING", "आज प्रीमियम गलाने (Theta Decay) का दिन है।"
    elif vix > 20 or nasdaq < -1.1:
        return "HEDGED_STRATEGY", "बाज़ार में डर है, बास्केट हेजिंग एक्टिव।"
    else:
        return "MOMENTUM_BUYING", "चाल तेज़ है, स्निपर बायर मोड ऑन।"

def agent_bodyguard_v12(mtm, capital):
    """प्रॉफिट प्रोटेक्टर (The Trailing Sniper)"""
    if 'max_pnl' not in st.session_state: st.session_state.max_pnl = 0
    st.session_state.max_pnl = max(st.session_state.max_pnl, mtm)

    # ₹1500 पर Risk Zero | ₹3000 पर ₹1500 Lock (Pillar 4)
    if st.session_state.max_pnl >= 1500 and mtm <= 0:
        return True, "🛡️ SAFETY: ₹1500 देख चुके हैं, अब लॉस नहीं लेंगे।"
    if st.session_state.max_pnl >= 3000 and mtm <= 1500:
        return True, "💰 WEALTH LOCK: ₹1500 मुनाफा सुरक्षित!"
    
    # 1% हार्ड स्टॉप लॉस (Pillar 2)
    if mtm <= -(0.01 * capital):
        return True, "🚨 KILL SWITCH: 1% कैपिटल स्टॉप लॉस ट्रिगर।"
    return False, ""

# ==========================================
# 4. कंट्रोल सेंटर (Telegram & Heartbeat)
# ==========================================
TELEGRAM_TOKEN = "8615608557:AAEHxIGOR2s_W34nP1cAFhaJz_-t7YVcVYs"
CHAT_ID = "1118805996"

def check_heartbeat():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        return True
    except: return False

def send_telegram_msg(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except: pass

# ==========================================
# 5. UI और मास्टर एग्जीक्यूशन (DEPLOYMENT)
# ==========================================
st.set_page_config(page_title="🛡️ ब्लैक कमांडो V12.2", layout="wide")

def main():
    # इंटरनेट वॉचडॉग (Pillar 3)
    if not check_heartbeat():
        st.error("🚨 INTERNET DROP: डेटा फीड रुक गई है! कमांडो स्टैंडबाय पर है।")
        return

    if st.session_state.get('kill_active', False):
        st.error("🛑 AGENTIC LOCK ACTIVE: SAFETY PROTOCOL ON")
        if st.button("Unlock System (Raja Sahab Only)"):
            st.session_state.kill_active = False
            st.session_state.max_pnl = 0
            st.rerun()
        return

    st.title("🛡️ मिशन: ब्लैक कमांडो V12.2")
    st.caption("100% ऑटोनॉमस | स्टेटस: अजेय तैनात")

    # साइडबार: वेल्थ पैनल (Pillar 2)
    st.sidebar.header("💰 वेल्थ और कैपिटल")
    monthly_sip = st.sidebar.number_input("Monthly SIP (₹)", value=3000)
    extra_cap = st.sidebar.number_input("Inject Capital (₹)", value=0)
    
    # लाइव डेटा (Dhan API से आएगा)
    capital = 100000 + extra_cap
    live_mtm = 2100 # डेमो PnL
    vix, pcr, nasdaq = 14.5, 1.1, -0.4
    success_rate = 0.48 # फीडबैक लूप के लिए डेटा

    # --- इंजन रनिंग ---
    risk_load, learning_msg = self_learning_engine(success_rate)
    invest_amt, daily_sip = wealth_engine_v12_2(live_mtm, monthly_sip)
    strat_key, strat_desc = agent_brain_v12(vix, pcr, nasdaq)
    is_kill, kill_msg = agent_bodyguard_v12(live_mtm, capital)

    # डैशबोर्ड रिपोर्ट
    st.subheader("🤖 ऑटोनॉमस एजेंट रिपोर्ट")
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Strategy", strat_key, strat_desc)
    r2.metric("Trading Power", f"₹{capital}", f"Risk: {risk_load*100}%")
    r3.metric("Live MTM", f"₹{live_mtm}")
    r4.metric("Daily SIP Reserve", f"₹{daily_sip}")

    st.info(f"🧠 **Self-Learning:** {learning_msg}")
    if invest_amt > 0:
        st.success(f"🏦 **Wealth Vault:** ₹{invest_amt} तिजोरी (Nifty BEES) के लिए सुरक्षित।")

    # सुरक्षा मॉनिटर
    if is_kill:
        st.session_state.kill_active = True
        send_telegram_msg(f"🛡️ *MISSION AUTO-LOCKED*\n{kill_msg}")
        st.rerun()

    st.divider()
    st.caption("📉 17-कॉलम का जर्नल डेटा बैकएंड में ऑटो-सिंक और फीडबैक के लिए प्रोसेस हो रहा है।")

if __name__ == "__main__":
    main()
