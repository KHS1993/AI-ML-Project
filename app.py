from datetime import datetime
import os

import requests
import streamlit as st


API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/predict",
)


# --------------------------------------------------
# Sidkonfiguration
# --------------------------------------------------

st.set_page_config(
    page_title="Energiprediktion AI",
    page_icon="⚡",
    layout="centered",
)


# --------------------------------------------------
# Anpassad CSS
# --------------------------------------------------

st.markdown(
    """
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
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Rubrik
# --------------------------------------------------

st.title("⚡ Energiprediktion för Bostad")

st.markdown(
    "Justera värdena nedan för att simulera miljö- och "
    "rumsvärden och beräkna energianvändningen med AI."
)


# --------------------------------------------------
# Formulär
# --------------------------------------------------

with st.form("prediction_form"):
    st.subheader("🏠 Interaktiva Mätvärden")

    col1, col2 = st.columns(2)

    with col1:
        t1 = st.slider(
            "🌡️ Temperatur i kök (°C)",
            min_value=10.0,
            max_value=35.0,
            value=21.0,
            step=0.5,
        )

        rh_1 = st.slider(
            "💧 Luftfuktighet i kök (%)",
            min_value=10.0,
            max_value=90.0,
            value=35.0,
            step=1.0,
        )

        t_out = st.slider(
            "🌤️ Utomhustemperatur (°C)",
            min_value=-10.0,
            max_value=35.0,
            value=10.0,
            step=0.5,
        )

    with col2:
        t2 = st.slider(
            "🌡️ Temperatur i vardagsrum (°C)",
            min_value=10.0,
            max_value=35.0,
            value=20.0,
            step=0.5,
        )

        rh_2 = st.slider(
            "💧 Luftfuktighet i vardagsrum (%)",
            min_value=10.0,
            max_value=90.0,
            value=40.0,
            step=1.0,
        )

        rh_out = st.slider(
            "💧 Luftfuktighet utomhus (%)",
            min_value=0.0,
            max_value=100.0,
            value=75.0,
            step=1.0,
        )

    selected_date = st.date_input(
        "📅 Datum",
        value=datetime.now().date(),
    )

    selected_time = st.time_input(
        "🕒 Tid",
        value=datetime.now().time().replace(
            second=0,
            microsecond=0,
        ),
    )

    submitted = st.form_submit_button(
        "Beräkna energiförbrukning 🚀"
    )


# --------------------------------------------------
# Skicka input till FastAPI
# --------------------------------------------------

if submitted:
    selected_datetime = datetime.combine(
        selected_date,
        selected_time,
    )

    # Samma tidsfeatures som modellen tränades med
    hour = selected_datetime.hour
    day_of_week = selected_datetime.weekday()
    is_weekend = int(day_of_week in [5, 6])

    input_data = {
        "T1": t1,
        "RH_1": rh_1,
        "T2": t2,
        "RH_2": rh_2,
        "T_out": t_out,
        "RH_out": rh_out,
        "hour": hour,
        "day_of_week": day_of_week,
        "is_weekend": is_weekend,
    }

    with st.spinner("Skickar data till AI-modellen..."):
        try:
            response = requests.post(
                API_URL,
                json=input_data,
                timeout=10,
            )

            response.raise_for_status()

            result = response.json()

            prediction = result["prediction"]
            unit = result["unit"]

            st.success("Beräkning klar!")

            st.metric(
                label="Beräknad energianvändning",
                value=f"{prediction:.2f} {unit}",
            )

        except requests.exceptions.RequestException:
            st.error(
                "Kunde inte ansluta till backend. "
                "Kontrollera att FastAPI-servern är igång och försök igen."
    )