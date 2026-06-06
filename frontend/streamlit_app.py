import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="PhishSentinel",
    page_icon="🛡️",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/predict-url"
EXPLAIN_URL = "http://127.0.0.1:8000/explain-url"

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #0f172a;
}
.sub-text {
    font-size: 16px;
    color: #475569;
}
.card {
    padding: 20px;
    border-radius: 16px;
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
}
.result-safe {
    padding: 15px;
    border-radius: 12px;
    background-color: #dcfce7;
    color: #166534;
    font-weight: 700;
}
.result-danger {
    padding: 15px;
    border-radius: 12px;
    background-color: #fee2e2;
    color: #991b1b;
    font-weight: 700;
}
.small-muted {
    color: #64748b;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ PhishSentinel</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-text">AI-Powered Real-Time Phishing URL Detection Dashboard</div><br>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

total_scans = len(st.session_state.history)
malicious_count = sum(1 for x in st.session_state.history if x["label"] == "Malicious")
safe_count = sum(1 for x in st.session_state.history if x["label"] == "Benign")

col1.metric("Total Scans", total_scans)
col2.metric("Safe URLs", safe_count)
col3.metric("Threats Detected", malicious_count)

st.divider()

left, right = st.columns([2, 1])


with left:
    st.markdown("### 🔍 Scan URL")

    url = st.text_input(
        "Enter URL",
        placeholder="https://example.com/login"
    )

    analyze = st.button("Analyze URL", use_container_width=True)

    if analyze:
        if url.strip() == "":
            st.warning("Please enter a valid URL.")
        else:
            try:
                response = requests.post(API_URL, json={"url": url}, timeout=20)
                data = response.json()
                prediction = data.get("prediction", 0)
                label = data.get("label", "Unknown")
                confidence = float(data.get("confidence", 0))
                explain_response = requests.post(
                  EXPLAIN_URL,
                  json={"url": url},
                   timeout=30
                )
                explain_data = explain_response.json()
                explanation = explain_data.get("explanation", "No explanation available.")
                
                
                # Result Banner
                if label == "Malicious":
                   st.markdown(
                       '<div class="result-danger">⚠️ Malicious URL Detected</div>',
                        unsafe_allow_html=True
                     )
                else:
                    st.markdown(
                       '<div class="result-safe">✅ Safe URL</div>',
                        unsafe_allow_html=True
                     )
                # Progress Bar
                st.progress(min(confidence, 1.0))

                # Metrics
                col_a, col_b = st.columns(2)

                with col_a:
                  st.metric("Prediction", label)
                
                with col_b:
                  st.metric("Confidence", f"{confidence*100:.2f}%")
                
                if prediction == 1 and confidence >= 0.80:
                    badge = """
                    <div style='padding:12px;border-radius:12px;
                    background:#fee2e2;color:#991b1b;
                    font-weight:800;text-align:center;'>
                    🔴 HIGH RISK
                    </div>
                    """
                
                elif prediction == 1:
                    badge = """
                    <div style='padding:12px;border-radius:12px;
                    background:#fef3c7;color:#92400e;
                    font-weight:800;text-align:center;'>
                    🟡 MEDIUM RISK
                    </div>
                    """
                
                elif prediction == 0 and confidence >= 0.80:
                    badge = """
                    <div style='padding:12px;border-radius:12px;
                    background:#dcfce7;color:#166534;
                    font-weight:800;text-align:center;'>
                    🟢 LOW RISK
                    </div>
                    """
                else:
                    badge = """
                    <div style='padding:12px;border-radius:12px;
                    background:#e0f2fe;color:#075985;
                    font-weight:800;text-align:center;'>
                    🔵 MEDIUM RISK
                    </div>
                    """
                
                st.markdown("### 🚨 Risk Assessment")
                st.markdown(badge, unsafe_allow_html=True)
                if label == "Malicious":
                  st.markdown("### 🤖 Why was it flagged?")
                  st.info(explanation)


                # Save history
                st.session_state.history.insert(0, {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "url": url,
                    "label": label,
                    "confidence": f"{confidence*100:.2f}%"
                })

            except Exception as e:
                st.error(f"Could not connect to backend API.\n\n{e}")

with right:
    st.markdown("### 📌 Security Tips")

    st.markdown("""
<div class="card">
✔ Check spelling of domains<br><br>
✔ Avoid urgent login links<br><br>
✔ Look for HTTPS certificate<br><br>
✔ Never share OTP/password<br><br>
✔ Verify sender identity
</div>
""", unsafe_allow_html=True)


st.divider()
st.markdown("### 🕘 Recent Scan History")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No scans yet.")

st.markdown("---")
st.caption("Built with Streamlit + FastAPI + Scikit-learn | PhishSentinel")