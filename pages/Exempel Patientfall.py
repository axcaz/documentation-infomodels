import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Dokumentation av patientinformation med olika informationsmodeller")

# Patientinformation för Anna Andersson
st.header("Patientscenario: Anna Andersson, 45 år")
st.markdown(
    """
    **Situation**  
    <small>Anna har kommit till vårdcentralen för en rutinkontroll. Hon har nyligen genomfört en hälsoundersökning, och det har uppstått några frågor kring hennes medicinska historia och aktuella symtom.</small>  

    **Bakgrund**  
    <small>Inga kända allergier. Patienten har aldrig haft några allergiska reaktioner mot mediciner eller andra ämnen.  
    Ingen tidigare känd hjärtsjukdom eller lungsjukdom. Patienten har genomgått regelbundna hälsokontroller, och inga tecken på hjärtsvikt eller KOL har noterats.  
    Inga fall av diabetes eller cancer inom närmaste familjen. Patienten har inga nära släktingar med hjärtsjukdom eller högt blodtryck.  
    Patienten röker inte och har aldrig rökt. Hon dricker alkohol mycket sparsamt, och det finns ingen historia av drogmissbruk.</small>  

    **Läkemedel**  
    <small>Tar inga regelbundna mediciner och har ingen dokumenterad användning av receptbelagda läkemedel under det senaste året.</small>  

    **Aktuella symtom**  
    <small>Patienten upplever inga andningssvårigheter och ingen smärta vid bröstet. Hon rapporterar ingen hosta eller feber de senaste månaderna.</small>
    """, 
    unsafe_allow_html=True
)

# Användarkod för att identifiera dokumentatören
user_code = st.text_input("Ange din användarkod (ex. initialer eller ID)")

# Skapa en lista för att samla in all data
data = []

# FHIR-sektionen med korrekta val för Condition.verificationStatus
st.subheader("1 - HL7 FHIR resource Condition.verificationStatus")

data.extend([
    {"Användarkod": user_code, "Modell": "FHIR", "Parameter": "Allergier", 
     "Värde": st.radio("Verifieringsstatus för allergier", 
                       ["Obekräftad", "Provisorisk", "Differentialdiagnos", "Bekräftad", "Motbevisad", "Felaktigt inmatad"], 
                       key="allergy_verification_status_fhir"), 
     "Kommentar": st.text_area("Kommentar för allergier (FHIR)", key="allergy_comment_fhir")},
    
    {"Användarkod": user_code, "Modell": "FHIR", "Parameter": "Hjärtsjukdom", 
     "Värde": st.radio("Verifieringsstatus för hjärtsjukdom", 
                       ["Obekräftad", "Provisorisk", "Differentialdiagnos", "Bekräftad", "Motbevisad", "Felaktigt inmatad"], 
                       key="heart_verification_status_fhir"), 
     "Kommentar": st.text_area("Kommentar för hjärtsjukdom (FHIR)", key="heart_comment_fhir")},
    
    {"Användarkod": user_code, "Modell": "FHIR", "Parameter": "Lungsjukdom", 
     "Värde": st.radio("Verifieringsstatus för lungsjukdom", 
                       ["Obekräftad", "Provisorisk", "Differentialdiagnos", "Bekräftad", "Motbevisad", "Felaktigt inmatad"], 
                       key="lung_verification_status_fhir"), 
     "Kommentar": st.text_area("Kommentar för lungsjukdom (FHIR)", key="lung_comment_fhir")},
    
    {"Användarkod": user_code, "Modell": "FHIR", "Parameter": "Familjehistoria", 
     "Värde": st.radio("Verifieringsstatus för familjehistoria (diabetes/cancer)", 
                       ["Obekräftad", "Provisorisk", "Differentialdiagnos", "Bekräftad", "Motbevisad", "Felaktigt inmatad"], 
                       key="family_history_verification_status_fhir"), 
     "Kommentar": st.text_area("Kommentar för familjehistoria (FHIR)", key="family_comment_fhir")},
    
    {"Användarkod": user_code, "Modell": "FHIR", "Parameter": "Rökning", 
     "Värde": st.radio("Verifieringsstatus för rökning", 
                       ["Obekräftad", "Provisorisk", "Differentialdiagnos", "Bekräftad", "Motbevisad", "Felaktigt inmatad"], 
                       key="smoking_verification_status_fhir"), 
     "Kommentar": st.text_area("Kommentar för rökning (FHIR)", key="smoking_comment_fhir")},
    
    {"Användarkod": user_code, "Modell": "FHIR", "Parameter": "Alkoholbruk", 
     "Värde": st.radio("Verifieringsstatus för alkoholbruk", 
                       ["Obekräftad", "Provisorisk", "Differentialdiagnos", "Bekräftad", "Motbevisad", "Felaktigt inmatad"], 
                       key="alcohol_verification_status_fhir"), 
     "Kommentar": st.text_area("Kommentar för alkoholbruk (FHIR)", key="alcohol_comment_fhir")},
    
    {"Användarkod": user_code, "Modell": "FHIR", "Parameter": "Mediciner", 
     "Värde": st.radio("Verifieringsstatus för mediciner", 
                       ["Obekräftad", "Provisorisk", "Differentialdiagnos", "Bekräftad", "Motbevisad", "Felaktigt inmatad"], 
                       key="medication_verification_status_fhir"), 
     "Kommentar": st.text_area("Kommentar för mediciner (FHIR)", key="medication_comment_fhir")},
    
    {"Användarkod": user_code, "Modell": "FHIR", "Parameter": "Aktuella symtom", 
     "Värde": st.radio("Verifieringsstatus för aktuella symtom", 
                       ["Obekräftad", "Provisorisk", "Differentialdiagnos", "Bekräftad", "Motbevisad", "Felaktigt inmatad"], 
                       key="symptoms_verification_status_fhir"), 
     "Kommentar": st.text_area("Kommentar för aktuella symtom (FHIR)", key="symptoms_comment_fhir")}
])

