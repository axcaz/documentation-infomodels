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

# Funktion för att läsa in data
def load_data():
    try:
        return pd.read_csv(csv_file)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Datum", "Kod", "Förhöjt blodtryck", "Stroke", "Allergi mot penicillin", "Operation i buken"])

# Funktion för att spara data
def save_data(df):
    df.to_csv(csv_file, index=False)

# Ladda befintlig data
data = load_data()

# Lägg till anpassad CSS för att ändra bredd
st.markdown("""
    <style>
    .stTextInput {
        max-width: 50% !important;  /* Studiekodens inmatningsruta - 50% av standardstorleken */
    }
    .stSelectbox {
        max-width: 30% !important;  /* Behåller selectboxarna på 30% */
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
### Patientscenario 1: Anna Andersson, 45 år
Patienten uppger att hon själv uppmätt förhöjt blodtryck hemma. Hon har aldrig fått diagnosen stroke och har inte haft några kända stroke-relaterade symtom. Det finns en osäkerhet kring eventuell penicillinallergi i barndomen, men ingen tidigare dokumenterad allergisk reaktion.
""")

# Enkla alternativ för dokumentation
options = ["(Välj ett alternativ)", "Ja", "Nej", "Vet ej"]

# Funktion för att visa en fråga med dropdown
def document_question(label):
    return st.selectbox(label, options, index=0)

# Frågor
blood_pressure = document_question("Har patienten förhöjt blodtryck?")
stroke = document_question("Har patienten haft stroke?")
pc_allergy = document_question("Har patienten allergi mot penicillin?")
abdominal_surgery = document_question("Är patienten opererad i buken?")

# Skicka in svaren
if st.button("Skicka in"):
    if user_code:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data = pd.DataFrame({
            "Datum": [current_time],
            "Kod": [user_code],
            "Förhöjt blodtryck": [blood_pressure],
            "Stroke": [stroke],
            "Allergi mot penicillin": [pc_allergy],
            "Operation i buken": [abdominal_surgery]
        })
        data = pd.concat([data, new_data], ignore_index=True)
        save_data(data)

        # Ladda upp filen till GitHub
        upload_to_github(csv_file)
    else:
        st.error("Vänligen ange din studiekod.")

