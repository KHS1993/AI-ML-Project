# PoC Redovisning - Punkt 2, 5 och 10

## 2. Testa riktig prediction i Swagger
- **Syfte:** Verifiera att FastAPI-endpointen `/predict` hanterar giltig indata korrekt samt att Pydantic-valideringen fångar upp felaktig eller saknad data.
- **Resultat:** 
  - Giltigt anrop gav status `200 OK` och returnerade en dynamiskt beräknad prediktion från maskininlärningsmodellen.
  - Test med saknad obligatorisk feature (`T1`) avvisades direkt av Pydantic med status `422 Unprocessable Entity`.

## 5. Testa Streamlit end-to-end
- **Syfte:** Säkerställa att helhetsflödet från användargränssnitt till backend och AI-modell fungerar i realtid.
- **Resultat:** 
  - Test A (standardvärden) och Test B (avvikande värden) anropade FastAPI via `requests.post` och visade upp korrekta, dynamiskt förändrade mätvärden i `st.metric`.

## 10. Dokumentera PoC-flödet
- **Dataflöde:** `Streamlit (UI) → FastAPI (Backend) → model_service → .joblib (Modell) → Prediction → Streamlit (Visning)`
- **Ändringar:** All hårdkodad mock-data har tagits bort och ersatts med riktiga dynamiska API-anrop till modellen.
- **Verifiering:** Testat end-to-end lokalt med både FastAPI och Streamlit igång parallellt.