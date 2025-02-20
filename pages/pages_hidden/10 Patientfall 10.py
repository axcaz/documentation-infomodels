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

# Lägg till anpassad CSS för att minska bredden på dropdown-menyerna
st.markdown("""
    <style>
    .stSelectbox {
        width: 30% !important;  /* Justerar bredden till 30% */
    }
    .stTextInput {
        width: 50% !important;  /* Justerar bredden på studiekods-input */
    }
    </style>
    """, unsafe_allow_html=True)

# Fråga om studiekod
user_code = st.text_input("Ange din studiekod och tryck enter:")

# Visa meddelande om att studiekoden har skickats
if user_code:
    st.success("Studiekod registrerad!")

# Titel och patientscenario
st.write("""
### Patientscenario 10: Fia Andersson, 34 år
Patienten söker för magont. Hon har inte celiaki. 
Hon är osäker på om hennes smärtor kan bero på laktosintolerans.
""")

# NIM-alternativ med förvald "(Välj ett alternativ)"
nim_options = [
    "(Välj ett alternativ)",  # Förvalt alternativ
    "Misstänkt",
    "Känt möjligt",
    "Bekräftat närvarande",
    "Känt frånvarande",
    "Okänt"
]

# Funktion för att visa en fråga med dropdown
def select_nim_status(label, key_prefix):
    st.write(f"### {label}")  # Behåller rubriken
    choice = st.selectbox(
        "",  # Tar bort rubriken ovanför dropdown-menyn
        nim_options,
        key=f"{key_prefix}_nim",
        index=0  # Förvalt som "(Välj ett alternativ)"
    )
    return choice

# NIM-status för Fia Andersson
nim_pain = select_nim_status("Har patienten magont?", "nim_pain")
nim_celiac = select_nim_status("Har patienten celiaki?", "nim_celiac")
nim_lactose = select_nim_status("Har patienten laktosintolerans?", "nim_lactose")
nim_diarrhea = select_nim_status("Har patienten diarré?", "nim_diarrhea")

# Sammanfattning av data
st.write("### Sammanfattning av dokumentation")
st.write(f"- Magont: {nim_pain if nim_pain != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Celiaki: {nim_celiac if nim_celiac != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Laktosintolerans: {nim_lactose if nim_lactose != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Diarré: {nim_diarrhea if nim_diarrhea != '(Välj ett alternativ)' else 'Ej angiven'}")

# Skicka in svaren
if st.button("Skicka in"):
    # Skapa en rad med svaren
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Datum och tid
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],  # Ange koden eller "Ej angiven"
        "Magont": [nim_pain if nim_pain != "(Välj ett alternativ)" else "Ej angiven"],
        "Celiaki": [nim_celiac if nim_celiac != "(Välj ett alternativ)" else "Ej angiven"],
        "Laktosintolerans": [nim_lactose if nim_lactose != "(Välj ett alternativ)" else "Ej angiven"],
        "Diarré": [nim_diarrhea if nim_diarrhea != "(Välj ett alternativ)" else "Ej angiven"]
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

    # Ladda upp till GitHub
    upload_to_github(csv_file)
