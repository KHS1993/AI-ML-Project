# Modellutvärdering – Appliances Energy Prediction

## Syfte

Syftet med denna utvärdering är att undersöka hur väl våra
regressionsmodeller kan uppskatta hushållsapparaternas energianvändning.

Vi jämför modellerna både mot varandra och mot en enkel baseline.
Vi undersöker även överanpassning, modellval och hur den valda
modellen fungerar på en senare testperiod.

---

## Problem och target

Projektets target är `Appliances`.

`Appliances` beskriver hushållsapparaternas energianvändning i Wh
under varje mätintervall.

Eftersom target är ett numeriskt värde är detta ett regressionsproblem.

---

## Features

Den första modellen använder följande klimatvariabler:

- `T1`
- `RH_1`
- `T2`
- `RH_2`
- `T_out`
- `RH_out`

För att ge modellerna mer information om när mätningen sker skapade
vi även tre tidsbaserade features från kolumnen `date`:

- `hour` – timmen på dygnet
- `day_of_week` – veckodagen
- `is_weekend` – 1 för lördag/söndag och 0 för vardag

Detta är feature engineering, eftersom nya features skapas från
information som redan finns i datasetet.

---

## Tidsbaserad datauppdelning

Datasetet innehåller tidsordnade observationer.

Vi valde därför att inte blanda observationerna slumpmässigt.
Istället behöll vi tidsordningen och delade datasetet i:

| Datadel | Andel | Observationer | Syfte |
|---|---:|---:|---|
| Train | 70 % | 13 814 | Träna modellerna |
| Validation | 15 % | 2 960 | Jämföra modeller och välja inställningar |
| Test | 15 % | 2 961 | Slutbedöma den valda modellen |

De äldsta observationerna används för träning och de senaste
observationerna används för test.

Det gör utvärderingen mer lik en situation där en modell tränas
på historisk data och sedan används på en senare period.

---

## Baseline

Vi skapade en enkel baseline som alltid gissar samma värde.

Baselinevärdet är medelvärdet av `Appliances` i träningsdatan:

**98,78 Wh**

Baselinen använder alltså inte temperatur, luftfuktighet eller
tidsinformation.

Syftet med baselinen är att kontrollera om våra Machine Learning-
modeller faktiskt tillför något jämfört med en mycket enkel gissning.

---

## Utvärderingsmått

Vi använder MAE, Mean Absolute Error.

MAE beskriver hur stort modellens absoluta fel är i genomsnitt.

Exempel:

Om en modell har:

`MAE = 50 Wh`

betyder det att modellens uppskattningar i genomsnitt ligger ungefär
50 Wh från de verkliga värdena.

Lägre MAE är bättre.

MAE är inte en procentsats.

---

# Modelljämförelse

Vi jämförde följande:

- Baseline
- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor

Alla modeller jämfördes på samma validation-period.

## Resultat på validation

| Modell | Validation MAE |
|---|---:|
| Baseline | 53,97 Wh |
| Linear Regression | 53,70 Wh |
| Decision Tree | **49,03 Wh** |
| Random Forest | 59,42 Wh |

Decision Tree hade lägst MAE på validation-datan och gav därför
det bästa validation-resultatet av de modeller vi testade.

---

# Linear Regression

Linear Regression fick:

**Validation MAE: 53,70 Wh**

Det var endast en liten förbättring jämfört med baselinen:

**Baseline MAE: 53,97 Wh**

Det betyder att Linear Regression inte lyckades utnyttja våra
features särskilt mycket bättre än den enkla baseline-gissningen.

---

# Decision Tree

## Första försöket

Den första versionen av Decision Tree hade inget begränsat träddjup.

Resultaten blev ungefär:

- Train MAE: 0,01 Wh
- Validation MAE: 92,46 Wh

Detta var ett tydligt tecken på overfitting.

Modellen hade nästan memorerat träningsdatan, men fungerade mycket
sämre på validation-datan.

---

## Begränsning av trädet

För att minska overfitting begränsade vi trädets maximala djup
med parametern `max_depth`.

Vi jämförde:

| Max depth | Train MAE | Validation MAE |
|---:|---:|---:|
| 3 | 55,23 Wh | 50,91 Wh |
| 5 | 52,96 Wh | 52,88 Wh |
| 7 | 49,75 Wh | **49,03 Wh** |
| 10 | 40,64 Wh | 49,67 Wh |

