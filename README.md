# Appliances Energy Prediction

## Appliances Energy Prediction

This student project was created to explore a complete machine learning workflow, from data analysis and model training to model evaluation, backend integration, frontend interaction and automated testing.

The project uses the **Appliances Energy Prediction** dataset from the UCI Machine Learning Repository.

The main question explored in the project is:

> Can indoor climate, outdoor climate and time-based information be used to estimate household appliance energy consumption?

The target variable is:

`Appliances`

and represents appliance energy consumption measured in **Wh**.

Because the target is a continuous numerical value, this is a **regression problem**.

---

## Dataset

Source:

[UCI Machine Learning Repository – Appliances Energy Prediction](https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction)

The dataset contains:

- 19,735 observations
- measurements recorded every 10 minutes
- indoor temperature measurements
- indoor relative humidity measurements
- outdoor weather measurements
- appliance energy consumption

The data covers approximately four and a half months.

Our initial exploratory data analysis showed:

- no missing values
- no identical duplicate rows
- measurements ordered chronologically
- 10-minute intervals between observations

The exploratory analysis can be found in:

`notebooks/01_eda.ipynb`

---

## Target and model features

### Target

The model predicts:

| Target | Description | Unit |
|---|---|---|
| `Appliances` | Appliance energy consumption | Wh |

### Features used by the final model

The final model uses nine features:

| Feature | Description | Unit / format |
|---|---|---|
| `T1` | Indoor temperature | °C |
| `RH_1` | Indoor relative humidity | % |
| `T2` | Indoor temperature | °C |
| `RH_2` | Indoor relative humidity | % |
| `T_out` | Outdoor temperature | °C |
| `RH_out` | Outdoor relative humidity | % |
| `hour` | Hour of day | 0–23 |
| `day_of_week` | Day of week | 0–6, Monday = 0 |
| `is_weekend` | Weekend indicator | 0 or 1 |

The features `hour`, `day_of_week` and `is_weekend` are created from the original timestamp.

The model does **not** use every column from the original dataset.

---

## Data split

Because the dataset is time ordered, the observations were not randomly shuffled.

The dataset was divided chronologically:

| Split | Percentage | Observations | Purpose |
|---|---:|---:|---|
| Train | 70% | 13,814 | Train the models |
| Validation | 15% | 2,960 | Compare models and select configuration |
| Test | 15% | 2,961 | Final evaluation |

The oldest observations were used for training and the newest observations were reserved for testing.

This was chosen to better represent a real-world scenario where a model is trained on historical observations and then used on later data.

---

## Baseline

A simple baseline was created before comparing the machine learning models.

The baseline always predicts the mean appliance energy consumption from the training set:

`98.78 Wh`

The purpose of the baseline is to determine whether the machine learning models actually provide an improvement over a simple reference method.

---

## Models evaluated

The following regression models were evaluated:

- Baseline
- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor

The main evaluation metrics were:

- **MAE – Mean Absolute Error**
- **RMSE – Root Mean Squared Error**
- **R² – Coefficient of determination**

Lower MAE and RMSE values are better.

Higher R² values are better.

---

## Validation results

All models were trained on the same training period and evaluated on the same validation period.

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Baseline | 53.97 Wh | 92.39 Wh | -0.003 |
| Linear Regression | 53.70 Wh | 91.05 Wh | 0.026 |
| **Decision Tree** | **49.03 Wh** | **90.77 Wh** | **0.032** |
| Random Forest | 59.42 Wh | 102.82 Wh | -0.243 |

The Decision Tree produced the best validation results among the tested models.

---

## Overfitting analysis

An unrestricted Decision Tree initially showed severe overfitting.

The model achieved almost perfect performance on the training data but performed much worse on the validation period.

Different values of `max_depth` were therefore tested.

| max_depth | Train MAE | Validation MAE |
|---:|---:|---:|
| 3 | 55.23 Wh | 50.91 Wh |
| 5 | 52.96 Wh | 52.88 Wh |
| 7 | 49.75 Wh | **49.03 Wh** |
| 10 | 40.64 Wh | 49.67 Wh |

Based on the validation results, the selected model was:

```python
DecisionTreeRegressor(
    max_depth=7,
    random_state=42,
)
```

For the selected Decision Tree:

| Metric | Train | Validation |
|---|---:|---:|
| MAE | 49.75 Wh | 49.03 Wh |
| RMSE | 91.23 Wh | 90.77 Wh |
| R² | 0.271 | 0.032 |

Random Forest showed much stronger overfitting:

