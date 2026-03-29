import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, time as dt_time
import requests
import socket

# ==========================================
# 1. राजा साहब का स्मार्ट वेल्थ इंजन (RSI Upgrade)
# ==========================================
def wealth_compounding_v12_2(daily_profit, user_sip_monthly=3000, nift_rsi=50):
    """
    अपग्रेड: RSI अगर 40 से नीचे, तो सिस्टम की बचत ₹150 से बढ़कर ₹300 (Double Dip)
    """
    # स्मार्ट RSI चेक (मंदी में ज़्यादा खरीदारी)
    base_system_sip = 300 if nift_rsi <= 40 else 150
    
    # A. सिस्टम की ऑटो-बचत
    system_sip_daily = base_system_sip if daily_profit > 0 else 0
    
    # B. आपकी जेब वाली SIP (₹3000/20)
    user_sip_daily = user_sip_monthly / 20
    
    # C. बचे मुनाफे का 50%
    remaining_profit = daily_profit - system_sip_daily
    profit_50_percent = (remaining_profit * 0.50) if remaining_profit > 0 else 0
    
    total_wealth_today = system_sip_daily + user_sip_daily + profit_50_percent
    return total_wealth_today, base_system_sip

# ==========================================
# 2. जंपिंग स्टॉप-लॉस गार्ड (Dynamic Trailing Upgrade)
# ==========================================
def agent_bodyguard_v12(mtm, capital):
    """
    नया लॉजिक: ₹3000 के बाद हर ₹500 के प्रॉफिट पर SL ₹300 ऊपर खिसकेगा।
    """
    if 'max_pnl' not in st.session_state: st.session_state.max_pnl = 0
    st.session_state.max_pnl = max(st.session_state.max_pnl, mtm)
    
    # हार्ड स्टॉप लॉस (1%)
    if mtm <= -(0.01 * capital):
        return True, "🚨 KILL SWITCH: 1% कैपिटल स्टॉप लॉस!"

    # --- जंपिंग स्टॉप-लॉस (Dynamic Trailing) ---
    if st.session_state.max_pnl >= 3000:
        # ₹3000 पर बेस लॉक ₹1500 है।
        # उसके ऊपर हर ₹500 पर ₹300 का जंप।
        extra_profit = st.session_state.max_pnl - 3000
        jumps = int(extra_profit // 500)
        dynamic_sl = 1500 + (jumps * 300)
        
        if mtm <= dynamic_sl:
            return True, f"💰 JUMPING SL HIT: ₹{dynamic_sl} मुनाफा सुरक्षित!"
            
    # बेसिक लॉक (अगर प्रॉफिट ₹3000 के नीचे है)
    elif st.session_state.max_pnl >= 1500 and mtm <= 0:
        return True, "🛡️ SAFETY: ₹1500 देख चुके हैं, अब लॉस नहीं लेंगे।"

    return False, ""

# ==========================================
# 3. कोर एजेंट्स (VIX & Strategy)
# ==========================================
def agent_brain_v12(vix, pcr, nasdaq):
    curr_time = datetime.now().time()
    if (vix > 20) and curr_time < dt_time(10, 45):
        return "NO_TRADE_ZONE", "🚨 VIX हाई! 10:45 तक बाज़ार को सिर्फ पढ़ें।"
    
    if vix < 15 and pcr > 0.85: return "SAFE_SELLING", "प्रीमियम गलाने का दिन।"
    elif vix > 20 or nasdaq < -1.1: return "HEDGED_STRATEGY", "सुरक्षा अनिवार्य।"
    else: return "MOMENTUM_BUYING", "स्निपर बायर मोड ऑन।"

# ==========================================
# 4. मास्टर UI (Deployment Ready)
# ==========================================
st.set_page_config(page_title="🛡️ ब्लैक कमांडो V12.2", layout="wide")

def main():
    try: socket.create_connection(("8.8.8.8", 53), timeout=1)
    except: st.error("🚨 INTERNET DROP"); return

    st.title("🛡️ मिशन: ब्लैक कमांडो V12.2 (Ultra)")
    
    # --- जादुई बॉक्स (Sidebar) ---
    st.sidebar.header("💰 वेल्थ कंट्रोल")
    with st.sidebar.expander("💸 फंड और RSI सेटिंग", expanded=True):
        base_cap = st.number_input("पुरानी पूँजी", value=100000)
        user_sip_input = st.number_input("जेब से मासिक SIP (₹)", value=3000)
        extra_fund = st.number_input("एक्स्ट्रा फंड (₹)", value=0)
        live_rsi = st.sidebar.slider("Nifty RSI (Live)", 10, 90, 45) # ऑटो फीड होगा
        
        total_power = base_cap + extra_fund + (user_sip_input / 20)
        st.sidebar.metric("आज की कुल ताकत", f"₹{int(total_power)}")

    # डेटा सिमुलेशन
    live_mtm = 5200  # मान लीजिए आज ₹5200 का प्रॉफिट है
    vix, pcr, nasdaq = 14.8, 1.1, -0.4

    # --- इंजन रनिंग ---
    today_wealth, current_sip_rate = wealth_compounding_v12_2(live_mtm, user_sip_input, live_rsi)
    strat_key, strat_desc = agent_brain_v12(vix, pcr, nasdaq)
    is_kill, kill_msg = agent_bodyguard_v12(live_mtm, total_trading_power=total_power)

    # डैशबोर्ड
    st.subheader("🤖 ऑटोनॉमस वेल्थ रिपोर्ट")
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Strategy", strat_key, strat_desc)
    r2.metric("Buying Power", f"₹{int(total_power)}")
    r3.metric("Live MTM", f"₹{live_mtm}")
    r4.metric("Wealth Compound", f"₹{int(today_wealth)}")

    # स्मार्ट अलर्ट्स
    if live_rsi <= 40:
        st.warning(f"📉 RSI {live_rsi} है! 'Buy-the-Dip' एक्टिव: आज बचत ₹150 के बजाय ₹300 हो रही है।")
    
    st.success(f"🚀 **Action:** ₹{int(today_wealth)} कंपाउंडिंग के लिए लॉक। (System: ₹{current_sip_rate})")

    if is_kill:
        st.session_state.kill_active = True
        st.error(f"🛡️ {kill_msg}")
        st.stop()

if __name__ == "__main__":
    main()