`max_depth=7` hade lägst validation-MAE av de värden vi testade.

Därför valde vi:

`DecisionTreeRegressor(max_depth=7, random_state=42)`

som vår Decision Tree-konfiguration.

---

## Train jämfört med validation

Den valda modellen fick:

- Train MAE: 49,75 Wh
- Validation MAE: 49,03 Wh

Resultaten ligger nära varandra.

Det innebär att den tydliga overfitting som fanns i det obegränsade
trädet minskade kraftigt när vi begränsade trädets djup.

---

# Random Forest

Random Forest med 100 träd fick:

- Train MAE: 11,64 Wh
- Validation MAE: 59,42 Wh

Skillnaden mellan train och validation är stor.

Det tyder på att Random Forest lärde sig träningsdatan betydligt
bättre än den kunde generalisera till validation-perioden.

Random Forest fick dessutom sämre validation-MAE än både Decision Tree,
Linear Regression och baselinen.

Därför valdes den inte.

---

# Val av modell

Utifrån validation-resultaten valde vi:

**Decision Tree med `max_depth=7`**

Modellen valdes eftersom den hade lägst validation-MAE bland de
modeller och inställningar vi testade.

Det är viktigt att modellen valdes utifrån validation-datan och
inte utifrån testdatan.

Testdatan sparades till den slutliga utvärderingen.

---

# Sluttest

Efter modellvalet utvärderades Decision Tree på den reserverade
testperioden.

Resultatet blev:

**Decision Tree Test MAE: 83,97 Wh**

Detta var betydligt sämre än modellens validation-resultat:

**Validation MAE: 49,03 Wh**

Modellen generaliserade alltså betydligt sämre till den senare
testperioden.

---

## Jämförelse med baseline på testdata

Vi utvärderade även samma baseline på testperioden.

| Modell | Test MAE |
|---|---:|
| Baseline | **52,83 Wh** |
| Decision Tree | 83,97 Wh |

På testperioden presterade alltså baselinen bättre än vår valda
Decision Tree-modell.

Det betyder att vi inte har visat att Decision Tree ger bättre
prediktioner än den enkla baseline-modellen på den senare testperioden.

---

# Analys av skillnaden mellan tidsperioderna

För att bättre förstå varför testresultatet blev sämre jämförde vi
bland annat utomhustemperaturen `T_out`.

Medelvärden:

| Datadel | Genomsnittlig T_out |
|---|---:|
| Train | 5,72 °C |
| Validation | 8,22 °C |
| Test | 14,51 °C |

Medianen för `T_out` var:

- Train: cirka 5,67 °C
- Validation: cirka 7,55 °C
- Test: cirka 14,30 °C

Testperioden innehåller alltså betydligt varmare väderförhållanden
än träningsperioden.

Detta visar att fördelningen av åtminstone vissa features förändras
mellan tidsperioderna.

Det kan beskrivas som distribution shift.

Det är en möjlig bidragande faktor till det sämre testresultatet,
men analysen visar inte att utomhustemperaturen ensam orsakar
modellens höga testfel.

---

# Slutsats

Decision Tree med `max_depth=7` var den modell som presterade bäst
på validation-datan.

Den slog baselinen på validation:

- Baseline: 53,97 Wh
- Decision Tree: 49,03 Wh

På den senare testperioden blev resultatet däremot betydligt sämre:

- Baseline: 52,83 Wh
- Decision Tree: 83,97 Wh

Det innebär att vår första modellversion inte generaliserade stabilt
till den senare tidsperioden.

Projektets modellresultat ska därför inte tolkas som att vi har byggt
en färdig eller produktionsklar modell.

Däremot har utvärderingen visat hur olika modeller beter sig,
hur overfitting kan upptäckas, hur validation kan användas för
modellval och varför ett separat sluttest är viktigt.

---

# Möjliga förbättringar i fortsatt arbete

Om projektet vidareutvecklas kan följande undersökas:

- mer representativ träningsdata från fler väder- och säsongsförhållanden
- flera tidsbaserade validation-perioder
- ytterligare relevant feature engineering
- bättre regularisering av modellerna
- tidigare energianvändning som feature, om användningsfallet tillåter det
- ytterligare analys av distribution shift

Dessa förbättringar bör behandlas som nya experiment och inte som
justeringar direkt mot den redan observerade testperioden.