import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Filnamn för CSV
csv_file = "responses.csv"

# CSS för stil
st.markdown("""
    <style>
        .description {
            font-size: 0.85em;
            color: #555;
            font-style: italic;
            margin-left: 10px;
        }
        .info-text {
            font-size: 0.75em;
            color: #0078D7;
            font-style: italic;
            margin-left: 25px; /* Indrag för att linjera med radio-knappen */
            margin-top: -5px;
        }
        .sub-option-container {
            margin-left: 40px; /* Indrag för underalternativ */
        }
        .sub-description {
            font-size: 0.85em;
            color: #555;
            font-style: italic;
            margin-left: 60px; /* Extra indrag för beskrivning */
        }
    </style>
""", unsafe_allow_html=True)

# Fråga om en unik kod
user_code = st.text_input("Ange din unika kod som du får av intervjuaren och tryck enter:")

# Titel och patientscenario
st.write("""
### Patientscenario 3: Kent Persson, 67 år
Patienten kommer till akuten med bröstsmärta. Han har aldrig haft en stroke. Han vet inte om han har högt blodtryck.
""")

# Huvudalternativ
fhir_main_options = {
    "Bekräftad": "Förklaring: Det finns tillräckligt med bevis för att fastställa förekomsten av patientens tillstånd.",
    "Motbevisad": "Förklaring: Detta tillstånd har uteslutits av efterföljande diagnostiska och kliniska bevis.",
    "Obekräftad": "Förklaring: Det finns inte tillräckligt med bevis för att fastställa förekomsten av patientens tillstånd."
}

# Underalternativ för "Obekräftad"
fhir_suboptions = {
    "Provisorisk": "Förklaring: Detta är en preliminär diagnos - fortfarande en kandidat som övervägs.",
    "Differential": "Förklaring: En av en uppsättning potentiella (och vanligtvis ömsesidigt uteslutande) diagnoser som anges för att ytterligare vägleda den diagnostiska processen och preliminär behandling."
}

# Funktion för att hantera val
def select_fhir_status(label, key_prefix):
    st.write(f"### {label}")

    options = list(fhir_main_options.keys())

    # Huvudval med radio-knappar
    selected_main = st.radio("Välj status:", options, key=f"{key_prefix}_main", index=None)

    # Blå förklarande text under "Obekräftad" – alltid synlig
    st.markdown('<p class="info-text">(Om du väljer "Obekräftad" måste du välja ett underalternativ)</p>', unsafe_allow_html=True)

    # Visa beskrivning av det valda alternativet
    if selected_main:
        st.markdown(f'<p class="description">{fhir_main_options[selected_main]}</p>', unsafe_allow_html=True)

    # Om Obekräftad väljs, visa underalternativ (med korrekt indrag)
    selected_sub = None
    if selected_main == "Obekräftad":
        st.markdown('<p class="sub-option-container"><strong>Underalternativ för Obekräftad:</strong></p>', unsafe_allow_html=True)

        suboptions = list(fhir_suboptions.keys())

        col1, col2 = st.columns([1, 4])  # Indrag av radio-knappen genom två kolumner
        with col2:
            selected_sub = st.radio("Välj underalternativ:", suboptions, key=f"{key_prefix}_sub", index=None)

        # Visa beskrivning av valt underalternativ
        if selected_sub:
            st.markdown(f'<p class="sub-description">{fhir_suboptions[selected_sub]}</p>', unsafe_allow_html=True)

    # Returnera vald kombination
    if selected_main == "Obekräftad" and selected_sub:
        return f"{selected_main} - {selected_sub}"
    return selected_main

# HL7 FHIR ConditionVerificationStatus
fhir_pain = select_fhir_status("Har patienten bröstsmärta?", "fhir_pain")
fhir_stroke = select_fhir_status("Har patienten haft en stroke tidigare?", "fhir_stroke")
fhir_bp = select_fhir_status("Har patienten högt blodtryck?", "fhir_bp")
fhir_medication = select_fhir_status("Finns det information om patientens aktuella medicinering i journalen?", "fhir_medication")

# Sammanfattning av valda alternativ
st.write("### Sammanfattning av dokumentation")
st.write(f"- Bröstsmärta: {fhir_pain if fhir_pain else 'Ej angiven'}")
st.write(f"- Stroke: {fhir_stroke if fhir_stroke else 'Ej angiven'}")
st.write(f"- Högt blodtryck: {fhir_bp if fhir_bp else 'Ej angiven'}")
st.write(f"- Aktuell medicinering: {fhir_medication if fhir_medication else 'Ej angiven'}")

# Skicka in svaren
if st.button("Skicka in"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],
        "Bröstsmärta": [fhir_pain],
        "Stroke": [fhir_stroke],
        "Högt blodtryck": [fhir_bp],
        "Aktuell medicinering": [fhir_medication]
    })

    if os.path.exists(csv_file):
        existing_data = pd.read_csv(csv_file)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(csv_file, index=False)
    st.success("Dina svar har sparats!")