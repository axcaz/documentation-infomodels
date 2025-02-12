import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Filnamn för CSV
csv_file = "openEHR_responses.csv"

# Lägg till anpassad CSS för att minska bredden på dropdown-menyerna
st.markdown("""
    <style>
    .stSelectbox {
        width: 80% !important;  /* Justerar bredden till 80% */
    }
    </style>
    """, unsafe_allow_html=True)

# Fråga om en unik kod
user_code = st.text_input("Ange din unika kod som du får av intervjuaren och tryck enter:")

# Titel och patientscenario
# Dokumentation enligt OpenEHR
st.write("""
### Patientscenario 4: Stina Eriksson, 52 år
Patienten söker vårdcentralen för ledsmärta. Hon har aldrig fått diagnosen reumatism. Hon är osäker på om någon i hennes familj har haft liknande besvär. 
""")

# OpenEHR-alternativ, inklusive en tom första rad för att ha dropdowns förvalda som tomma
openehr_options = [
    "",  # Tomt alternativ (standard)
    "Evaluation.Problem/Diagnosis, Finns (Bekräftad diagnos eller tillstånd).",
    "Evaluation.Exclusion specific, Uteslutet (Tillståndet har aktivt bedömts som frånvarande).",
    "Evaluation.Absence of information, Information saknas (Det finns ingen tillgänglig information om tillståndet).",
    "Evaluation.Problem/Diagnosis + Cluster.Problem/Diagnosis Qualifier Preliminary, Bedömt som kliniskt relevant men inte verifierat.",
    "Evaluation.Problem/Diagnosis + Cluster.Problem/Diagnosis Qualifier Working, Noterat men bedöms som en möjlig alternativ förklaring."
]

# Funktion för att välja OpenEHR-status
def select_openehr_status(label, key_prefix):
    st.write(f"### {label}")
    choice = st.selectbox(
        "Välj ett alternativ:",
        openehr_options,
        key=f"{key_prefix}_openehr",
        index=0  # Förvalt tom
    )
    return choice

# OpenEHR Condition-verifikationer för Stina Eriksson
ehr_pain = select_openehr_status("Har patienten ledsmärta?", "ehr_pain")
ehr_rheumatism = select_openehr_status("Har patienten konstaterad reumatism?", "ehr_rheumatism")
ehr_inheritance = select_openehr_status("Finns ärftlighet för liknande besvär?", "ehr_inheritance")
ehr_fever = select_openehr_status("Har patienten feber?", "ehr_fever")

# Skicka in svaren
if st.button("Skicka in"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],
        "Ledsmärta": [ehr_pain],
        "Reumatism": [ehr_rheumatism],
        "Ärftlighet": [ehr_inheritance],
        "Feber": [ehr_fever]
    })

    if os.path.exists(csv_file):
        existing_data = pd.read_csv(csv_file)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(csv_file, index=False)
    st.success("Dina svar har sparats!")

# Visa insamlade svar
if st.button("Visa insamlade svar"):
    if os.path.exists(csv_file):
        data = pd.read_csv(csv_file)
        st.write(data)
    else:
        st.warning("Inga svar har samlats in ännu.")
