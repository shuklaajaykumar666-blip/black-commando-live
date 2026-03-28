import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import requests
import time

# ==========================================
# टेलीग्राम सेटिंग्स (राजा साहब का कंट्रोल सेंटर)
# ==========================================
TELEGRAM_TOKEN = "8615608557:AAEHxIGOR2s_W34nP1cAFhaJz_-t7YVcVYs"
CHAT_ID = "1118805996" 

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload)
    except Exception as e:
        pass

def check_telegram_kill_switch():
    """सिर्फ ताज़ा हुक्म मानने की शक्ति (30 सेकंड का फिल्टर)"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
        response = requests.get(url).json()
        if response["result"]:
            last_msg_obj = response["result"][-1]["message"]
            last_msg_text = last_msg_obj.get("text", "")
            last_msg_date = last_msg_obj.get("date", 0) 
            
            # वर्तमान समय (Unix Timestamp)
            current_unix_time = time.time()
            
            # अगर मैसेज '/kill' है और 30 सेकंड से पुराना नहीं है, तभी लॉक होगा
            if last_msg_text == "/kill" and (current_unix_time - last_msg_date) < 30:
                return True
    except:
        return False
    return False

# ==========================================
# ऑटो-अलर्ट और इंजन
# ==========================================
def run_auto_monitor(mtm):
    # 1. स्मार्ट किल स्विच (ताज़ा हुक्म पर ही चलेगा)
    if check_telegram_kill_switch():
        if 'kill_active' not in st.session_state:
            kill_msg = "🚨 *KILL SWITCH ACTIVATED!* \n\nराजा साहब, आपके ताज़ा हुक्म पर सिस्टम लॉक कर दिया गया है।"
            send_telegram_msg(kill_msg)
            st.session_state.kill_active = True

    # 2. स्टॉप लॉस अलर्ट
    if mtm <= -1200:
        if 'sl_alert_sent' not in st.session_state:
            alert_msg = f"🚨 *खतरा! स्टॉप लॉस अलर्ट*\n\n⚠️ राजा साहब, लॉस ₹{mtm} पहुँच गया है।"
            send_telegram_msg(alert_msg)
            st.session_state.sl_alert_sent = True 

    # 3. क्लोजिंग रिपोर्ट
    now = datetime.now()
    if now.hour == 15 and now.minute == 30:
        if 'auto_report_sent' not in st.session_state:
            summary = f"🏁 *ऑटो रिपोर्ट: 3:30 PM*\n💰 MTM: ₹{mtm}"
            send_telegram_msg(summary)
            st.session_state.auto_report_sent = True

# ==========================================
# UI और डिजाइन
# ==========================================
st.set_page_config(page_title="🛡️ ब्लैक कमांडो V10.6", layout="wide")
st.markdown("""<style>.main { background-color: #05080a; color: #e0e0e0; }</style>""", unsafe_allow_html=True)

def update_sheet_automation(tab_name, data_list):
    st.toast(f"✅ {tab_name} अपडेट!")

def render_intelligence_radar():
    st.subheader("🧠 इंटेलिजेंस रडार")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("1H Trend", "BULLISH 🟢")
    c2.metric("PCR", "0.85")
    c3.metric("VIX", "19.5")
    c4.metric("Mood", "32%")
    c5.metric("Nasdaq", "-1.15%")
    return 32, "BULLISH 🟢"

def render_war_chart(master_trend):
    st.subheader(f"📊 वॉर-चार्ट | {master_trend}")
    fig = go.Figure(data=[go.Candlestick(x=['09:15', '09:30'], open=[22400, 22420], high=[22430, 22440], low=[22390, 22410], close=[22415, 22435])])
    fig.update_layout(template="plotly_dark", height=400, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

def render_wealth_portal(mtm, fear_idx):
    st.sidebar.markdown("### 💰 वेल्थ पोर्टल")
    if st.sidebar.button("📥 Deposit SIP (₹3000)"):
        st.sidebar.success("SIP दर्ज!")
    st.sidebar.metric("Target Investment", f"₹{3000 + max(0, mtm*0.5)}")

def render_control_tower(mtm, master_trend, fear_idx):
    st.sidebar.markdown("### 🔐 कंट्रोल टॉवर")
    st.sidebar.metric("LIVE MTM", f"₹{mtm}", delta=f"{mtm-1200}")
    if st.sidebar.button("🚀 EXECUTE COMMANDO STRIKE"):
        send_telegram_msg("🎯 स्ट्राइक सफल!")
    return True

# ==========================================
# MAIN EXECUTION
# ==========================================
def main():
    # किल स्विच चेक
    if st.session_state.get('kill_active', False):
        st.error("🛑 SYSTEM LOCKED BY RAJA SAHAB")
        if st.button("Unlock & Restart System"):
            st.session_state.kill_active = False
            st.rerun()
        return

    st.title("🛡️ मिशन: ब्लैक कमांडो V10.6")
    live_pnl = 1500 
    current_fear, master_trend = render_intelligence_radar() 
    run_auto_monitor(live_pnl)
    
    st.divider()
    col_main, col_side = st.columns([2.2, 1])
    with col_main:
        render_war_chart(master_trend) 
    with col_side:
        if render_control_tower(live_pnl, master_trend, current_fear): 
            render_wealth_portal(live_pnl, current_fear)

if __name__ == "__main__":
    main()
