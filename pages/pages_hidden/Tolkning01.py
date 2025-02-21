import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime
import requests
import base64

# Filnamn för CSV
csv_file = "responses.csv"
tolkning_file = "tolkningar.csv"

# GitHub repo detaljer
GITHUB_REPO = "axcaz/documentation-infomodels"
GITHUB_BRANCH = "main"
GITHUB_FILE_PATH = "tolkningar.csv"
GITHUB_TOKEN = os.getenv("github_token")

# Funktion för att ladda upp fil till GitHub
def upload_to_github(file_path):
    if not GITHUB_TOKEN:
        st.error("GitHub-token saknas! Kontrollera att den är satt i Render's Environment Variables.")
        return
    with open(file_path, "rb") as file:
        content = base64.b64encode(file.read()).decode()
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    sha = response.json()["sha"] if response.status_code == 200 else None
    data = {"message": "Uppdaterar tolkningar.csv", "content": content, "branch": GITHUB_BRANCH}
    if sha:
        data["sha"] = sha
    response = requests.put(url, json=data, headers=headers)
    if response.status_code in [200, 201]:
        st.success("Tolkningen har sparats och laddats upp till forskningsansvarig!")
    else:
        st.error(f"Något gick fel vid uppladdning: {response.json()}")

# CSS för layout
st.markdown("""
    <style>
    .stTextInput { width: 50% !important; }
    .stSelectbox { width: 30% !important; }
    </style>
""", unsafe_allow_html=True)

# Studiekod-input
user_code = st.text_input("Ange din studiekod och tryck enter:")
if user_code:
    st.success("Studiekod registrerad!")

# Ladda tidigare svar
if os.path.exists(csv_file):
    data = pd.read_csv(csv_file)
    if data.empty:
        st.warning("Inga dokumenterade patientfall ännu!")
    else:
        random_row = data.sample(1).iloc[0]
        st.write("### Dokumenterade fynd för tolkning")
        for col in data.columns[2:]:
            st.write(f"- **{col}:** {random_row[col]}")

        # Alternativ för tolkning
        tolkning_options = ["Misstänkt diagnos", "Bekräftad diagnos", "Trolig differentialdiagnos", "Oklar betydelse"]
        user_interpretation = st.selectbox("Hur tolkar du dokumentationen?", tolkning_options, index=0)

        # Skicka in tolkningen
        if st.button("Skicka in tolkning"):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_tolkning = pd.DataFrame({
                "Datum": [current_time],
                "Kod": [user_code if user_code else "Ej angiven"],
                "Tolkning": [user_interpretation],
                "Referens-ID": [random_row["Kod"]]  # Koppla till original
            })
            if os.path.exists(tolkning_file):
                existing_tolkningar = pd.read_csv(tolkning_file)
                updated_tolkningar = pd.concat([existing_tolkningar, new_tolkning], ignore_index=True)
            else:
                updated_tolkningar = new_tolkning
            updated_tolkningar.to_csv(tolkning_file, index=False)
            upload_to_github(tolkning_file)

# Visa sammanfattning av tolkningar
if os.path.exists(tolkning_file):
    tolkningar = pd.read_csv(tolkning_file)
    st.write("### Sammanfattning av inskickade tolkningar")
    st.write(tolkningar)
