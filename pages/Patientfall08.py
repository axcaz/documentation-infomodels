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

# CSS för layout och stil
st.markdown("""
    <style>
        .stTextInput {
            max-width: 50% !important;  /* Studiekodens inmatningsruta - 50% */
        }
        .stSelectbox {
            width: 30% !important;  /* Svarsalternativen i dropdown-menyerna - 30% */
        }
    </style>
""", unsafe_allow_html=True)

# Fråga om studiekod och visa meddelande vid registrering
user_code = st.text_input("Ange din studiekod som du får av intervjuaren och tryck enter:")
if user_code:
    st.success("Studiekod registrerad!")

# Titel och patientscenario
st.write("""
### Patientscenario 8: Maja Lind, 48 år
Patienten söker vårdcentralen för yrsel. Hon har aldrig haft migrän. Hon är osäker på om hon har lågt blodtryck. 
Det finns ingen information om hon tar blodförtunnande läkemedel.
""")

# Enkla alternativ för dokumentation med förvald "(Välj ett alternativ)"
options = ["(Välj ett alternativ)", "Ja", "Nej", "Vet ej"]

# Funktion för att visa en fråga med dropdown
def document_question(label, key_prefix):
    st.write(f"### {label}")  
    return st.selectbox("", options, key=key_prefix, index=0)  

# Frågor för Maja Lind
dizziness = document_question("Upplever patienten yrsel?", "dizziness")
migraine = document_question("Har patienten migrän?", "migraine")
low_bp = document_question("Har patienten lågt blodtryck?", "low_bp")
anticoagulants = document_question("Står patienten på blodförtunnande medicinering?", "anticoagulants")

# 🔹 **Sammanfattning av valda alternativ**
st.write("### Sammanfattning av dokumentation")
st.write(f"- **Yrsel:** {dizziness if dizziness != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- **Migrän:** {migraine if migraine != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- **Lågt blodtryck:** {low_bp if low_bp != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- **Blodförtunnande medicinering:** {anticoagulants if anticoagulants != '(Välj ett alternativ)' else 'Ej angiven'}")

# Skicka in svaren
if st.button("Skicka in"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],
        "Yrsel": [dizziness if dizziness != "(Välj ett alternativ)" else "Ej angiven"],
        "Migrän": [migraine if migraine != "(Välj ett alternativ)" else "Ej angiven"],
        "Lågt blodtryck": [low_bp if low_bp != "(Välj ett alternativ)" else "Ej angiven"],
        "Blodförtunnande medicinering": [anticoagulants if anticoagulants != "(Välj ett alternativ)" else "Ej angiven"]
    })

    # Kontrollera om filen redan finns
    if os.path.exists(csv_file):
        existing_data = pd.read_csv(csv_file)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(csv_file, index=False)

    upload_to_github(csv_file)
