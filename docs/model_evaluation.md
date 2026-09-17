# Modellutvärdering – Appliances Energy Prediction

## Syfte

Syftet med modellutvärderingen är att jämföra våra regressionsmodeller
och undersöka hur väl de kan uppskatta hushållsapparaternas
energianvändning.

Vi jämför modellerna med en enkel baseline och använder flera
regressionsmått för att bedöma resultaten.

Vi undersöker även skillnaden mellan train och validation för att
upptäcka möjlig overfitting.

---

## Problem och target

Projektets target är `Appliances`.

`Appliances` representerar hushållsapparaternas energianvändning
i Wh under varje mätintervall.

Eftersom target är ett kontinuerligt numeriskt värde är detta
ett regressionsproblem.

---

## Features

Modellerna använder följande klimatvariabler:

- `T1`
- `RH_1`
- `T2`
- `RH_2`
- `T_out`
- `RH_out`

Vi skapade även tre tidsbaserade features från kolumnen `date`:

- `hour`
- `day_of_week`
- `is_weekend`

Syftet är att ge modellerna information om när observationen gjordes,
eftersom energianvändningen kan följa olika mönster vid olika tider
och dagar.

---

## Datauppdelning

Datasetet är tidsordnat.

Därför behöll vi tidsordningen istället för att blanda observationerna
slumpmässigt.

| Datadel | Andel | Observationer | Användning |
|---|---:|---:|---|
| Train | 70 % | 13 814 | Träna modellerna |
| Validation | 15 % | 2 960 | Jämföra modeller och välja inställningar |
| Test | 15 % | 2 961 | Slutlig utvärdering |

De äldsta observationerna används för träning och de senaste för test.

Det gör utvärderingen mer lik ett verkligt scenario där historiska
mätningar används för att göra prediktioner på en senare tidsperiod.

---

## Baseline

Som referens skapade vi en enkel baseline.

Baselinen förutsäger alltid medelvärdet av target i träningsdatan.

Baselinevärdet är cirka:

**98,78 Wh**

Baselinen använder alltså inga features.

Syftet är att kontrollera om Machine Learning-modellerna faktiskt
ger bättre resultat än en mycket enkel metod.

---

# Utvärderingsmått

Vi använder tre regressionsmått:

## MAE

MAE står för Mean Absolute Error.

Det visar hur stort det absoluta prediktionsfelet är i genomsnitt.

Ett MAE på 50 Wh betyder att modellens prediktioner i genomsnitt
avviker ungefär 50 Wh från de verkliga värdena.

Lägre MAE är bättre.

## RMSE

RMSE står för Root Mean Squared Error.

Precis som MAE mäter det storleken på prediktionsfelet, men RMSE
straffar stora fel hårdare.

Lägre RMSE är bättre.

## R²

R² beskriver hur väl modellen fångar variationen i target jämfört
med en enkel referens.

Ett högre värde är bättre.

Ett R² nära 0 betyder att modellen ger liten förbättring jämfört
med en enkel referens.

Ett negativt R² betyder att modellen presterar sämre än referensen
på den aktuella datan.

R² ska inte tolkas som procent korrekt.

---

# Jämförelse på validation-data

Alla modeller tränades på samma train-data och jämfördes på samma
validation-data.

| Modell | MAE | RMSE | R² |
|---|---:|---:|---:|
| Baseline | 53,97 Wh | 92,39 Wh | -0,003 |
| Linear Regression | 53,70 Wh | 91,05 Wh | 0,026 |
| Decision Tree | **49,03 Wh** | **90,77 Wh** | **0,032** |
| Random Forest | 59,42 Wh | 102,82 Wh | -0,243 |

Decision Tree hade lägst MAE och RMSE samt högst R² på
validation-datan bland modellerna vi testade.

Därför gav Decision Tree bäst validation-resultat i våra experiment.

---

# Linear Regression

Linear Regression fick:

- MAE: 53,70 Wh
- RMSE: 91,05 Wh
- R²: 0,026

Resultatet ligger nära baselinen.

Det visar att modellen endast gav en liten förbättring jämfört med
att alltid använda träningsdatans medelvärde.

---

# Decision Tree

## Begränsning av modellens komplexitet

En tidigare obegränsad Decision Tree visade tydlig overfitting.

Vi testade därför olika värden för `max_depth`.

Bland de testade inställningarna gav:

`max_depth=7`

lägst validation-MAE.

Den valda modellen blev därför:

