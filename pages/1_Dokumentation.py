import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Spara och visa dokumentation för negationer med användarkod")

# Användarkod (används för att identifiera filen)
user_code = st.text_input("Ange din användarkod (t.ex. initialer eller ID)").strip()

# Skapa en lista för att samla in data
data = []

# Scenario 1: Patienten har inga kända allergier
st.header("Scenario 1: Inga kända allergier")

# Modell: openEHR
allergy_open_ehr = st.radio("Finns det kända allergier?", ["Ja", "Nej"], key="allergy_open_ehr")  # openEHR
allergy_comment_open_ehr = st.text_area("Kommentar för allergier", key="allergy_comment_open_ehr")  # openEHR
data.append({
    "Användarkod": user_code,
    "Scenario": "Inga kända allergier",
    "Modell": "openEHR",
    "Allergi": allergy_open_ehr,
    "Kommentar": allergy_comment_open_ehr,
    "Tidpunkt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

# Modell: FHIR
allergy_fhir = st.radio("Finns det kända allergier?", ["Ja", "Nej"], key="allergy_fhir")  # FHIR
allergy_comment_fhir = st.text_area("Kommentar för allergier", key="allergy_comment_fhir")  # FHIR
data.append({
    "Användarkod": user_code,
    "Scenario": "Inga kända allergier",
    "Modell": "FHIR",
    "Allergi": allergy_fhir,
    "Kommentar": allergy_comment_fhir,
    "Tidpunkt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

# Modell: NIM Hälsotillstånd
allergy_nim = st.checkbox("Inga kända allergier", key="allergy_nim")  # NIM Hälsotillstånd
allergy_comment_nim = st.text_area("Kommentar för allergier", key="allergy_comment_nim")  # NIM Hälsotillstånd
data.append({
    "Användarkod": user_code,
    "Scenario": "Inga kända allergier",
    "Modell": "NIM Hälsotillstånd",
    "Allergi": "Sant" if allergy_nim else "Falskt",
    "Kommentar": allergy_comment_nim,
    "Tidpunkt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

# Modell: eHälsospecifikationer
allergy_ehals = st.radio("Allergistatus", ["Negativ", "Positiv"], key="allergy_ehals")  # eHälsospecifikationer
allergy_comment_ehals = st.text_area("Kommentar för allergier", key="allergy_comment_ehals")  # eHälsospecifikationer
data.append({
    "Användarkod": user_code,
    "Scenario": "Inga kända allergier",
    "Modell": "eHälsospecifikationer",
    "Allergistatus": allergy_ehals,
    "Kommentar": allergy_comment_ehals,
    "Tidpunkt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

# Scenario 2: Patienten är inte gravid och har ingen tidigare känd hjärtsjukdom
st.header("Scenario 2: Inte gravid och ingen tidigare känd hjärtsjukdom")

# Modell: openEHR
preg_open_ehr = st.radio("Graviditetsstatus", ["Gravid", "Inte gravid"], key="preg_open_ehr")  # openEHR
heart_open_ehr = st.radio("Hjärtsjukdomsstatus", ["Hjärtsjukdom finns", "Ingen tidigare hjärtsjukdom"], key="heart_open_ehr")  # openEHR
preg_comment_open_ehr = st.text_area("Kommentar för graviditet och hjärtsjukdom", key="preg_comment_open_ehr")  # openEHR
data.append({
    "Användarkod": user_code,
    "Scenario": "Inte gravid och ingen tidigare känd hjärtsjukdom",
    "Modell": "openEHR",
    "Graviditetsstatus": preg_open_ehr,
    "Hjärtsjukdomsstatus": heart_open_ehr,
    "Kommentar": preg_comment_open_ehr,
    "Tidpunkt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

# Modell: FHIR
preg_fhir = st.radio("Graviditetsstatus", ["Gravid", "Inte gravid"], key="preg_fhir")  # FHIR
heart_fhir = st.radio("Hjärtsjukdomsstatus", ["Hjärtsjukdom finns", "Ingen tidigare hjärtsjukdom"], key="heart_fhir")  # FHIR
preg_comment_fhir = st.text_area("Kommentar för graviditet och hjärtsjukdom", key="preg_comment_fhir")  # FHIR
data.append({
    "Användarkod": user_code,
    "Scenario": "Inte gravid och ingen tidigare känd hjärtsjukdom",
    "Modell": "FHIR",
    "Graviditetsstatus": preg_fhir,
    "Hjärtsjukdomsstatus": heart_fhir,
    "Kommentar": preg_comment_fhir,
    "Tidpunkt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

# Modell: NIM Hälsotillstånd
preg_nim = st.checkbox("Inte gravid", key="preg_nim")  # NIM Hälsotillstånd
heart_nim = st.checkbox("Ingen tidigare hjärtsjukdom", key="heart_nim")  # NIM Hälsotillstånd
preg_comment_nim = st.text_area("Kommentar för graviditet och hjärtsjukdom", key="preg_comment_nim")  # NIM Hälsotillstånd
data.append({
    "Användarkod": user_code,
    "Scenario": "Inte gravid och ingen tidigare känd hjärtsjukdom",
    "Modell": "NIM Hälsotillstånd",
    "Graviditetsstatus": "Sant" if preg_nim else "Falskt",
    "Hjärtsjukdomsstatus": "Sant" if heart_nim else "Falskt",
    "Kommentar": preg_comment_nim,
    "Tidpunkt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

# Modell: eHälsospecifikationer
preg_ehals = st.radio("Graviditetsstatus", ["Positiv", "Negativ"], key="preg_ehals")  # eHälsospecifikationer
heart_ehals = st.radio("Hjärtsjukdomsstatus", ["Positiv", "Negativ"], key="heart_ehals")  # eHälsospecifikationer
preg_comment_ehals = st.text_area("Kommentar för graviditet och hjärtsjukdom", key="preg_comment_ehals")  # eHälsospecifikationer
data.append({
    "Användarkod": user_code,
    "Scenario": "Inte gravid och ingen tidigare känd hjärtsjukdom",
    "Modell": "eHälsospecifikationer",
    "Graviditetsstatus": preg_ehals,
    "Hjärtsjukdomsstatus": heart_ehals,
    "Kommentar": preg_comment_ehals,
    "Tidpunkt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

# Scenario 3: Patienten uppger inga tidigare operationer
st.header("Scenario 3: Inga tidigare operationer")

# Modell: openEHR
surgery_open_ehr = st.checkbox("Inga tidigare operationer", key="surgery_open_ehr")  # openEHR
surgery_comment_open_ehr = st.text_area("Kommentar för tidigare operationer", key="surgery_comment_open_ehr")  # openEHR
data.append({
    "Användarkod": user_code,
    "Scenario": "Inga tidigare operationer",
    "Modell": "openEHR",
    "Tidigare operationer": "Sant" if surgery_open_ehr else "Falskt",
    "Kommentar": surgery_comment_open_ehr,
    "Tidpunkt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

# Modell: FHIR
surgery_fhir = st.checkbox("Inga tidigare operationer", key="surgery_fhir")  # FHIR
surgery_comment_fhir = st.text_area("Kommentar för tidigare operationer", key="surgery_comment_fhir")  # FHIR
data.append({
    "Användarkod": user_code,
    "Scenario": "Inga tidigare operationer",
    "Modell": "FHIR",
    "Tidigare operationer": "Sant" if surgery_fhir else "Falskt",
    "Kommentar": surgery_comment_fhir,
    "Tidpunkt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

# Modell: NIM Hälsotillstånd
surgery_nim = st.checkbox("Inga tidigare operationer", key="surgery_nim")  # NIM Hälsotillstånd
surgery_comment_nim = st.text_area("Kommentar för tidigare operationer", key="surgery_comment_nim")  # NIM Hälsotillstånd
data.append({
    "Användarkod": user_code,
    "Scenario": "Inga tidigare operationer",
    "Modell": "NIM Hälsotillstånd",
    "Tidigare operationer": "Sant" if surgery_nim else "Falskt",
    "Kommentar": surgery_comment_nim,
    "Tidpunkt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

# Modell: eHälsospecifikationer
surgery_ehals = st.radio("Operationsstatus", ["Positiv", "Negativ"], key="surgery_ehals")  # eHälsospecifikationer
surgery_comment_ehals = st.text_area("Kommentar för tidigare operationer", key="surgery_comment_ehals")  # eHälsospecifikationer
data.append({
    "Användarkod": user_code,
    "Scenario": "Inga tidigare operationer",
    "Modell": "eHälsospecifikationer",
    "Operationsstatus": surgery_ehals,
    "Kommentar": surgery_comment_ehals,
    "Tidpunkt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

# Spara-knapp för att logga användarinmatning
if st.button("Spara dokumentation") and user_code:
    # Konvertera till DataFrame
    df = pd.DataFrame(data)
    
    # Spara till en gemensam CSV-fil
    try:
        # Läs in befintlig data om filen redan finns
        existing_data = pd.read_csv("negation_data_all.csv", encoding="utf-8-sig")
        # Lägg till ny data till den befintliga
        updated_data = pd.concat([existing_data, df], ignore_index=True)
    except FileNotFoundError:
        # Om filen inte finns, skapa en ny
        updated_data = df

    # Spara till fil
    updated_data.to_csv("negation_data_all.csv", index=False, encoding="utf-8-sig")
    st.success("Informationen har sparats i den gemensamma filen negation_data_all.csv!")
else:
    st.warning("Ange en användarkod innan du sparar data.")
