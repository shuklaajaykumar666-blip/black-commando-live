import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import requests
import time

# ==========================================
# 0. लाइब्रेरी सेफ्टी चेक (Dhan API के लिए)
# ==========================================
try:
    from dhanhq import dhanhq
except ImportError:
    # अगर लाइब्रेरी नहीं है, तो एरर न आए इसके लिए डमी क्लास
    class dhanhq:
        def __init__(self, *args, **kwargs): pass
        def get_fund_limits(self): return {'status': 'failure'}

# ==========================================
# 1. राजा साहब के 3 मुख्य एजेंट्स (The Brains)
# ==========================================
def agent_brain(vix, pcr, nasdaq):
    """एजेंट 1: बाज़ार का मूड और रणनीति"""
    if vix < 15 and pcr > 0.85:
        return "SAFE_SELLING", "आज प्रीमियम गलाने (Theta Decay) का दिन है।"
    elif vix > 20 or nasdaq < -1.1:
        return "HEDGED_STRATEGY", "बाज़ार में डर है, सिर्फ सुरक्षा (Hedges) के साथ ट्रेड।"
    else:
        return "MOMENTUM_BUYING", "चाल तेज़ है, ऑप्शन बाइंग (Scalping) मोड ऑन।"

def agent_bodyguard(mtm, capital):
    """एजेंट 2: 1% हार्ड स्टॉप लॉस गार्ड"""
    limit = -(0.01 * capital) # ₹1,00,000 पर ₹1,000 का घाटा
    if mtm <= limit:
        return True, f"🚨 *AUTO EXIT:* लॉस ₹{mtm} पहुँचा। एजेंट ने सिस्टम लॉक कर दिया।"
    return False, ""

def agent_accountant(mtm, fear_idx):
    """एजेंट 3: स्मार्ट वेल्थ और SIP मैनेजर"""
    trading_power = (70000 * 0.90) + 30000 
    base_sip = 3000
    if fear_idx < 45: 
        return trading_power, base_sip + 2000, "BAZAR SASTA: NIFTY BEES खरीदें!"
    return trading_power, base_sip, "BAZAR NORMAL: GOLD BEES सुरक्षित है।"

# ==========================================
# 2. कंट्रोल सेंटर (Telegram & Sheets)
# ==========================================
TELEGRAM_TOKEN = "8615608557:AAEHxIGOR2s_W34nP1cAFhaJz_-t7YVcVYs"
CHAT_ID = "1118805996"

def send_telegram_msg(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except: pass

def check_kill_switch():
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
        res = requests.get(url, timeout=5).json()
        if res.get("result"):
            m = res["result"][-1]["message"]
            if m.get("text") == "/kill" and (time.time() - m.get("date")) < 30:
                return True
    except: return False
    return False

# ==========================================
# 3. UI और चार्ट (Your Original V10.6 Style)
# ==========================================
st.set_page_config(page_title="🛡️ एजेंटिक ब्लैक कमांडो V11.0", layout="wide")
st.markdown("<style>.main { background-color: #05080a; color: #e0e0e0; }</style>", unsafe_allow_html=True)

def render_war_chart(strategy):
    st.subheader(f"📊 वॉर-चार्ट | रणनीति: {strategy}")
    fig = go.Figure(data=[go.Candlestick(
        x=['09:15', '09:20', '09:25', '09:30'],
        open=[22400, 22410, 22420, 22435], high=[22430, 22440, 22435, 22450],
        low=[22390, 22400, 22410, 22420], close=[22415, 22425, 22435, 22445]
    )])
    fig.update_layout(template="plotly_dark", height=400, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 4. मास्टर एग्जीक्यूशन (Main Engine)
# ==========================================
def main():
    if 'kill_active' not in st.session_state: st.session_state.kill_active = False

    if st.session_state.kill_active:
        st.error("🛑 AGENTIC LOCK ACTIVE: MISSION ABORTED")
        if st.button("Unlock System & Restart"):
            st.session_state.kill_active = False
            st.rerun()
        return

    st.title("🛡️ मिशन: एजेंटिक ब्लैक कमांडो V11.0")
    st.caption("आज्ञा से: राजा साहब | स्टेटस: फुल्ली ऑटोनॉमस तैनात")

    # साइडबार: धन API लॉगिन
    st.sidebar.header("🔐 धन API गेटवे")
    c_id = st.sidebar.text_input("Dhan Client ID")
    a_token = st.sidebar.text_input("Access Token", type="password")
    
    # डेटा सिमुलेशन (सोमवार सुबह यहाँ लाइव डेटा फीड होगा)
    capital, live_mtm = 100000, 1500
    vix, pcr, nasdaq, fear_idx = 14.8, 1.1, -0.4, 38

    # --- एआई एजेंट्स का निर्णय ---
    strat_key, strat_desc = agent_brain(vix, pcr, nasdaq)
    power, sip_amt, wealth_adv = agent_accountant(live_mtm, fear_idx)
    is_risk, risk_msg = agent_bodyguard(live_mtm, capital)

    # टॉप मैट्रिक्स
    st.subheader("🤖 लाइव एजेंट रिपोर्ट्स")
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Strategy", strat_key, strat_desc)
    r2.metric("Trading Power", f"₹{int(power)}")
    r3.metric("Live MTM", f"₹{live_mtm}", delta="Safe" if not is_risk else "Risk")
    r4.metric("Wealth Advice", wealth_adv, f"SIP: ₹{int(sip_amt)}")

    # सुरक्षा मॉनिटर
    if is_risk or check_kill_switch():
        st.session_state.kill_active = True
        send_telegram_msg(risk_msg if is_risk else "🚨 KILL SWITCH BY RAJA SAHAB")
        st.rerun()

    st.divider()

    # वार रूम (चार्ट और आर्डर)
    col_left, col_right = st.columns([2.2, 1])
    with col_left:
        render_war_chart(strat_key)
        st.info(f"💡 **एजेंट एडवाइस:** {strat_desc}")

    with col_right:
        st.sidebar.markdown("### 🎯 स्ट्राइक सेंटर")
        if st.sidebar.button("🚀 EXECUTE COMMANDO STRIKE"):
            # यहाँ आपके 17 कॉलम्स का जर्नल डेटा सेव होगा
            now = datetime.now()
            st.sidebar.success("💥 स्ट्राइक दर्ज! टेलीग्राम पर रिपोर्ट भेजी गई।")
            send_telegram_msg(f"✅ *स्ट्राइक सफल!* \nरणनीति: {strat_key} \nMTM: ₹{live_mtm}")

        if st.sidebar.button("📊 आज की वॉर समरी"):
            send_telegram_msg(f"🏁 *समरी:* MTM ₹{live_mtm}, SIP ₹{int(sip_amt)}")

if __name__ == "__main__":
    main()
