import streamlit as st
import requests

# Sidkonfiguration
st.set_page_config(
    page_title="Energiprediktion AI",
    page_icon="⚡",
    layout="centered"
)

# Anpassad CSS för snyggare knappar
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Energiprediktion för Bostad")
st.markdown("Justera reglagen nedan för att simulera miljö- och rumsvärden och beräkna energiförbrukningen med AI.")

# Skapa formulär med reglage (sliders) i två kolumner
with st.form("prediction_form"):
    st.subheader("🏠 Interaktiva Mätvärden")
    
    col1, col2 = st.columns(2)
    
    with col1:
        t1 = st.slider("🌡️ Temperatur i kök (°C)", min_value=10.0, max_value=35.0, value=21.0, step=0.5)
        rh_1 = st.slider("💧 Luftfuktighet i kök (%)", min_value=10.0, max_value=90.0, value=35.0, step=1.0)
        windspeed = st.slider("💨 Vindhastighet (m/s)", min_value=0.0, max_value=20.0, value=2.0, step=0.5)
        
    with col2:
        t2 = st.slider("🌡️ Temperatur i vardagsrum (°C)", min_value=10.0, max_value=35.0, value=20.0, step=0.5)
        rh_2 = st.slider("💧 Luftfuktighet i vardagsrum (%)", min_value=10.0, max_value=90.0, value=40.0, step=1.0)
        visibility = st.slider("👁️ Sikt (km)", min_value=0.0, max_value=80.0, value=40.0, step=1.0)

    submitted = st.form_submit_button("Beräkna energiförbrukning 🚀")

if submitted:
    input_data = {
        "T1": t1,
        "RH_1": rh_1,
        "T2": t2,
        "RH_2": rh_2,
        "Windspeed": windspeed,
        "Visibility": visibility
    }

    with st.spinner("Skickar data till AI-modellen..."):
        try:
            response = requests.post("http://127.0.0.1:8000/predict", json=input_data)
            if response.status_code == 200:
                prediction = response.json()["prediction"]
                
                st.success("Beräkning klar!")
                st.metric(label="Beräknad energiförbrukning", value=f"{prediction} Wh")
            else:
                st.error(f"Kunde inte nå API:et. Statuskod: {response.status_code}")
        except Exception as e:
            st.error(f"Ett fel uppstod vid anslutning till backend: {e}")