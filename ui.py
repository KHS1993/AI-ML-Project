import streamlit as st
import requests

# 1. Sidans utseende
st.set_page_config(
    page_title="EnergiPrediktion - AI",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ Energi- och Apparatförbrukning")
st.write("Här kan du mata in miljö- och husvärden för att uppskatta energiförbrukningen med hjälp av vår tränade AI-modell.")

# 2. Skapa ett formulär för inmatning (Inputs baserade på features från datasetet)
st.subheader("Mätvärden för bostaden")

with st.form("energy_form"):
    # Vi delar upp i kolumner för snyggare design
    col1, col2 = st.columns(2)
    
    with col1:
        temperature_kitchen = st.number_input("Temperatur i kök (°C)", value=21.0, step=0.1)
        humidity_kitchen = st.number_input("Luftfuktighet i kök (%)", value=35.0, step=0.1)
        temperature_living = st.number_input("Temperatur i vardagsrum (°C)", value=20.0, step=0.1)
        
    with col2:
        humidity_living = st.number_input("Luftfuktighet i vardagsrum (%)", value=40.0, step=0.1)
        windspeed = st.number_input("Vindhastighet (m/s)", value=2.0, step=0.1)
        visibility = st.number_input("Sikt (km)", value=40.0, step=1.0)

    # Knapp för att skicka iväg prediktionen
    submit_button = st.form_submit_button(label="Beräkna energiförbrukning 🚀")

# 3. Vad som händer när man klickar på knappen
if submit_button:
    # Här förbereder vi datan som ska skickas till API:et (FastAPI)
    input_data = {
        "T1": temperature_kitchen,
        "RH_1": humidity_kitchen,
        "T2": temperature_living,
        "RH_2": humidity_living,
        "Windspeed": windspeed,
        "Visibility": visibility
    }
    
    st.info("Skickar data till AI-modellen...")
    
    # Exempel på anrop till FastAPI (när bakgrunden är klar kommer API:et ligga på t.ex. http://127.0.0.1:8000/predict)
    try:
        # response = requests.post("http://127.0.0.1:8000/predict", json=input_data)
        # result = response.json()


        
        
        # Hårdkodat testsvar så länge för att se att gränssnittet ser bra ut:
        fake_result = 145.50 
        
        st.success(f"🔑 Beräknad energiförbrukning: **{fake_result} Wh**")
        
    except Exception as e:
        st.error(f"Kunde inte nå API:et. Kontrollera att FastAPI-servern är igång! Fel: {e}")

        