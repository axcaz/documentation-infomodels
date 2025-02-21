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
### Patientscenario 9: Olle Jansson, 70 år
Patienten har hosta sedan flera veckor tillbaka. Han har inte KOL. 
Han är osäker på om han haft lunginflammation tidigare.
""")

# Enkla alternativ för dokumentation med förvald "(Välj ett alternativ)"
options = ["(Välj ett alternativ)", "Ja", "Nej", "Vet ej"]

# Funktion för att visa en fråga med stor rubrik och dropdown (utan upprepning)
def document_question(label, key_prefix):
    st.write(f"### {label}")  # Behåller stora rubriken
    return st.selectbox("", options, key=key_prefix, index=0)  # Tar bort liten text i dropdown

# Frågor för Olle Jansson
cough = document_question("Har patienten hosta?", "cough")
copd = document_question("Har patienten KOL?", "copd")
pneumonia = document_question("Har patienten haft lunginflammation?", "pneumonia")
oxygenation = document_question("Hur syresätter sig patienten?", "oxygenation")

# Sammanfattning av data
st.write("### Sammanfattning av dokumentation")
st.write(f"- Hosta: {cough if cough != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- KOL: {copd if copd != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Lunginflammation: {pneumonia if pneumonia != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Syresättning: {oxygenation if oxygenation != '(Välj ett alternativ)' else 'Ej angiven'}")

# Skicka in svaren
if st.button("Skicka in"):
    # Skapa en rad med svaren
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Datum och tid
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],  # Ange koden eller "Ej angiven"
        "Hosta": [cough if cough != "(Välj ett alternativ)" else "Ej angiven"],
        "KOL": [copd if copd != "(Välj ett alternativ)" else "Ej angiven"],
        "Lunginflammation": [pneumonia if pneumonia != "(Välj ett alternativ)" else "Ej angiven"],
        "Syresättning": [oxygenation if oxygenation != "(Välj ett alternativ)" else "Ej angiven"]
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
