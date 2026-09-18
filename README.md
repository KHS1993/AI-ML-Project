# AI-ML-Project

This is student project for us to learn the process of machine learning. Main goal of this project was to create a simpler training model that once taught would be able to use information from a dataset to predict pattern or answer a certain form of question. For out project we chose a dataset that recorded the energy usage and the average humidity/temprature of rooms in a building over a longer period of time. With this data we wanted to set the question to be: "Can we predict the energy usage of a building just from the amount of appliances in said buulding but also the average temprature and humidity.

### Dataset
https://archive.ics.uci.edu/dataset/374/appliances%2Benergy%2Bprediction?utm_source=chatgpt.com 


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
uv run uvicorn database.FastAPI:app --reload
```

## Result


### Group Members
- Kifle / KHS1993
- Zhaneta Lecini / Zhaneta-Lecini
- Gustav Fransson / Chim-Cham