import streamlit as st
import requests

st.set_page_config(page_title="Sensor Dashboard", layout="centered")
st.title("📟 Dashboard Sensor Ultrasonik")

# Fungsi klasifikasi jarak
def klasifikasi_jarak(jarak):
    if jarak < 20:
        return "🚨 Terlalu Dekat"
    elif jarak <= 100:
        return "✅ Aman"
    else:
        return "📏 Jarak Jauh"

try:
    # Ambil data dari Flask
    response = requests.get("http://localhost:5000/data")
    data = response.json()
    distance = float(data.get("distance", 0))

    # Tampilkan metrik dan klasifikasi AI
    st.metric("📏 Jarak Terdeteksi", f"{distance:.2f} cm")
    st.subheader("🧠 AI Analisis Jarak:")
    st.success(klasifikasi_jarak(distance))

except Exception as e:
    st.error("⚠️ Gagal mengambil data dari server Flask.")
    st.caption(f"Detail error: {e}")
