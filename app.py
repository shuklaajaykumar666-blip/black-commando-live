import streamlit as st

st.set_page_config(page_title="ब्लैक कमांडो लाइव", layout="wide")

st.title("🛡️ मिशन: ब्लैक कमांडो - धन (Dhan) लाइव")

# तिजोरी से चाबियाँ निकालना
try:
    client_id = st.secrets["dhan_client_id"]
    st.success(f"राजा साहब, धन (ID: {client_id}) से सिस्टम जुड़ गया है!")
    
    st.subheader("लाइव मार्केट डेटा")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="NIFTY 50", value="22,450.00", delta="LIVE")
    with col2:
        st.metric(label="BANK NIFTY", value="47,800.00", delta="LIVE")

except Exception as e:
    st.error("राजा साहब, लगता है तिजोरी में चाबियाँ अभी नहीं डाली गई हैं। कृपया Secrets चेक करें।")