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

# CSS för att ändra bredd på studiekodens inmatningsruta och behålla stil för andra element
st.markdown("""
    <style>
        .stTextInput {
            max-width: 50% !important;  /* Studiekodens inmatningsruta - 50% av standardstorleken */
        }
        .stRadio {
            margin-left: 20px;
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

# Fråga om en studiekod och visa meddelande vid inmatning
user_code = st.text_input("Ange din studiekod som du får av intervjuaren och tryck enter:")
if user_code:
    st.success("Studiekod registrerad!")  # Visar meddelande att studiekoden skickats

# Titel och patientscenario
st.write("""
### Patientscenario 4: Stina Eriksson, 52 år
Patienten söker vårdcentralen för ledsmärta. Hon har aldrig fått diagnosen reumatism. Hon är osäker på om någon i hennes familj har haft liknande besvär.
""")

# Huvudalternativ
diagnostic_security_options = {
    "Misstänkt": "Diagnosen har identifierats med en låg grad av säkerhet.",
    "Sannolik": "Diagnosen har identifierats med en hög grad av säkerhet.",
    "Bekräftad": "Diagnosen har bekräftats mot kända kriterier. **OBS: Detta innebär inte nödvändigtvis att patienten har tillståndet – en bekräftad diagnos kan även vara motbevisad!**"
}

# Alternativ för diagnosstatus (fas i diagnostiseringsprocessen)
diagnosis_phase_options = {
    "Preliminär": "Den initiala diagnosen, vanligtvis kopplad till en låg klinisk säkerhet.",
    "Arbetsdiagnos": "En interimistisk diagnos som kan förändras baserat på nya testresultat.",
    "Fastställd": "Den slutliga och bekräftade diagnosen, förväntas inte ändras.",
    "Motbevisad": "En tidigare registrerad diagnos har omvärderats och motbevisats."
}

# Funktion för att hantera val
def select_status_and_phase(label, key_prefix):
    st.write(f"### {label}")

    # Välj diagnostisk säkerhet
    selected_security = st.radio(
        "Välj diagnostisk säkerhet:", 
        list(diagnostic_security_options.keys()), 
        key=f"{key_prefix}_security",
        index=None
    )

    if selected_security:
        st.markdown(f'<p class="description">{diagnostic_security_options[selected_security]}</p>', unsafe_allow_html=True)

    # Välj diagnosstatus (fas i processen)
    selected_phase = st.radio(
        "Välj diagnosstatus (fas i processen):", 
        list(diagnosis_phase_options.keys()), 
        key=f"{key_prefix}_phase",
        index=None
    )

    if selected_phase:
        st.markdown(f'<p class="description">{diagnosis_phase_options[selected_phase]}</p>', unsafe_allow_html=True)

    return selected_security, selected_phase

# OpenEHR-diagnostisk säkerhet och diagnosstatus för Stina Eriksson
ehr_fever, phase_fever = select_status_and_phase("Har patienten feber?", "ehr_fever")
ehr_inheritance, phase_inheritance = select_status_and_phase("Finns ärftlighet för liknande besvär?", "ehr_inheritance")
ehr_pain, phase_pain = select_status_and_phase("Har patienten ledsmärta?", "ehr_pain")
ehr_rheumatism, phase_rheumatism = select_status_and_phase("Har patienten konstaterad reumatism?", "ehr_rheumatism")

# Sammanfattning av valda alternativ
st.write("### Sammanfattning av dokumentation")
st.write(f"- Feber: {ehr_fever} - {phase_fever}")
st.write(f"- Ärftlighet: {ehr_inheritance} - {phase_inheritance}")
st.write(f"- Ledsmärta: {ehr_pain} - {phase_pain}")
st.write(f"- Reumatism: {ehr_rheumatism} - {phase_rheumatism}")

# Skicka in svaren
if st.button("Skicka in"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],
        "Feber": [f"{ehr_fever} - {phase_fever}" if ehr_fever and phase_fever else "Ej angiven"],
        "Ärftlighet": [f"{ehr_inheritance} - {phase_inheritance}" if ehr_inheritance and phase_inheritance else "Ej angiven"],
        "Ledsmärta": [f"{ehr_pain} - {phase_pain}" if ehr_pain and phase_pain else "Ej angiven"],
        "Reumatism": [f"{ehr_rheumatism} - {phase_rheumatism}" if ehr_rheumatism and phase_rheumatism else "Ej angiven"]
    })

    if os.path.exists(csv_file):
        existing_data = pd.read_csv(csv_file)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(csv_file, index=False)

    # Ladda upp till GitHub
    upload_to_github(csv_file)