# OpenEHR Adverse Reaction Screening Questionnaire baserat på patientfallet
st.subheader("2 - OpenEHR Adverse reaction screening questionnaire")

data.extend([
    {"Användarkod": user_code, "Modell": "OpenEHR", "Parameter": "Allergier", 
     "Värde": st.radio("Kända allergier?", ["Ja", "Nej", "Okänt"], key="allergy_reaction"), 
     "Kommentar": st.text_area("Kommentar för allergier", key="allergy_comment")},
    
    {"Användarkod": user_code, "Modell": "OpenEHR", "Parameter": "Hjärtsjukdom", 
     "Värde": st.radio("Tidigare känd hjärtsjukdom?", ["Ja", "Nej", "Okänt"], key="heart_reaction"), 
     "Kommentar": st.text_area("Kommentar för hjärtsjukdom", key="heart_comment")},
    
    {"Användarkod": user_code, "Modell": "OpenEHR", "Parameter": "Lungsjukdom", 
     "Värde": st.radio("Tidigare känd lungsjukdom?", ["Ja", "Nej", "Okänt"], key="lung_reaction"), 
     "Kommentar": st.text_area("Kommentar för lungsjukdom", key="lung_comment")},
    
    {"Användarkod": user_code, "Modell": "OpenEHR", "Parameter": "Familjehistoria (diabetes/cancer)", 
     "Värde": st.radio("Fall av diabetes eller cancer inom familjen?", ["Ja", "Nej", "Okänt"], key="family_history_reaction"), 
     "Kommentar": st.text_area("Kommentar för familjehistoria", key="family_history_comment")},
    
    {"Användarkod": user_code, "Modell": "OpenEHR", "Parameter": "Rökning", 
     "Värde": st.radio("Patienten röker?", ["Ja", "Nej", "Okänt"], key="smoking_reaction"), 
     "Kommentar": st.text_area("Kommentar för rökning", key="smoking_comment")},
    
    {"Användarkod": user_code, "Modell": "OpenEHR", "Parameter": "Alkoholbruk", 
     "Värde": st.radio("Dricker alkohol sparsamt?", ["Ja", "Nej", "Okänt"], key="alcohol_reaction"), 
     "Kommentar": st.text_area("Kommentar för alkoholbruk", key="alcohol_comment")},
    
    {"Användarkod": user_code, "Modell": "OpenEHR", "Parameter": "Läkemedel", 
     "Värde": st.radio("Tar regelbundna mediciner?", ["Ja", "Nej", "Okänt"], key="medication_reaction"), 
     "Kommentar": st.text_area("Kommentar för läkemedel", key="medication_comment")},
    
    {"Användarkod": user_code, "Modell": "OpenEHR", "Parameter": "Andningssvårigheter/smärta vid bröstet", 
     "Värde": st.radio("Andningssvårigheter eller smärta vid bröstet?", ["Ja", "Nej", "Okänt"], key="breathing_symptoms"), 
     "Kommentar": st.text_area("Kommentar för andningssvårigheter och bröstsmärta", key="breathing_symptoms_comment")},
    
    {"Användarkod": user_code, "Modell": "OpenEHR", "Parameter": "Hosta/feber", 
     "Värde": st.radio("Hosta eller feber de senaste månaderna?", ["Ja", "Nej", "Okänt"], key="cough_fever_symptoms"), 
     "Kommentar": st.text_area("Kommentar för hosta och feber", key="cough_fever_comment")}
])

