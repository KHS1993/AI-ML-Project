# AI-ML-Project## Modellutvärdering – första versionen

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

### Slutsats och begränsningar

Decision Tree presterade bättre än baselinen på valideringsdatan,
men sämre på den senare testperioden.

Vi har därför inte visat att den valda modellen ger bättre
prediktioner än vår enkla baseline på testperioden.

Testperioden hade högre utomhustemperaturer än träningsperioden.
Det är en möjlig bidragande faktor, men analysen bevisar inte
att temperaturen förklarar modellens större fel.

Detta är resultatet för vår första modellversion. Eventuella
fortsatta förbättringar ska dokumenteras som nya experiment.