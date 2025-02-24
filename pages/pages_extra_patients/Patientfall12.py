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

# CSS för layout och dropdown-menyer
st.markdown("""
    <style>
    .stTextInput {
        width: 50% !important;  /* Justerar bredden på studiekods-input */
    }
    .stSelectbox {
        width: 30% !important;  /* Justerar bredden på dropdown-menyer */
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

# Sammanfattning av valda alternativ
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

    # Kontrollera om filen redan finns
    if os.path.exists(csv_file):
        existing_data = pd.read_csv(csv_file)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    # Spara tillbaka till CSV-filen
    updated_data.to_csv(csv_file, index=False)

    # Ladda upp till GitHub
    upload_to_github(csv_file)