# Socvialstyrelsens NIM hälsotillstånd baserat på patientfallet
st.subheader("3 - Socialstyrelsens NIM hälsotillstånd")

# Bakgrund
st.markdown("<h4>Bakgrund</h4>", unsafe_allow_html=True)

allergi_negation = st.checkbox("Inga kända allergier")
if allergi_negation:
    data.append({
        "Användarkod": user_code,
        "Parameter": "Allergier",
        "Negation": "Ja",
        "Kommentar": "Patienten har utretts för allergier men inga allergiska reaktioner hittades."
    })

hjart_negation = st.checkbox("Ingen tidigare känd hjärtsjukdom")
if hjart_negation:
    data.append({
        "Användarkod": user_code,
        "Parameter": "Hjärtsjukdom",
        "Negation": "Ja",
        "Kommentar": "Patienten har utretts för hjärtsjukdom men inga tecken på hjärtsvikt eller KOL hittades."
    })

lung_negation = st.checkbox("Ingen tidigare känd lungsjukdom")
if lung_negation:
    data.append({
        "Användarkod": user_code,
        "Parameter": "Lungsjukdom",
        "Negation": "Ja",
        "Kommentar": "Patienten har utretts för lungsjukdom men ingen lungsjukdom hittades."
    })

familj_negation = st.checkbox("Inga fall av diabetes eller cancer i familjen")
if familj_negation:
    data.append({
        "Användarkod": user_code,
        "Parameter": "Familjehistoria (diabetes/cancer)",
        "Negation": "Ja",
        "Kommentar": "Ingen närstående familjemedlem har diabetes eller cancer."
    })

rok_negation = st.checkbox("Patienten röker inte")
if rok_negation:
    data.append({
        "Användarkod": user_code,
        "Parameter": "Rökning",
        "Negation": "Ja",
        "Kommentar": "Patienten har aldrig rökt."
    })

alkohol_negation = st.checkbox("Patienten dricker alkohol sparsamt")
if alkohol_negation:
    data.append({
        "Användarkod": user_code,
        "Parameter": "Alkoholbruk",
        "Negation": "Ja",
        "Kommentar": "Patienten dricker alkohol sparsamt, inget drogmissbruk."
    })

# Läkemedel
st.markdown("<h4>Läkemedel</h4>", unsafe_allow_html=True)

mediciner_negation = st.checkbox("Tar inga regelbundna mediciner")
if mediciner_negation:
    data.append({
        "Användarkod": user_code,
        "Parameter": "Läkemedel",
        "Negation": "Ja",
        "Kommentar": "Inga regelbundna mediciner under det senaste året."
    })

# Aktuella symptom
st.markdown("<h4>Aktuella symptom</h4>", unsafe_allow_html=True)

andas_negation = st.checkbox("Inga andningssvårigheter eller smärta vid bröstet")
if andas_negation:
    data.append({
        "Användarkod": user_code,
        "Parameter": "Andningssvårigheter/smärta vid bröstet",
        "Negation": "Ja",
        "Kommentar": "Patienten rapporterar inga andningssvårigheter eller smärta vid bröstet."
    })

