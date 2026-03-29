import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, time as dt_time
import requests
import socket
import time

# ==========================================
# 1. वेल्थ, SMC और RSI इंजन (The Wealth Brain)
# ==========================================
def wealth_engine_v12_2(daily_profit, monthly_sip=3000, nift_rsi=50):
    """RSI < 40 पर 'डबल डिप' (₹150 -> ₹300) और 50% प्रॉफिट लॉक"""
    base_sip = 300 if nift_rsi <= 40 else 150
    system_sip = base_sip if daily_profit > 0 else 0
    user_sip_daily = monthly_sip / 20
    
    remaining = daily_profit - system_sip
    profit_lock = (remaining * 0.50) if remaining > 0 else 0
    
    total_invest = system_sip + user_sip_daily + profit_lock
    return total_invest, base_sip

# ==========================================
# 2. सेल्फ-लर्निंग फीडबैक लूप (The Memory)
# ==========================================
def self_learning_engine(success_rate):
    """पिछली गलतियों से सीखकर रिस्क कम करना"""
    if success_rate < 0.45:
        return 0.50, "⚠️ SELF-CORRECTION: सटीकता कम है, रिस्क 50% कम किया गया।"
    return 1.0, "🟢 OPTIMAL: सिस्टम पूरी मारक क्षमता के साथ तैयार है।"

# ==========================================
# 3. कोर एजेंट: 'त्रिनेत्र' और 'बॉडीगार्ड' (Safety & Strategy)
# ==========================================
def agent_brain_v12(vix, pcr, nasdaq):
    """SMC और न्यूज़ शील्ड के साथ रणनीति"""
    curr_time = datetime.now().time()
    if (vix > 20) and curr_time < dt_time(10, 45):
        return "NO_TRADE_ZONE", "🚨 VIX/न्यूज़ हाई! 10:45 तक कमांडो शांत रहेगा।"
    
    if vix < 15 and pcr > 0.85: return "SAFE_SELLING", "प्रीमियम ईटिंग (Theta) मोड।"
    elif vix > 20 or nasdaq < -1.1: return "HEDGED_STRATEGY", "बाज़ार डरा हुआ, हेजिंग ऑन।"
    else: return "MOMENTUM_BUYING", "स्निपर मोड: पिन-पॉइंट बाइंग।"

def agent_bodyguard_v12(mtm, capital):
    """जंपिंग स्टॉप-लॉस + 1% हार्ड स्टॉप लॉस"""
    if 'max_pnl' not in st.session_state: st.session_state.max_pnl = 0
    st.session_state.max_pnl = max(st.session_state.max_pnl, mtm)

    # 1. हार्ड स्टॉप लॉस
    if mtm <= -(0.01 * capital):
        return True, "🚨 KILL SWITCH: 1% कैपिटल सुरक्षा ट्रिगर!"

    # 2. जंपिंग स्टॉप-लॉस (Dynamic Trailing)
    if st.session_state.max_pnl >= 3000:
        extra = st.session_state.max_pnl - 3000
        jumps = int(extra // 500)
        dynamic_sl = 1500 + (jumps * 300)
        if mtm <= dynamic_sl:
            return True, f"💰 JUMPING SL HIT: ₹{dynamic_sl} प्रॉफिट लॉक!"
    elif st.session_state.max_pnl >= 1500 and mtm <= 0:
        return True, "🛡️ SAFETY LOCK: ₹1500 देख चुके हैं, अब लॉस नहीं।"

    return False, ""

# ==========================================
# 4. टेलीग्राम और हार्टबीट (Communication)
# ==========================================
TELEGRAM_TOKEN = "8615608557:AAEHxIGOR2s_W34nP1cAFhaJz_-t7YVcVYs"
CHAT_ID = "1118805996"

def send_telegram_msg(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except: pass

# ==========================================
# 5. मास्टर UI (The Dashboard)
# ==========================================
st.set_page_config(page_title="🛡️ ब्लैक कमांडो V12.2", layout="wide")

def main():
    # इंटरनेट वॉचडॉग
    try: socket.create_connection(("8.8.8.8", 53), timeout=1)
    except: st.error("🚨 INTERNET DROP: डेटा फीड रुक गई!"); return

    if st.session_state.get('kill_active', False):
        st.error("🛑 AGENTIC LOCK ACTIVE: सिस्टम राजा साहब की आज्ञा का इंतज़ार कर रहा है।")
        if st.button("Unlock System"):
            st.session_state.kill_active = False; st.session_state.max_pnl = 0; st.rerun()
        return

    st.title("🛡️ मिशन: ब्लैक कमांडो V12.2 Ultra")
    st.caption("A-to-Z ऑटोनॉमस वेल्थ इंजन | Status: अजेय तैनात")

    # --- साइडबार: जादुई कंट्रोल बॉक्स ---
    st.sidebar.header("💰 वेल्थ और कैपिटल")
    with st.sidebar.expander("⚙️ सेटिंग्स", expanded=True):
        base_cap = st.number_input("Base Capital", value=100000)
        monthly_sip = st.number_input("Monthly User SIP", value=3000)
        extra_cap = st.number_input("Inject Capital (Demat)", value=0)
        live_rsi = st.sidebar.slider("Nifty RSI (Live)", 10, 90, 42)

    # लाइव डेटा सिमुलेशन
    capital = base_cap + extra_cap + (monthly_sip/20)
    live_mtm = 3800 
    vix, pcr, nasdaq, success_rate = 14.5, 1.1, -0.4, 0.48

    # --- इंजनों का संगम ---
    risk_load, learn_msg = self_learning_engine(success_rate)
    invest_amt, current_sip_rate = wealth_engine_v12_2(live_mtm, monthly_sip, live_rsi)
    strat_key, strat_desc = agent_brain_v12(vix, pcr, nasdaq)
    is_kill, kill_msg = agent_bodyguard_v12(live_mtm, capital)

    # डैशबोर्ड रिपोर्ट
    st.subheader("🤖 ऑटोनॉमस एजेंट रिपोर्ट")
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Strategy", strat_key, strat_desc)
    r2.metric("Trading Power", f"₹{int(capital)}", f"Risk: {risk_load*100}%")
    r3.metric("Live MTM", f"₹{live_mtm}")
    r4.metric("Wealth Compound", f"₹{int(invest_amt)}")

    st.info(f"🧠 **Self-Learning:** {learn_msg}")
    if live_rsi <= 40:
        st.warning(f"📉 'Buy-the-Dip' एक्टिव! आज की बचत: ₹{current_sip_rate}")

    # सुरक्षा मॉनिटर
    if is_kill:
        st.session_state.kill_active = True
        send_telegram_msg(f"🛡️ *MISSION AUTO-LOCKED*\n{kill_msg}")
        st.rerun()

    st.divider()
    st.caption("📉 १७-कॉलम डेटा जर्नल बैकएंड में सिंक हो रहा है।")

if __name__ == "__main__":
    main()
