# Modellutvärdering – Appliances Energy Prediction

## Syfte

Vi undersöker om våra modeller kan uppskatta hushållsapparaternas
energianvändning bättre än en enkel referens, en baseline.

Dokumentet beskriver hur vi jämförde modellerna, vilka resultat
vi fick och hur vi valde modellen för sluttestet.

## Utvärderingsupplägg

### Vad försöker vi förutsäga?

Vår target är `Appliances`, hushållsapparaternas energianvändning
angiven i Wh.

Det är ett regressionsproblem eftersom modellen ska uppskatta
ett numeriskt värde.

### Vilken information använder modellerna?

Vi använder sex klimatvariabler:

`T1`, `RH_1`, `T2`, `RH_2`, `T_out` och `RH_out`.

Dessutom skapade vi tre tidsvariabler från datumkolumnen:

- `hour`: timmen på dygnet.
- `day_of_week`: veckodagen.
- `is_weekend`: 1 för lördag och söndag, annars 0.

Tidsvariablerna ger modellerna möjlighet att skilja mellan
exempelvis natt, dag, vardag och helg.

### Hur delade vi upp datan?

Det tidsordnade datasetet delades upp i tre delar.
Vi blandade inte raderna slumpmässigt.

| Datadel | Ungefärlig andel | Antal observationer | Användning |
|---|---:|---:|---|
| Train | 70 % | 13 814 | Träna modellerna och beräkna baselinevärdet |
| Validation | 15 % | 2 960 | Jämföra modeller och välja inställningar |
| Test | 15 % | 2 961 | Slutbedöma den valda modellversionen |

De äldsta observationerna användes för träning och de senaste
för test. Syftet var att undersöka hur en modell tränad på
historiska mätningar fungerar på en senare period.

### Vad är vår baseline?

Baselinen gissar alltid träningsdatans genomsnittliga energianvändning,
cirka 98,78 Wh, oavsett temperatur och tid.

Den används för att kontrollera om modellerna tillför något
jämfört med en enkel konstantgissning.

Baselinevärdet beräknades enbart från träningsdatan.

### Hur mäter vi resultatet?

Vi använder MAE, Mean Absolute Error.

MAE beskriver hur stort det absoluta felet är i genomsnitt.
Ett MAE på 50 Wh betyder att uppskattningarna i genomsnitt
avviker 50 Wh från de verkliga värdena.

Lägre MAE är bättre. Måttet är inte en procentsats.

## Resultat på valideringsdata

Modellerna tränades på samma träningsperiod och jämfördes på
samma valideringsperiod.

| Modell | Validation MAE (Wh) |
|---|---:|
| Baseline: träningsmedelvärdet | 53,97 |
| Linear Regression | 53,70 |
| Decision Tree, max_depth=7 | 49,03 |
| Random Forest, 100 träd | 59,42 |

### Tolkning

Decision Tree med `max_depth=7` hade lägst valideringsfel bland
de modeller och inställningar vi testade. Den valdes därför
för sluttestet.

Linear Regression gav en liten förbättring jämfört med baselinen,
medan Random Forest gav större fel.

Resultaten ovan gäller endast valideringsperioden.
Sluttestet behöver redovisas separat för att visa hur den
valda modellen fungerade på den senare testperioden.