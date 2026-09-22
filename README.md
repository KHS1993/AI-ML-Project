# AI-ML-Project

This is student project for us to learn the process of machine learning. Main goal of this project was to create a simpler training model that once taught would be able to use information from a dataset to predict pattern or answer a certain form of question. For out project we chose a dataset that recorded the energy usage and the average humidity/temprature of rooms in a building over a longer period of time. With this data we wanted to set the question to be: "Can we predict the energy usage of a building just from the amount of appliances in said buulding but also the average temprature and humidity.

### Dataset
https://archive.ics.uci.edu/dataset/374/appliances%2Benergy%2Bprediction?utm_source=chatgpt.com 

### Upplägg

Vi delade datasetet i tidsordning:

- De första 70 procenten användes för träning.
- Nästa 15 procent användes för validering och modellval.
- De sista 15 procenten användes för sluttest.

Modellerna använder temperatur, luftfuktighet och tidsinformation
för att uppskatta `Appliances`.

Vi jämförde modellerna med MAE, alltså det genomsnittliga absoluta
felet. Felet anges i Wh. Lägre MAE är bättre.

### Resultat på valideringsdata

| Modell | MAE (Wh) |
|---|---:|
| Baseline: träningsdatans medelvärde | 53,97 |
| Linear Regression | 53,70 |
| Decision Tree, max_depth=7 | 49,03 |
| Random Forest | 59,42 |

Decision Tree med `max_depth=7` hade lägst fel på valideringsdatan.
Därför valdes den modellen för sluttestet.

### Resultat på testdata

Vi jämförde den valda modellen och samma baseline på testperioden.

| Modell | MAE (Wh) |
|---|---:|
| Baseline: träningsdatans medelvärde | 52,83 |
| Decision Tree, max_depth=7 | 83,97 |

### Targets and Features
Listed below we have our targets and features used from the dataset:

|**Targets:**|
|:--------|
|Appliances|

|**Features:**|
|:--------|
|date|
|lights|
|T1|
|RH_1|
|T2|
|RH_2|
|T3|
|RH_3|
|T|
|RH_4|
|T5|
|RH_5|
|T6|
|RH_6|
|T7|
|RH_7|
|T8|
|RH_8|
|T|
|RH_9|
|T_out|
|Press_mm_hg|
|RH_out|
|Windspeed|
|Visibility|
|Tdewpoint|
|rv1|
|rv|

## Teknikstack
The following is the programs/tools we used during the development of this app:
- Python
- Jupyter Notebook
- Visual Studio Code
- PostgreSQL
- Streamlit
- Git
- Github

## Project Structure

```
AI-ML-Project
├── .venv/
├── data/
    ├── .gitkeep
    ├── energydata_complete.csv
    └── README.md
├── database/
    ├── __pychache__ 
    ├── .gitkeep
    ├── connection.py
    └── FastAPI.py
├── models/
    └── .gitkeep 
├── notebooks/
    └── .gitkeep 
├── src/
    └── .gitkeep 
├── .env
├── .gitignore
├── app.py
├── README.md
└── requirments.txt

```

## Installation
```
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt

```

## How to run
```
Start Frontend:
python -m streamlit run app.py

Start Backend:
uv run uvicorn database.FastAPI:app --reload

Open app in webbrowser:
Network URL: http://192.168.1.124:8501

```

### Slutsats och begränsningar

Descision Tree preformed better than the baseline on the validation 
data, but performed worse on the later testperiods.

Therefor we have not shown that the chosen model gives better 
prediction than our more simple baseline during the testperiod.

Testperiod had higher outside temperature than the trainings period.
It is a possible contributing factor, but the analysis doesnt 
prove that the temprature explains the models bigger errors.

Detta är resultatet för vår första modellversion. Eventuella
fortsatta förbättringar ska dokumenteras som nya experiment.

This is the result of our first modelversion. Eventual continued 
improvments will be documented as new experiements.


### Group Members
- Kifle / KHS1993
- Zhaneta Lecini / Zhaneta-Lecini
- Gustav Fransson / Chim-Cham
- Samir Polozen / samirpolozen
