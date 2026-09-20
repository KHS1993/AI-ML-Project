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

# 2. Skapa ett formulär för inmatning
st.subheader("Mätvärden för bostaden")

with st.form("energy_form"):
    temperature_kitchen = st.number_input("Temperatur i kök (°C)", value=21.0, step=0.1)
    humidity_kitchen = st.number_input("Luftfuktighet i kök (%)", value=35.0, step=0.1)
    temperature_living = st.number_input("Temperatur i vardagsrum (°C)", value=20.0, step=0.1)
    humidity_living = st.number_input("Luftfuktighet i vardagsrum (%)", value=40.0, step=0.1)
    windspeed = st.number_input("Vindhastighet (m/s)", value=2.0, step=0.1)
    visibility = st.number_input("Sikt (km)", value=40.0, step=1.0)

    # Knapp för att skicka iväg prediktionen
    submit_button = st.form_submit_button(label="Beräkna energiförbrukning 🚀")


# 3. Vad som händer när man klickar på knappen (Kopplingen till FastAPI)

if submit_button: #Koden här inne triggas enbart när användaren fyller i värdena och klickar på knappen "Beräkna energiförbrukning

# Förbered datan som ska skickas till FastAPI-servern

#Steg A (input_data):
#Här paketeras alla inmatade siffror från reglagen in i ett rent JSON-format. 
# Variablerna (T1, RH_1 med flera) måste matcha exakt det som er FastAPI-endpoint (i FastAPI.py) förväntar sig att få in i sitt request-schema.
    input_data = {
        "T1": temperature_kitchen,
        "RH_1": humidity_kitchen,
        "T2": temperature_living,
        "RH_2": humidity_living,
        "Windspeed": windspeed,
        "Visibility": visibility
    }

    st.info("Skickar data till AI-modellen...")

    try:
# Anropar FastAPI-servern

#Steg B 
#Det här är själva bryggan mellan Streamlit (frontend) och FastAPI (backend).
        response = requests.post("http://127.0.0.1:8000/predict", json=input_data)

#Steg C (response.json()):
#När FastAPI har tagit emot datan, kört den genom er maskininlärningsmodell och räknat ut ett värde, 
#skickar servern tillbaka ett svar.
        if response.status_code == 200:
            result = response.json()
            predicted_energy = result.get("prediction", 145.50)
            st.success(f"Beräknad energiförbrukning: **{predicted_energy} Wh**")
        else:
            st.error(f"Kunde inte nå API:et. Statuskod: {response.status_code}")

    except Exception as e:
        st.error(f"Kunde inte ansluta till FastAPI-servern. Kontrollera att den är igång! Fel: {e}")
        