| Metric | Train | Validation |
|---|---:|---:|
| MAE | 11.64 Wh | 59.42 Wh |
| RMSE | 24.58 Wh | 102.82 Wh |
| R² | 0.947 | -0.243 |

---

## Final test results

After model selection, the selected Decision Tree was evaluated on the reserved test period.

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Baseline | **52.83 Wh** | **90.89 Wh** | approximately 0 |
| Decision Tree | 83.97 Wh | 146.93 Wh | -1.614 |

Although the Decision Tree performed best on the validation data, it performed significantly worse than the baseline on the later test period.

This means that the current model has **not demonstrated stable generalization to later unseen data**.

The model should therefore be considered a first experimental model rather than a production-ready system.

More detailed evaluation can be found in:

`docs/model_evaluation.md`

---

## Distribution shift

One possible contributing factor to the weaker test performance was a change in the input data distribution.

Average outdoor temperature (`T_out`) changed between the splits:

| Split | Mean T_out |
|---|---:|
| Train | 5.72 °C |
| Validation | 8.22 °C |
| Test | 14.51 °C |

The later test period was therefore considerably warmer than the training period.

This is an example of **distribution shift**.

The analysis does not prove that outdoor temperature alone caused the worse test performance, but it demonstrates that the model was evaluated under different conditions than much of its training data.

---

# Application architecture

The project includes a complete Proof of Concept where the trained model can be used through a web interface.

The prediction flow is:

```text
User
  ↓
Streamlit
  ↓
POST /predict
  ↓
FastAPI
  ↓
model_service.py
  ↓
Saved Decision Tree model
  ↓
Prediction in Wh
  ↓
FastAPI response
  ↓
Streamlit
```

The model is **not retrained when a prediction is requested**.

Instead, the already trained model is loaded and reused.

---

## Saved model

The selected Decision Tree is saved using Joblib:

```text
models/decision_tree_model.joblib
```

The saved model allows the application to make predictions without running the training process again.

Important model-related files:

| File | Responsibility |
|---|---|
| `train.py` | Trains, evaluates and saves the model |
| `models/decision_tree_model.joblib` | Saved trained Decision Tree |
| `src/model_config.py` | Defines model path, features, feature order and units |
| `src/model_service.py` | Loads the model, validates features and makes predictions |
| `verify_saved_model.py` | Verifies that the saved model can be used without retraining |

The project also verifies that predictions remain identical before and after saving/loading the model.

More information can be found in:

`docs/model_usage.md`

---

# Backend

The backend is built with **FastAPI**.

Important endpoints include:

| Endpoint | Purpose |
|---|---|
| `GET /health` | Verify that the backend is running |
| `GET /test-db` | Verify the database connection |
| `GET /test-table` | Verify access to the database table |
| `POST /predict` | Make an energy prediction using the saved model |

FastAPI automatically validates prediction input using Pydantic.

If a required feature is missing, the API rejects the request instead of sending incomplete input to the model.

Swagger documentation is available while the backend is running at:

```text
http://127.0.0.1:8000/docs
```

---

# Frontend

The frontend is built with **Streamlit**.

The user can enter:

- indoor temperature
- indoor humidity
- outdoor temperature
- outdoor humidity
- date
- time

Streamlit automatically converts the selected date and time into:

- `hour`
- `day_of_week`
- `is_weekend`

The input is then sent to FastAPI through the `/predict` endpoint.

The returned prediction is displayed in **Wh**.

The frontend also handles backend connection errors and displays a user-friendly error message instead of crashing.

---

# Database

The project uses:

- PostgreSQL
- Supabase
- SQLAlchemy

The database is used to store project data.

Database-related files are located in:

```text
database/
```

The application stores sensitive database connection information in a local `.env` file.

Real credentials must never be committed to GitHub.

An example configuration is provided in:

```text
.env.example
```

---

# Automated tests

The project uses **Pytest** for automated testing.

The current test suite covers:

### Model tests

- saved model can be loaded
- expected model features are defined
- model can make a prediction
- missing required feature is rejected

### Database tests

- CSV data can be read
- imported values are converted correctly
- database import flow behaves as expected

### API tests

- `/health`
- `/test-db`
- `/test-table`
- `/predict`
- missing prediction feature validation

Latest verified result:

```text
10 passed
0 failed
```

Some dependency deprecation warnings may still appear, but they do not currently cause test failures.

Tests can be run with:

```bash
python -m pytest -v
```

---

# Proof of Concept

