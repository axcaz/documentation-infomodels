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
        .stSelectbox {
            width: 80% !important;  /* Justerar dropdown-menyerna till 80% */
        }
    </style>
""", unsafe_allow_html=True)

# Fråga om en studiekod och visa meddelande vid inmatning
user_code = st.text_input("Ange din studiekod som du får av intervjuaren och tryck enter:")
if user_code:
    st.success("Studiekod registrerad!")  # Visar meddelande att studiekoden skickats

# Titel och patientscenario
st.write("""
### Patientscenario 5: Lotten Larsson, 29 år
Patienten söker för långvarig hosta och feber. Hon har aldrig haft lunginflammation. Hon är osäker på om hon kanske har astma.
""")

# OpenEHR-alternativ med förvald tom rad
openehr_options = [
    "",  # Tomt alternativ (standard)
    "Finns (Bekräftad diagnos eller tillstånd).",
    "Uteslutet (Tillståndet har aktivt bedömts som frånvarande).",
    "Information saknas (Det finns ingen tillgänglig information om tillståndet).",
    "Preliminärt, Bedömt som kliniskt relevant men inte verifierat.",
    "Arbetsdiagnos, Noterat men bedöms som en möjlig alternativ förklaring."
]

# Funktion för att visa en fråga med dropdown
def select_openehr_status(label, key_prefix):
    st.write(f"### {label}")
    choice = st.selectbox(
        "Välj ett alternativ:",
        openehr_options,
        key=f"{key_prefix}_openehr",
        index=0  # Förvalt tom
    )
    return choice

# OpenEHR Condition-verifikationer för Lotten Larsson
ehr_fever = select_openehr_status("Har patienten feber?", "ehr_fever")
ehr_pneumonia = select_openehr_status("Har patienten en historia av lunginflammation?", "ehr_pneumonia")
ehr_asthma = select_openehr_status("Har patienten astma?", "ehr_asthma")
ehr_smoking = select_openehr_status("Röker patienten?", "ehr_smoking")

# 🔹 **Sammanfattning av valda alternativ**
st.write("### Sammanfattning av dokumentation")
st.write(f"- **Feber:** {ehr_fever if ehr_fever else 'Ej angiven'}")
st.write(f"- **Lunginflammation:** {ehr_pneumonia if ehr_pneumonia else 'Ej angiven'}")
st.write(f"- **Astma:** {ehr_asthma if ehr_asthma else 'Ej angiven'}")
st.write(f"- **Rökning:** {ehr_smoking if ehr_smoking else 'Ej angiven'}")

# Skicka in svaren
if st.button("Skicka in"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],
        "Feber": [ehr_fever if ehr_fever else "Ej angiven"],
        "Lunginflammation": [ehr_pneumonia if ehr_pneumonia else "Ej angiven"],
        "Astma": [ehr_asthma if ehr_asthma else "Ej angiven"],
        "Rökning": [ehr_smoking if ehr_smoking else "Ej angiven"]
    })

    # Spara lokalt först
    if os.path.exists(csv_file):
        existing_data = pd.read_csv(csv_file)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(csv_file, index=False)

    # Ladda upp till GitHub
    upload_to_github(csv_file)
