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
        width: 30% !important;  /* Justerar bredden till 30% */
    }
    </style>
    """, unsafe_allow_html=True)

# Fråga om en unik kod
user_code = st.text_input("Ange din unika kod som du får av intervjuaren och tryck enter:")

# Titel och patientscenario
st.title("Dokumentera enligt HL7 FHIR ConditionVerificationStatus")
st.write("""
### Patientscenario 1: Anna Andersson, 45 år
Anna söker vårdcentralen r/t förhöjt blodtryck som hon märkt av hemma själv med sin blodtrycksmätare. 
Hon har aldrig haft någon stroke. Hon är osäker på om hon reagerat på penicillin som barn.
""")

# HL7 FHIR-alternativ med hierarki och beskrivningar
fhir_main_options = {
    "Unconfirmed": {
        "description": "There is not sufficient diagnostic and/or clinical evidence to treat this as a confirmed condition.",
        "suboptions": {
            "Provisional": "This is a tentative diagnosis - still a candidate that is under consideration.",
            "Differential": "One of a set of potential (and typically mutually exclusive) diagnoses asserted to further guide the diagnostic process and preliminary treatment."
        }
    },
    "Confirmed": {
        "description": "There is sufficient diagnostic and/or clinical evidence to treat this as a confirmed condition.",
        "suboptions": None
    },
    "Refuted": {
        "description": "This condition has been ruled out by subsequent diagnostic and clinical evidence.",
        "suboptions": None
    }
}

# Funktion för att hantera dropdown-logik med inforutor
def select_hierarchical_with_info(label, main_options, key_prefix):
    # Första dropdown
    st.write(f"### {label}")
    main_choice = st.selectbox(
        "Välj en huvudstatus:",
        list(main_options.keys()),
        key=f"{key_prefix}_main"
    )
    st.markdown(f"ℹ️ **Beskrivning:** {main_options[main_choice]['description']}")

    # Om huvudstatus har underalternativ, visa en andra dropdown
    sub_choice = None
    if main_options[main_choice]["suboptions"]:
        sub_choice = st.selectbox(
            "Välj en understatus:",
            list(main_options[main_choice]["suboptions"].keys()),
            key=f"{key_prefix}_sub"
        )
        st.markdown(f"ℹ️ **Beskrivning:** {main_options[main_choice]['suboptions'][sub_choice]}")

    # Återvänd valda alternativ
    if sub_choice:
        return f"{main_choice} - {sub_choice}"
    return main_choice

# HL7 FHIR ConditionVerificationStatus
fhir_bp = select_hierarchical_with_info("Har patienten förhöjt blodtryck?", fhir_main_options, "fhir_bp")
fhir_stroke = select_hierarchical_with_info("Har patienten haft stroke?", fhir_main_options, "fhir_stroke")
fhir_pc_allergy = select_hierarchical_with_info("Har patienten allergi mot penicillin?", fhir_main_options, "fhir_pc_allergy")
fhir_surgery = select_hierarchical_with_info("Är patienten opererad i buken?", fhir_main_options, "fhir_surgery")

# Skicka in svaren
if st.button("Skicka in"):
    # Skapa en rad med svaren
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Datum och tid
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],  # Ange koden eller "Ej angiven"
        "Förhöjt blodtryck": [fhir_bp],
        "Stroke": [fhir_stroke],
        "Allergi mot penicillin": [fhir_pc_allergy],
        "Operation i buken": [fhir_surgery]
    })

    # Kontrollera om filen redan finns
    if os.path.exists(csv_file):
        # Om filen finns, läs in den och lägg till nya svar
        existing_data = pd.read_csv(csv_file)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        # Om filen inte finns, skapa en ny
        updated_data = new_data

    # Spara tillbaka till CSV-filen
    updated_data.to_csv(csv_file, index=False)
    st.success("Dina svar har sparats!")

# Visa insamlade svar
if st.button("Visa insamlade svar"):
    if os.path.exists(csv_file):
        data = pd.read_csv(csv_file)
        st.write(data)
    else:
        st.warning("Inga svar har samlats in ännu.")