The complete prediction flow was manually verified.

Different Streamlit inputs produced different model predictions, confirming that the old hardcoded demo result had been replaced by the real saved model.

The same input was also tested through both Swagger and Streamlit.

Example:

```text
Swagger:
54.489092996555684 Wh

Streamlit:
54.49 Wh
```

The difference is only display rounding in Streamlit.

This verifies that both interfaces use the same backend prediction logic.

More information can be found in:

`docs/poc_redovisning.md`

---

# Technology stack

The project uses:

- **Python** – main programming language
- **Pandas** – data handling
- **NumPy** – numerical operations
- **scikit-learn** – machine learning models and metrics
- **Joblib** – saving and loading the trained model
- **Matplotlib** – data visualization
- **Jupyter Notebook** – exploratory data analysis
- **PostgreSQL** – relational database
- **Supabase** – hosted PostgreSQL database
- **SQLAlchemy** – database access
- **FastAPI** – backend API
- **Streamlit** – frontend
- **Pytest** – automated testing
- **Git** – version control
- **GitHub** – repository, Issues and Pull Requests
- **Visual Studio Code** – development environment

---

# Project structure

```text
appliances-energy-prediction/
├── app.py
├── train.py
├── verify_saved_model.py
├── requirements.txt
├── README.md
├── .env.example
│
├── data/
│   ├── energydata_complete.csv
│   └── README.md
│
├── database/
│   ├── FastAPI.py
│   ├── connection.py
│   ├── db_test.py
│   └── load_csv.py
│
├── docs/
│   ├── model_evaluation.md
│   ├── model_usage.md
│   └── poc_redovisning.md
│
├── models/
│   └── decision_tree_model.joblib
│
├── notebooks/
│   └── 01_eda.ipynb
│
├── src/
│   ├── model_config.py
│   └── model_service.py
│
└── tests/
    ├── test_api.py
    ├── test_database.py
    └── test_model_service.py
```

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/KHS1993/appliances-energy-prediction.git
cd appliances-energy-prediction
```


## 2. Create a virtual environment

Windows Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

---

## 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

## 4. Configure environment variables

Copy:

```text
.env.example
```

to:

```text
.env
```

On Git Bash:

```bash
cp .env.example .env
```

Add a valid PostgreSQL connection string:

```text
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
```

The real `DATABASE_URL` must be shared privately and must never be committed to GitHub.

---

# Running the project

The backend and frontend run as two separate processes.

## Start FastAPI

Open the first terminal:

```bash
python -m uvicorn database.FastAPI:app --reload --host 127.0.0.1 --port 8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Start Streamlit

Open a second terminal.

Activate the same virtual environment:

```bash
source .venv/Scripts/activate
```

Then run:

```bash
python -m streamlit run app.py
```

The Streamlit application will open in the browser.

---

# Clean clone verification

The project has been tested from a completely new clone.

The test included:

- cloning the repository into a new directory
- creating a new virtual environment
- installing `requirements.txt`
- creating `.env` from `.env.example`
- starting FastAPI
- starting Streamlit
- making a real prediction

The project could therefore be started without relying on files from the original development environment.

---

# Git workflow

The project uses a branch-based workflow:

```text
feature branch
      ↓
     dev
      ↓
    main
```

Development work is completed in feature branches and reviewed through Pull Requests before being merged into `dev`.

The final stable version is merged from `dev` into `main`.

GitHub Issues were used to divide the project into smaller tasks.

---

# Limitations

The current model has several important limitations:

- Decision Tree performed better than the baseline on validation data but worse on the later test period.
- The model has not demonstrated stable generalization to unseen future periods.
- The dataset represents one building and one limited time period.
- Distribution shift was observed between the training and test periods.
- The model should not be considered production ready.

Future experiments could investigate:

- more representative training data
- additional time-based validation periods
- TimeSeriesSplit
- additional feature engineering
- stronger regularization
- alternative models
- lagged energy consumption features where appropriate

Future model improvements should be evaluated as new experiments rather than being tuned directly against the already inspected test period.

---

# Documentation

Additional project documentation:

- `docs/model_evaluation.md` – model comparison and evaluation
- `docs/model_usage.md` – saved model usage
- `docs/poc_redovisning.md` – Proof of Concept and integration flow
- `notebooks/01_eda.ipynb` – exploratory data analysis

---

# Group members

- Kifle / KHS1993
- Zhaneta Lecini / Zhaneta-Lecini
- Gustav Fransson / Chim-Cham
- Samir Polozen / samirpolozen