hosta_negation = st.checkbox("Ingen hosta eller feber de senaste månaderna")
if hosta_negation:
    data.append({
        "Användarkod": user_code,
        "Parameter": "Hosta/feber",
        "Negation": "Ja",
        "Kommentar": "Patienten har inte haft hosta eller feber de senaste månaderna."
    })

# E-hälsospecifikationer - negationsdokumentation
st.subheader("4 - E-hälsospecifikationer")

data.extend([
    {"Användarkod": user_code, "Modell": "eHälsospecifikationer", "Parameter": "Allergier", 
     "Negation": st.radio("Allergistatus (negation)", ["Negativ", "Positiv"], key="allergy_status"), 
     "Kommentar": st.text_area("Kommentar för allergier", key="allergy_comment_ehals")},
    
    {"Användarkod": user_code, "Modell": "eHälsospecifikationer", "Parameter": "Hjärtsjukdom", 
     "Negation": st.radio("Hjärtsjukdomsstatus (negation)", ["Negativ", "Positiv"], key="heart_status"), 
     "Kommentar": st.text_area("Kommentar för hjärtsjukdom", key="heart_comment_ehals")},
    
    {"Användarkod": user_code, "Modell": "eHälsospecifikationer", "Parameter": "Lungsjukdom", 
     "Negation": st.radio("Lungsjukdomsstatus (negation)", ["Negativ", "Positiv"], key="lung_status"), 
     "Kommentar": st.text_area("Kommentar för lungsjukdom", key="lung_comment_ehals")},
    
    {"Användarkod": user_code, "Modell": "eHälsospecifikationer", "Parameter": "Familjehistoria (diabetes/cancer)", 
     "Negation": st.radio("Familjehistorik för diabetes/cancer (negation)", ["Negativ", "Positiv"], key="family_history_status"), 
     "Kommentar": st.text_area("Kommentar för familjehistoria", key="family_history_comment_ehals")},
    
    {"Användarkod": user_code, "Modell": "eHälsospecifikationer", "Parameter": "Rökning", 
     "Negation": st.radio("Rökning (negation)", ["Negativ", "Positiv"], key="smoking_status"), 
     "Kommentar": st.text_area("Kommentar för rökning", key="smoking_comment_ehals")},
    
    {"Användarkod": user_code, "Modell": "eHälsospecifikationer", "Parameter": "Alkoholbruk", 
     "Negation": st.radio("Alkoholbruk (negation)", ["Negativ", "Positiv"], key="alcohol_status"), 
     "Kommentar": st.text_area("Kommentar för alkoholbruk", key="alcohol_comment_ehals")},
    
    {"Användarkod": user_code, "Modell": "eHälsospecifikationer", "Parameter": "Läkemedel", 
     "Negation": st.radio("Använder patienten mediciner? (negation)", ["Negativ", "Positiv"], key="medication_status"), 
     "Kommentar": st.text_area("Kommentar för läkemedel", key="medication_comment_ehals")},
    
    {"Användarkod": user_code, "Modell": "eHälsospecifikationer", "Parameter": "Andningssvårigheter/bröstsmärta", 
     "Negation": st.radio("Andningssvårigheter eller bröstsmärta? (negation)", ["Negativ", "Positiv"], key="breathing_symptoms_ehals"), 
     "Kommentar": st.text_area("Kommentar för andningssvårigheter och bröstsmärta", key="breathing_symptoms_comment_ehals")},
    
    {"Användarkod": user_code, "Modell": "eHälsospecifikationer", "Parameter": "Hosta/feber", 
     "Negation": st.radio("Hosta eller feber (negation)", ["Negativ", "Positiv"], key="cough_fever_symptoms_ehals"), 
     "Kommentar": st.text_area("Kommentar för hosta och feber", key="cough_fever_comment_ehals")}
])


# Spara-knapp för att logga all användarinmatning
if st.button("Spara dokumentation") and user_code:
    df = pd.DataFrame(data)
    try:
        existing_data = pd.read_csv("negation_data_all.csv", encoding="utf-8-sig")
        updated_data = pd.concat([existing_data, df], ignore_index=True)
    except FileNotFoundError:
        updated_data = df

    updated_data.to_csv("negation_data_all.csv", index=False, encoding="utf-8-sig")
    st.success("Informationen har sparats i negation_data_all.csv!")
else:
    st.warning("Ange en användarkod innan du sparar data.")
