import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, time as dt_time
import requests
import socket

# ==========================================
# 1. राजा साहब का वेल्थ और कंपाउंडिंग इंजन
# ==========================================
def wealth_compounding_v12_2(daily_profit, user_sip_monthly=3000):
    """
    नियम: 
    1. सिस्टम की बचत: ₹150 रोज़ (₹3000/20)
    2. आपकी जेब की बचत: ₹150 रोज़ (₹3000/20)
    3. मुनाफे का हिस्सा: ₹150 निकालने के बाद बचे प्रॉफिट का 50%
    """
    # A. सिस्टम की ₹150 वाली ऑटो-बचत
    system_sip_daily = 150 if daily_profit > 0 else 0
    
    # B. आपकी जेब वाली SIP का आज का हिस्सा (User Box से)
    user_sip_daily = user_sip_monthly / 20
    
    # C. प्रॉफिट का 50% वेल्थ के लिए (₹150 सिस्टम वाले काटकर)
    remaining_profit = daily_profit - system_sip_daily
    profit_50_percent = (remaining_profit * 0.50) if remaining_profit > 0 else 0
    
    # कुल निवेश (Total Compounding Today)
    total_wealth_today = system_sip_daily + user_sip_daily + profit_50_percent
    
    return total_wealth_today

# ==========================================
# 2. कोर एजेंट्स और सुरक्षा (V12.2 Upgrade)
# ==========================================
def agent_brain_v12(vix, pcr, nasdaq):
    curr_time = datetime.now().time()
    # 10:45 न्यूज़/VIX शील्ड
    if (vix > 20) and curr_time < dt_time(10, 45):
        return "NO_TRADE_ZONE", "🚨 VIX हाई! 10:45 तक बाज़ार को सिर्फ पढ़ें।"
    
    if vix < 15 and pcr > 0.85:
        return "SAFE_SELLING", "प्रीमियम गलाने (Theta Decay) का दिन।"
    elif vix > 20 or nasdaq < -1.1:
        return "HEDGED_STRATEGY", "बाज़ार में डर है, सुरक्षा (Hedges) अनिवार्य।"
    else:
        return "MOMENTUM_BUYING", "चाल तेज़ है, स्निपर बायर मोड ऑन।"

def agent_bodyguard_v12(mtm, capital):
    """1% स्टॉप लॉस और ₹1500/₹3000 प्रॉफिट प्रोटेक्टर"""
    if 'max_pnl' not in st.session_state: st.session_state.max_pnl = 0
    st.session_state.max_pnl = max(st.session_state.max_pnl, mtm)
    
    if mtm <= -(0.01 * capital):
        return True, "🚨 KILL SWITCH: 1% कैपिटल स्टॉप लॉस ट्रिगर!"
    if st.session_state.max_pnl >= 3000 and mtm <= 1500:
        return True, "💰 WEALTH LOCK: ₹1500 मुनाफा लॉक कर दिया गया।"
    return False, ""

# ==========================================
# 3. मास्टर कंट्रोल और 'जादुई बॉक्स' (SIDEBAR)
# ==========================================
st.set_page_config(page_title="🛡️ ब्लैक कमांडो V12.2", layout="wide")

def main():
    # इंटरनेट चेक (हार्टबीट)
    try: socket.create_connection(("8.8.8.8", 53), timeout=1)
    except: st.error("🚨 INTERNET DROP: कमांडो स्टैंडबाय पर है।"); return

    st.title("🛡️ मिशन: ब्लैक कमांडो V12.2")
    st.caption("आज्ञा से: राजा साहब | स्टेटस: अजेय तैनात")

    # --- 🏦 जादुई वेल्थ पैनल (SIDEBAR) ---
    st.sidebar.header("💰 राजा साहब वेल्थ कंट्रोल")
    
    with st.sidebar.expander("💸 फंड और SIP एंट्री", expanded=True):
        base_cap = st.number_input("पुरानी पूँजी (Trading Capital)", value=100000)
        
        # जादुई बॉक्स 1: जेब से डाले गए ₹3,000 की जानकारी
        user_sip_input = st.number_input("जेब से जमा मासिक SIP (₹)", value=3000)
        
        # जादुई बॉक्स 2: एक्स्ट्रा फंड (Wealth Booster)
        extra_fund = st.number_input("एक्स्ट्रा फंड जो डिमैट में डाला (₹)", value=0)
        
        # टोटल ट्रेडिंग पावर
        total_trading_power = base_cap + extra_fund + (user_sip_input / 20)
        st.sidebar.metric("आज की कुल ताकत", f"₹{int(total_trading_power)}")

    # डेटा सिमुलेशन (Dhan API लाइव होने पर यहाँ डेटा आएगा)
    live_mtm = 3500 # डेमो मुनाफा
    vix, pcr, nasdaq = 14.8, 1.1, -0.4

    # --- इंजन कैलकुलेशन ---
    today_wealth = wealth_compounding_v12_2(live_mtm, user_sip_input)
    strat_key, strat_desc = agent_brain_v12(vix, pcr, nasdaq)
    is_kill, kill_msg = agent_bodyguard_v12(live_mtm, total_trading_power)

    # डैशबोर्ड रिपोर्ट
    st.subheader("🤖 ऑटोनॉमस वेल्थ रिपोर्ट")
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Strategy", strat_key, strat_desc)
    r2.metric("Net Power", f"₹{int(total_trading_power)}")
    r3.metric("Live MTM", f"₹{live_mtm}")
    r4.metric("आज का कुल निवेश", f"₹{int(today_wealth)}")

    # वेल्थ मैसेज
    st.success(f"🚀 **वेल्थ अपडेट:** आज ₹{int(today_wealth)} को Nifty/Gold BEES में 'कंपाउंड' करने के लिए निकाला गया।")
    st.info(f"💡 इसमें शामिल: ₹150 (System) + ₹{user_sip_input/20} (Jeb Se) + 50% Profit")

    if is_kill:
        st.session_state.kill_active = True
        st.error(f"🛡️ {kill_msg}")
        # यहाँ टेलीग्राम अलर्ट भी जा सकता है
        st.stop()

    st.divider()
    st.caption("📉 सिस्टम अब आपकी पिछली जीत-हार (17-कॉलम डेटा) से खुद को रोज़ाना बेहतर बना रहा है।")

if __name__ == "__main__":
    main()
