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
### Patientscenario 7: Erik Eriksson, 62 år
Patienten söker akut för kraftig ryggsmärta mellan skulderbladen som kom plötsligt. 
Han har aldrig rökt. Han är osäker på om någon i familjen haft aneurysm i bröstkorgsaortan.
""")

# NIM-alternativ med förvald "(Välj ett alternativ)"
nim_options = [
    "(Välj ett alternativ)",  
    "Misstänkt",
    "Känt möjligt",
    "Bekräftat närvarande",
    "Känt frånvarande",
    "Okänt"
]

# Funktion för att visa en fråga med dropdown
def select_nim_status(label, key_prefix):
    st.write(f"### {label}")
    choice = st.selectbox(
        "",  
        nim_options,
        key=f"{key_prefix}_nim",
        index=0  
    )
    return choice if choice != "(Välj ett alternativ)" else "Ej angiven"

# NIM-status för Erik Eriksson
nim_pain = select_nim_status("Har patienten ryggsmärta?", "nim_pain")
nim_smoking = select_nim_status("Röker patienten?", "nim_smoking")
nim_aneurysm = select_nim_status("Finns ärftlighet för aortaaneurysm?", "nim_aneurysm")
nim_hypertension = select_nim_status("Har patienten hypertoni?", "nim_hypertension")

# 🔹 **Sammanfattning av valda alternativ**
st.write("### Sammanfattning av dokumentation")
st.write(f"- **Ryggsmärta:** {nim_pain}")
st.write(f"- **Rökning:** {nim_smoking}")
st.write(f"- **Ärftlighet för aortaaneurysm:** {nim_aneurysm}")
st.write(f"- **Hypertoni:** {nim_hypertension}")

# Skicka in svaren
if st.button("Skicka in"):
    # Skapa en rad med svaren
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],
        "Ryggsmärta": [nim_pain],
        "Rökning": [nim_smoking],
        "Ärftlighet för aortaaneurysm": [nim_aneurysm],
        "Hypertoni": [nim_hypertension]
    })

    # Kontrollera om filen redan finns
    if os.path.exists(csv_file):
        existing_data = pd.read_csv(csv_file)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(csv_file, index=False)

    upload_to_github(csv_file)
