import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Filnamn för CSV
csv_file = "responses.csv"

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
# Dokumenterat som openEHR
st.write("""
### Patientscenario 12: Linda Sjöberg, 22 år
Patienten söker för långvarig trötthet. Hon har aldrig haft anemi. 
Hon är osäker på om hon har låga järnvärden.
""")

# OpenEHR-alternativ med förvald "(Välj ett alternativ)"
openehr_options = [
    "(Välj ett alternativ)",  # Förvalt alternativ
    "Evaluation.Problem/Diagnosis, Finns (Bekräftad diagnos eller tillstånd).",
    "Evaluation.Exclusion specific, Uteslutet (Tillståndet har aktivt bedömts som frånvarande).",
    "Evaluation.Absence of information, Information saknas (Det finns ingen tillgänglig information om tillståndet).",
    "Evaluation.Problem/Diagnosis + Cluster.Problem/Diagnosis Qualifier Preliminary, Bedömt som kliniskt relevant men inte verifierat.",
    "Evaluation.Problem/Diagnosis + Cluster.Problem/Diagnosis Qualifier Working, Noterat men bedöms som en möjlig alternativ förklaring."
]

# Funktion för att visa en fråga med dropdown
def select_openehr_status(label, key_prefix):
    st.write(f"### {label}")  # Behåller rubriken
    choice = st.selectbox(
        "",  # Tar bort rubriken ovanför dropdown-menyn
        openehr_options,
        key=f"{key_prefix}_openehr",
        index=0  # Förvalt som "(Välj ett alternativ)"
    )
    return choice

# OpenEHR Condition-verifikationer för Linda Sjöberg
ehr_fatigue = select_openehr_status("Upplever patienten trötthet?", "ehr_fatigue")
ehr_anemia = select_openehr_status("Har patienten tidigare haft anemi?", "ehr_anemia")
ehr_iron = select_openehr_status("Har patienten låga järnvärden?", "ehr_iron")
ehr_bleeding = select_openehr_status("Har patienten kraftiga menstruationsblödningar?", "ehr_bleeding")

# Sammanfattning av data
st.write("### Sammanfattning av dokumentation")
st.write(f"- Trötthet: {ehr_fatigue if ehr_fatigue != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Anemi: {ehr_anemia if ehr_anemia != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Låga järnvärden: {ehr_iron if ehr_iron != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Kraftiga menstruationsblödningar: {ehr_bleeding if ehr_bleeding != '(Välj ett alternativ)' else 'Ej angiven'}")

# Skicka in svaren
if st.button("Skicka in"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],
        "Trötthet": [ehr_fatigue if ehr_fatigue != "(Välj ett alternativ)" else "Ej angiven"],
        "Anemi": [ehr_anemia if ehr_anemia != "(Välj ett alternativ)" else "Ej angiven"],
        "Låga järnvärden": [ehr_iron if ehr_iron != "(Välj ett alternativ)" else "Ej angiven"],
        "Kraftiga menstruationsblödningar": [ehr_bleeding if ehr_bleeding != "(Välj ett alternativ)" else "Ej angiven"]
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
