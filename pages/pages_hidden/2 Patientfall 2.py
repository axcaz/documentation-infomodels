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

# Lägg till anpassad CSS för att styra bredden
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

# Fråga om en studiekod och visa meddelande vid inmatning
user_code = st.text_input("Ange din studiekod som du får av intervjuaren och tryck enter:")
if user_code:
    st.success("Studiekod registrerad!")  # Visar meddelande att studiekoden skickats

# Titel och introduktion
st.write("""
### Patientscenario 2: Mats Matsson 73 år
Patienten söker för huvudvärk, ramlat för ett par veckor sedan, upplever inga förändringar i synen. Han tror inte han har slagit i huvudet.
""")

# Alternativ med beskrivningar
nim_options = {
    "Misstänkt": "Tillståndet är misstänkt men ännu inte bekräftat.",
    "Känt möjligt": "Tillståndet är känt som en möjlig diagnos, men ej bekräftat.",
    "Bekräftad närvarande": "Tillståndet eller diagnosen har bekräftats som närvarande.",
    "Känt frånvarande": "Tillståndet eller diagnosen är känd att vara frånvarande.",
    "Okänt": "Informationen om tillståndet är okänd eller oidentifierad."
}

# Funktion för att visa en dropdown med ett tomt förvalt alternativ
def select_with_tooltips(label, options, key_prefix):
    st.write(f"### {label}")
    options_with_empty = ["(Välj ett alternativ)"] + list(options.keys())
    selected = st.selectbox("", options_with_empty, key=f"{key_prefix}_selectbox")
    if selected and selected != "(Välj ett alternativ)":
        st.markdown(f"""
            **Valt alternativ:** {selected}  
            ℹ️ **Beskrivning:** {options[selected]}
        """)
    return selected if selected != "(Välj ett alternativ)" else None

# Socialstyrelsens NIM Hälsotillstånd
nim_bloodthinners = select_with_tooltips("Tar patienten blodförtunnande mediciner?", nim_options, "nim_bloodthinners")
nim_headtrauma = select_with_tooltips("Har patienten slagit i huvudet?", nim_options, "nim_headtrauma")
nim_pain = select_with_tooltips("Har patienten huvudvärk?", nim_options, "nim_pain")
nim_eyes = select_with_tooltips("Har patienten synpåverkan?", nim_options, "nim_eyes")

# Sammanfattning av valda alternativ
st.write("### Sammanfattning av dokumentation")
st.write(f"- Blodförtunnande mediciner: {nim_bloodthinners if nim_bloodthinners else 'Ej angiven'}")
st.write(f"- Slagit i huvudet: {nim_headtrauma if nim_headtrauma else 'Ej angiven'}")
st.write(f"- Huvudvärk: {nim_pain if nim_pain else 'Ej angiven'}")
st.write(f"- Synpåverkan: {nim_eyes if nim_eyes else 'Ej angiven'}")

# Skicka in svaren
if st.button("Skicka in"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],
        "Blodförtunnande mediciner": [nim_bloodthinners if nim_bloodthinners else "Ej angivet"],
        "Slagit i huvudet": [nim_headtrauma if nim_headtrauma else "Ej angivet"],
        "Huvudvärk": [nim_pain if nim_pain else "Ej angivet"],
        "Synpåverkan": [nim_eyes if nim_eyes else "Ej angivet"]
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
