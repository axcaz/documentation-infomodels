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
GITHUB_BRANCH = "main"  # Ändra om du använder en annan branch
GITHUB_FILE_PATH = "responses.csv"  # Plats i ditt repo

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

    # Hämta nuvarande filens SHA (nödvändigt för att uppdatera en befintlig fil)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha = response.json()["sha"]
    else:
        sha = None  # Filen finns inte än

    # Skapa JSON-data för att uppdatera filen
    data = {
        "message": "Uppdaterar responses.csv med nya inskickade svar",
        "content": content,
        "branch": GITHUB_BRANCH
    }
    if sha:
        data["sha"] = sha  # Behövs för att uppdatera en fil på GitHub

    # Skicka PUT-request för att ladda upp filen
    response = requests.put(url, json=data, headers=headers)

    if response.status_code in [200, 201]:
        st.success("Svaren har sparats och laddats upp till forskningsansvarig!")
    else:
        st.error(f"Något gick fel vid uppladdning: {response.json()}")

# CSS för layout och checkboxar
st.markdown("""
    <style>
    .stTextInput {
        width: 50% !important;  /* Justerar bredden på studiekods-input */
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
    .checkbox-inline {
        display: inline-flex;
        align-items: center;
        gap: 10px;
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
### Patientscenario 11: Mohammad Rashid, 55 år
Patienten söker för bensvullnad. Han har aldrig haft en djup ventrombos (DVT). 
Han är osäker på om han har hjärtsvikt.
""")

# HL7 FHIR-alternativ (på engelska)
fhir_main_options = {
    "Confirmed": {
        "description": "There is sufficient diagnostic and/or clinical evidence to treat this as a confirmed condition.",
        "suboptions": None
    },
    "Refuted": {
        "description": "This condition has been ruled out by subsequent diagnostic and clinical evidence.",
        "suboptions": None
    },
    "Unconfirmed": {
        "description": "There is not sufficient diagnostic and/or clinical evidence to treat this as a confirmed condition.",
        "suboptions": {
            "Provisional": "This is a tentative diagnosis - still a candidate that is under consideration.",
            "Differential": "One of a set of potential (and typically mutually exclusive) diagnoses asserted to further guide the diagnostic process and preliminary treatment."
        }
    }
}

# Funktion för att hantera kryssrutor med hover-info och korrekt placering av kryssrutan (avstånd 3)
def select_fhir_with_checkbox(label, main_options, key_prefix):
    st.write(f"### {label}")

    selected_main = None
    selected_sub = None

    for option, details in main_options.items():
        col1, col2 = st.columns([3, 1])  
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

            # Om "Unconfirmed" väljs, visa underval
            if option == "Unconfirmed" and details["suboptions"]:
                st.write("#### Välj ett underalternativ:")
                for suboption, sub_desc in details["suboptions"].items():
                    col1, col2 = st.columns([3, 1])  
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

    # Returnera valda alternativ
    if selected_main and selected_sub:
        return f"{selected_main} - {selected_sub}"
    elif selected_main:
        return selected_main
    else:
        return ""

# HL7 FHIR ConditionVerificationStatus – Frågor på svenska
fhir_leg_swelling = select_fhir_with_checkbox("Har patienten svullna ben?", fhir_main_options, "fhir_leg_swelling")
fhir_dvt = select_fhir_with_checkbox("Har patienten haft DVT tidigare?", fhir_main_options, "fhir_dvt")
fhir_heart_failure = select_fhir_with_checkbox("Har patienten hjärtsvikt?", fhir_main_options, "fhir_heart_failure")
fhir_diuretics = select_fhir_with_checkbox("Tar patienten vätskedrivande läkemedel?", fhir_main_options, "fhir_diuretics")

# Sammanfattning av valda alternativ
st.write("### Sammanfattning av dokumentation")
st.write(f"- Bensvullnad: {fhir_leg_swelling if fhir_leg_swelling else 'Ej angiven'}")
st.write(f"- DVT-historik: {fhir_dvt if fhir_dvt else 'Ej angiven'}")
st.write(f"- Hjärtsvikt: {fhir_heart_failure if fhir_heart_failure else 'Ej angiven'}")
st.write(f"- Vätskedrivande: {fhir_diuretics if fhir_diuretics else 'Ej angiven'}")

# Skicka in svaren
if st.button("Skicka in"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],
        "Bensvullnad": [fhir_leg_swelling],
        "DVT-historik": [fhir_dvt],
        "Hjärtsvikt": [fhir_heart_failure],
        "Vätskedrivande": [fhir_diuretics]
    })

    updated_data = new_data if not os.path.exists(csv_file) else pd.concat([pd.read_csv(csv_file), new_data], ignore_index=True)
    updated_data.to_csv(csv_file, index=False)

    # Ladda upp till GitHub
    upload_to_github(csv_file)