`DecisionTreeRegressor(max_depth=7, random_state=42)`

---

## Train jämfört med validation

Resultaten för Decision Tree blev:

| Mått | Train | Validation |
|---|---:|---:|
| MAE | 49,75 Wh | 49,03 Wh |
| RMSE | 91,23 Wh | 90,77 Wh |
| R² | 0,271 | 0,032 |

MAE och RMSE ligger mycket nära varandra mellan train och validation.

Det betyder att den extrema overfitting som fanns i det obegränsade
trädet minskade tydligt efter att modellens djup begränsades.

R² sjunker däremot från 0,271 på train till 0,032 på validation,
vilket visar att modellen fortfarande har begränsad förmåga att
förklara variationen i ny data.

---

# Random Forest

Random Forest fick:

| Mått | Train | Validation |
|---|---:|---:|
| MAE | 11,64 Wh | 59,42 Wh |
| RMSE | 24,58 Wh | 102,82 Wh |
| R² | 0,947 | -0,243 |

Skillnaden mellan train och validation är mycket stor.

Random Forest fungerar mycket bra på träningsdatan men betydligt
sämre på validation-datan.

Det är ett tydligt tecken på overfitting.

Modellen valdes därför inte.

---

# Modellval

Vi valde:

**Decision Tree med `max_depth=7`**

Beslutet baserades på resultaten från validation-datan.

Decision Tree hade:

- lägst MAE
- lägst RMSE
- högst R²

bland modellerna vi testade på samma validation-period.

Testdatan användes inte för det ursprungliga modellvalet.

---

# Sluttest

Efter modellvalet utvärderades Decision Tree på testperioden.

## Resultat

| Modell | MAE | RMSE | R² |
|---|---:|---:|---:|
| Baseline | **52,83 Wh** | **90,89 Wh** | cirka 0,000 |
| Decision Tree | 83,97 Wh | 146,93 Wh | -1,614 |

Decision Tree presterade betydligt sämre på testperioden än på
validation-perioden.

Baselinen presterade även bättre än Decision Tree på samtliga
testmått.

Det betyder att vår valda Decision Tree inte visade stabil
generaliseringsförmåga till den senare testperioden.

---

# Distribution shift

För att undersöka en möjlig förklaring till skillnaden mellan
validation och test analyserade vi `T_out`.

Genomsnittlig utomhustemperatur:

| Datadel | T_out |
|---|---:|
| Train | 5,72 °C |
| Validation | 8,22 °C |
| Test | 14,51 °C |

Testperioden var alltså betydligt varmare än träningsperioden.

Medianen för `T_out` var också tydligt högre:

- Train: 5,67 °C
- Validation: 7,55 °C
- Test: 14,30 °C

Det visar att fördelningen av åtminstone vissa features förändras
mellan tidsperioderna.

Detta är ett exempel på distribution shift.

Det kan bidra till att modellen generaliserar sämre på testperioden,
men analysen bevisar inte att förändringen i `T_out` ensam orsakar
det höga testfelet.

---

# Slutsats

Decision Tree med `max_depth=7` gav bäst resultat på validation-data
av de modeller vi testade.

Validation-resultaten var:

- MAE: 49,03 Wh
- RMSE: 90,77 Wh
- R²: 0,032

Modellen valdes därför utifrån faktiska resultat på validation-datan.

Random Forest visade tydlig overfitting genom den stora skillnaden
mellan train och validation.

På den senare testperioden presterade Decision Tree däremot sämre
än baselinen:

- Decision Tree MAE: 83,97 Wh
- Baseline MAE: 52,83 Wh

Testresultatet visar därför att den nuvarande modellen inte
generaliserar stabilt till den senare tidsperioden.

Projektets resultat ska inte tolkas som att modellen är
produktionsklar.

Utvärderingen visar däremot ett komplett ML-arbetsflöde där modeller
jämförs på samma validation-data, flera regressionsmått används,
overfitting analyseras och modellvalet baseras på faktiska resultat.

---

# Möjliga framtida förbättringar

Vid fortsatt utveckling skulle vi kunna undersöka:

- fler tidsbaserade validation-perioder
- TimeSeriesSplit
- fler relevanta features
- ytterligare regularisering
- mer representativ träningsdata
- ytterligare analys av distribution shift
- tidigare energianvändning som feature om användningsfallet tillåter det

Nya modellförändringar bör utvärderas utan att optimera direkt mot
den testperiod som redan har analyserats.