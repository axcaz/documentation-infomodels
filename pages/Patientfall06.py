import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import base64
import os

# Filnamn för CSV
csv_file = "responses.csv"

# GitHub repo detaljer
GITHUB_REPO = "axcaz/documentation-infomodels"  
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

# CSS för layout och stil
st.markdown("""
    <style>
        .stTextInput {
            max-width: 50% !important;  /* Studiekodens inmatningsruta - 50% */
        }
        .checkbox-label {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 16px;
        }
        .tooltip {
            position: relative;
            display: inline-block;
            cursor: pointer;
            font-weight: 
        }
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 250px;
            background-color: black;
            color: #fff;
            text-align: center;
            padding: 5px;
            border-radius: 5px;
            position: absolute;
            z-index: 1;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            opacity: 0;
            transition: opacity 0.3s;
        }
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
    </style>
""", unsafe_allow_html=True)

# Fråga om studiekod och visa meddelande vid registrering
user_code = st.text_input("Ange din studiekod som du får av intervjuaren och tryck enter:")
if user_code:
    st.success("Studiekod registrerad!")

# Titel och patientscenario
st.write("""
### Patientscenario 6: Aaro Niemi, 80 år
Aaro, från Finland, inkommer till sjukhuset med svår andfåddhet när han hälsar på sitt barnbarn i Stockholm. 
Han har aldrig haft astma. Han tar någon medicin pga tidigare hjärtinfarkt men minns inte namnet. 
Han gjorde en lungröntgen i Helsingfors för någon månad sedan.
""")

# HL7 FHIR-alternativ med hierarki
fhir_main_options = {
    "Bekräftad": {
        "description": "Det finns tillräckligt med diagnostiska och kliniska bevis för att fastställa tillståndet.",
        "suboptions": None
    },
    "Motbevisad": {
        "description": "Detta tillstånd har uteslutits genom kliniska och diagnostiska bevis.",
        "suboptions": None
    },
    "Obekräftad": {
        "description": "Det finns inte tillräckliga bevis för att bekräfta tillståndet.",
        "suboptions": {
            "Provisorisk": "En preliminär diagnos - fortfarande under utredning.",
            "Differential": "En av flera möjliga diagnoser för att vägleda behandling och fortsatt utredning."
        }
    }
}

# Funktion för att hantera kryssrutor med beskrivningar
def select_fhir_with_checkbox(label, main_options, key_prefix):
    st.write(f"### {label}")

    selected_main = None
    selected_sub = None

    for option, details in main_options.items():
        col1, col2 = st.columns([3, 1])  # Layout: Text + Checkbox
        with col1:
            st.markdown(f"""
            <div class="tooltip">{option}
                <span class="tooltiptext">{details['description']}</span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            checked = st.checkbox("", key=f"{key_prefix}_{option}")

        if checked:
            selected_main = option

            if option == "Obekräftad" and details["suboptions"]:
                st.write("#### Välj ett underalternativ:")
                for suboption, sub_desc in details["suboptions"].items():
                    col1, col2 = st.columns([3, 1])  # Samma layout här
                    with col1:
                        st.markdown(f"""
                        <div class="tooltip">{suboption}
                            <span class="tooltiptext">{sub_desc}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        sub_checked = st.checkbox("", key=f"{key_prefix}_{suboption}")

                    if sub_checked:
                        selected_sub = suboption

    if selected_main and selected_sub:
        return f"{selected_main} - {selected_sub}"
    elif selected_main:
        return selected_main
    else:
        return ""

# HL7 FHIR ConditionVerificationStatus
fhir_dyspnea = select_fhir_with_checkbox("Är patienten andfådd?", fhir_main_options, "fhir_dyspnea")
fhir_asthma = select_fhir_with_checkbox("Har patienten astma?", fhir_main_options, "fhir_asthma")
fhir_beta_blockers = select_fhir_with_checkbox("Tar patienten betablockerare?", fhir_main_options, "fhir_beta_blockers")
fhir_lung_scan = select_fhir_with_checkbox("Vad visar lungröntgen?", fhir_main_options, "fhir_lung_scan")

# 🔹 **Sammanfattning av valda alternativ**
st.write("### Sammanfattning av dokumentation")
st.write(f"- **Andfåddhet:** {fhir_dyspnea if fhir_dyspnea else 'Ej angiven'}")
st.write(f"- **Astma:** {fhir_asthma if fhir_asthma else 'Ej angiven'}")
st.write(f"- **Betablockerare:** {fhir_beta_blockers if fhir_beta_blockers else 'Ej angiven'}")
st.write(f"- **Lungröntgen:** {fhir_lung_scan if fhir_lung_scan else 'Ej angiven'}")

# Skicka in svaren
if st.button("Skicka in"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],
        "Andfåddhet": [fhir_dyspnea],
        "Astma": [fhir_asthma],
        "Betablockerare": [fhir_beta_blockers],
        "Lungröntgen": [fhir_lung_scan]
    })

    if os.path.exists(csv_file):
        existing_data = pd.read_csv(csv_file)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(csv_file, index=False)

    upload_to_github(csv_file)
