import streamlit as st
import pandas as pd
import time
import random
import matplotlib.pyplot as plt

# Simulated phishing detection function
def detect_phishing(url):
    phishing_keywords = ['login', 'bank', 'verify', 'account', 'secure', 'update']
    if any(keyword in url.lower() for keyword in phishing_keywords):
        return "Phishing"
    return "Safe"

# Initialize session state if not present
if 'phishing_data' not in st.session_state:
    st.session_state.phishing_data = []

if 'url_simulation' not in st.session_state:
    st.session_state.url_simulation = False

st.title("🔒 Real-Time Phishing Detection & Dashboard")

# URL input form
url = st.text_input("Enter a URL to check:")
if st.button("Check URL"):
    result = detect_phishing(url)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    st.session_state.phishing_data.append({"URL": url, "Status": result, "Timestamp": timestamp})
    st.success(f"URL classified as: {result}")

# Toggle for real-time URL simulation
st.session_state.url_simulation = st.checkbox("Enable Real-Time URL Simulation")
if st.session_state.url_simulation:
    simulated_urls = ["login-example.com", "secure-bank.net", "random-site.org", "update-password.io"]
    if random.random() < 0.3:  # 30% chance of new URL every refresh
        new_url = random.choice(simulated_urls)
        result = detect_phishing(new_url)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        st.session_state.phishing_data.append({"URL": new_url, "Status": result, "Timestamp": timestamp})

# Convert session state data to DataFrame
phishing_df = pd.DataFrame(st.session_state.phishing_data)

# Real-time dashboard
st.subheader("📊 Live Phishing Analysis")
st.dataframe(phishing_df)

# Statistics & Metrics
if not phishing_df.empty:
    phishing_count = phishing_df[phishing_df['Status'] == "Phishing"].shape[0]
    safe_count = phishing_df[phishing_df['Status'] == "Safe"].shape[0]
    
    st.metric("Total Phishing URLs", phishing_count)
    st.metric("Total Safe URLs", safe_count)
    
    # Bar chart visualization
    chart_data = pd.DataFrame({
        "Category": ["Phishing", "Safe"],
        "Count": [phishing_count, safe_count]
    })
    st.bar_chart(chart_data.set_index("Category"))
    
    # Line chart for trend over time
    phishing_df['Timestamp'] = pd.to_datetime(phishing_df['Timestamp'])
    phishing_trend = phishing_df.groupby(phishing_df['Timestamp'].dt.strftime('%H:%M:%S'))['Status'].value_counts().unstack().fillna(0)
    st.line_chart(phishing_trend)
    
    # Pie Chart
    fig, ax = plt.subplots()
    ax.pie([phishing_count, safe_count], labels=["Phishing", "Safe"], autopct='%1.1f%%', colors=['red', 'green'])
    ax.set_title("Phishing vs Safe URLs")
    st.pyplot(fig)
    
    # Threat Level Indicator
    threat_level = (phishing_count / max(1, len(phishing_df))) * 100  # Normalize threat level
    st.progress(int(threat_level))
    st.write(f"Threat Level: {int(threat_level)}%")
    
# Auto-refresh every 5 seconds
st.experimental_rerun()
