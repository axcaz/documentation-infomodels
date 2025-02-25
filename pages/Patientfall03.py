import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import base64
import os

# Filnamn för CSV
csv_file = "responses.csv"

# GitHub repo detaljer
GITHUB_REPO = "axcaz/documentation-infomodels"  # Byt ut till ditt riktiga repo
GITHUB_BRANCH = "main"
GITHUB_FILE_PATH = "responses.csv"

# Hämta GitHub-token från Render's Environment Variables
GITHUB_TOKEN = os.getenv("github_token")

# Funktion för att ladda upp fil till GitHub
def upload_to_github(file_path):
    """Laddar upp responses.csv till GitHub"""
    if not GITHUB_TOKEN:
        st.error("GitHub-token saknas! Kontrollera att den är satt i Render's Environment Variables.")
        return

    with open(file_path, "rb") as file:
        content = base64.b64encode(file.read()).decode()

    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha = response.json()["sha"]
    else:
        sha = None  # Filen finns inte än

    data = {
        "message": "Uppdaterar responses.csv med nya inskickade svar",
        "content": content,
        "branch": GITHUB_BRANCH
    }
    if sha:
        data["sha"] = sha  # Behövs för att uppdatera en fil på GitHub

    response = requests.put(url, json=data, headers=headers)

    if response.status_code in [200, 201]:
        st.success("Svaren har sparats och laddats upp till forskningsansvarig!")
    else:
        st.error(f"Något gick fel vid uppladdning: {response.json()}")

# CSS för att ändra bredd på inmatningsfältet för studiekod och behålla stil för andra element
st.markdown("""
    <style>
        .stTextInput {
            max-width: 50% !important;  /* Studiekodens inmatningsruta - 50% av standardstorleken */
        }
        .stRadio {
            margin-left: 20px;  /* Lättare justering för radio-knappar */
        }
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
            margin-left: 25px;
            margin-top: -5px;
        }
        .sub-option-container {
            margin-left: 40px;
        }
        .sub-description {
            font-size: 0.85em;
            color: #555;
            font-style: italic;
            margin-left: 60px;
        }
    </style>
""", unsafe_allow_html=True)

# Fråga om en studiekod och säkerställ att den sparas i rätt format (001-020)
user_code = st.text_input("Ange din studiekod som du får av intervjuaren och tryck enter:")

# Om en kod matas in, konvertera till tre siffror (exempel: "1" → "001", "2" → "002")
if user_code:
    user_code = user_code.zfill(3)  # Se till att koden alltid har tre siffror
    st.success(f"Studiekod registrerad: {user_code}")

# Titel och patientscenario
st.write("""
### Patientscenario 3: Kent Persson, 67 år
Patienten kommer till akuten med bröstsmärta. Han har aldrig haft en hjärninfarkt. Han vet inte om han har hypertoni.
""")

# Huvudalternativ
fhir_main_options = {
    "Bekräftad": "Det finns tillräckligt med bevis för att fastställa förekomsten av patientens tillstånd.",
    "Motbevisad": "Detta tillstånd har uteslutits av efterföljande diagnostiska och kliniska bevis.",
    "Obekräftad": "Det finns inte tillräckligt med bevis för att fastställa förekomsten av patientens tillstånd."
}

# Underalternativ för "Obekräftad"
fhir_suboptions = {
    "Provisorisk": "Detta är en preliminär diagnos - fortfarande en kandidat som övervägs.",
    "Differential": "En av en uppsättning potentiella diagnoser för att vägleda diagnostiska processen."
}

# Funktion för att hantera val
def select_fhir_status(label, key_prefix):
    st.write(f"### {label}")

    options = list(fhir_main_options.keys())

    selected_main = st.radio("Välj status:", options, key=f"{key_prefix}_main", index=None)

    st.markdown('<p class="info-text">(Om du väljer "Obekräftad" måste du välja ett underalternativ)</p>', unsafe_allow_html=True)

    if selected_main:
        st.markdown(f'<p class="description">{fhir_main_options[selected_main]}</p>', unsafe_allow_html=True)

    selected_sub = None
    if selected_main == "Obekräftad":
        st.markdown('<p class="sub-option-container"><strong>Underalternativ för Obekräftad:</strong></p>', unsafe_allow_html=True)

        suboptions = list(fhir_suboptions.keys())

        col1, col2 = st.columns([1, 4])
        with col2:
            selected_sub = st.radio("Välj underalternativ:", suboptions, key=f"{key_prefix}_sub", index=None)

        if selected_sub:
            st.markdown(f'<p class="sub-description">{fhir_suboptions[selected_sub]}</p>', unsafe_allow_html=True)

    if selected_main == "Obekräftad" and selected_sub:
        return f"{selected_main} - {selected_sub}"
    return selected_main

# HL7 FHIR ConditionVerificationStatus
fhir_medication = select_fhir_status("Finns det information om patientens aktuella medicinering i journalen?", "fhir_medication")
fhir_pain = select_fhir_status("Har patienten bröstsmärta?", "fhir_pain")
fhir_bp = select_fhir_status("Har patienten hypertoni?", "fhir_bp")
fhir_braininfarct = select_fhir_status("Har patienten haft en hjärninfarkt tidigare?", "fhir_braininfarct")

# Sammanfattning av valda alternativ
st.write("### Sammanfattning av dokumentation")
st.write(f"- Aktuell medicinering: {fhir_medication if fhir_medication else 'Ej angiven'}")
st.write(f"- Bröstsmärta: {fhir_pain if fhir_pain else 'Ej angiven'}")
st.write(f"- Högt blodtryck: {fhir_bp if fhir_bp else 'Ej angiven'}")
st.write(f"- Hjärninfarkt: {fhir_braininfarct if fhir_braininfarct else 'Ej angiven'}")

# Skicka in svaren
if st.button("Skicka in"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],
        "Aktuell medicinering": [fhir_medication],
        "Bröstsmärta": [fhir_pain],
        "Högt blodtryck": [fhir_bp],
        "Hjärninfarkt": [fhir_braininfarct]
    })

    if os.path.exists(csv_file):
        existing_data = pd.read_csv(csv_file)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(csv_file, index=False)

    # Ladda upp till GitHub
    upload_to_github(csv_file)
