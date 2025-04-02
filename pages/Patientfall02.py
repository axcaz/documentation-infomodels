import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import base64
import os

# Filnamn och GitHub-setup
csv_file = "responses.csv"
GITHUB_REPO = "axcaz/documentation-infomodels"
GITHUB_BRANCH = "main"
GITHUB_FILE_PATH = "responses.csv"
GITHUB_TOKEN = os.getenv("github_token")

# GitHub-upload
def upload_to_github(file_path):
    if not GITHUB_TOKEN:
        st.error("GitHub-token saknas! Kontrollera Render.")
        return

    with open(file_path, "rb") as file:
        content = base64.b64encode(file.read()).decode()

    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    sha = response.json()["sha"] if response.status_code == 200 else None

    data = {
        "message": "Uppdaterar responses.csv med nya inskickade svar",
        "content": content,
        "branch": GITHUB_BRANCH
    }
    if sha:
        data["sha"] = sha

    response = requests.put(url, json=data, headers=headers)
    if response.status_code in [200, 201]:
        st.success("Svaren har sparats och laddats upp!")
    else:
        st.error(f"Något gick fel: {response.json()}")

# Datahantering
def load_data():
    try:
        return pd.read_csv(csv_file)
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "Datum", "Kod",
            "Arm-svaghet - Status", "Arm-svaghet - Verifiering",
            "Tidigare stroke - Status", "Tidigare stroke - Verifiering",
            "Blodförtunnande - Status", "Blodförtunnande - Verifiering",
            "Synpåverkan - Status", "Synpåverkan - Verifiering",
            "Dokumentationssäkerhet"
        ])

def save_data(df):
    df.to_csv(csv_file, index=False)

data = load_data()

st.set_page_config(page_title="Patientscenario 2 – Mats Matsson", layout="centered")
st.title("Patientscenario 2")

# Patientfall
st.markdown("""
🩺 **Mats Matsson, 73 år**

Du arbetar på akuten och träffar Mats Matsson 73 år, som söker för nyuppkommen svaghet i ena armen.  
Han har aldrig tidigare haft stroke. Han upplevs något förvirrad och är osäker på om han tar blodförtunnande läkemedel.
""")

# CSS för konsekvent stil
st.markdown("""
<style>
    .description {
        font-size: 0.85rem;
        color: #555;
        font-style: italic;
    }
    .info-text {
        font-size: 0.8rem;
        color: #0078D7;
        font-style: italic;
        margin-top: -5px;
    }
</style>
""", unsafe_allow_html=True)

# Studiekod
user_code = st.text_input("Ange din studiekod som du får av intervjuaren och tryck enter:")
if user_code:
    user_code = user_code.zfill(3)
    st.success(f"Studiekod registrerad: {user_code}")

# Alternativ
problem_status_options = ["(Välj)", "Aktiv", "Inaktiv"]
verification_status_options = [
    "(Välj klinisk status för problemet eller diagnosen)",
    "Misstänkt", "Känt möjligt", "Bekräftad närvarande",
    "Känt frånvarande", "Okänt"
]

# Funktion för ZIB-liknande struktur
def zib_radio_question(label, key_prefix):
    # Fråga direkt i första radio
    status = st.radio(f"**{label}**", problem_status_options, key=f"{key_prefix}_status")

    # Beskrivning efter val
    if status == "Aktiv":
        st.markdown("<p class='description'>Aktiva problem innebär att patienten har symtom eller att bevis föreligger.</p>", unsafe_allow_html=True)
    elif status == "Inaktiv":
        st.markdown("<p class='description'>Inaktiva problem påverkar inte längre patienten eller har inte längre evidens.</p>", unsafe_allow_html=True)

    # Andra radio – verifiering
    ver = st.radio("**Verifieringsstatus:**", verification_status_options, key=f"{key_prefix}_ver")
    return status, ver

# Frågor
arm_status, arm_ver = zib_radio_question("Har patienten svaghet i armen?", "arm")
stroke_status, stroke_ver = zib_radio_question("Har patienten tidigare diagnostiserats med stroke?", "stroke")
blood_status, blood_ver = zib_radio_question("Tar patienten blodförtunnande läkemedel?", "blood")
vision_status, vision_ver = zib_radio_question("Har patienten synpåverkan?", "vision")

# Skala för säkerhet
confidence = st.slider("Hur säker är du på din dokumentation?", 1, 7, 4)

# Sammanfattning
st.subheader("📋 Sammanfattning")
st.write(f"- Arm-svaghet: {arm_status} / {arm_ver}")
st.write(f"- Tidigare stroke: {stroke_status} / {stroke_ver}")
st.write(f"- Blodförtunnande: {blood_status} / {blood_ver}")
st.write(f"- Synpåverkan: {vision_status} / {vision_ver}")
st.write(f"- Dokumentationssäkerhet: {confidence}")

# Skicka in
if st.button("Skicka in"):
    if not user_code:
        st.error("Vänligen ange din studiekod.")
    elif any(x == "(Välj)" for x in [arm_status, arm_ver, stroke_status, stroke_ver, blood_status, blood_ver, vision_status, vision_ver]):
        st.error("Besvara alla frågor innan du skickar in.")
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data = pd.DataFrame({
            "Datum": [current_time],
            "Kod": [user_code],
            "Arm-svaghet - Status": [arm_status],
            "Arm-svaghet - Verifiering": [arm_ver],
            "Tidigare stroke - Status": [stroke_status],
            "Tidigare stroke - Verifiering": [stroke_ver],
            "Blodförtunnande - Status": [blood_status],
            "Blodförtunnande - Verifiering": [blood_ver],
            "Synpåverkan - Status": [vision_status],
            "Synpåverkan - Verifiering": [vision_ver],
            "Dokumentationssäkerhet": [confidence]
        })
        data = pd.concat([data, new_data], ignore_index=True)
        save_data(data)
        upload_to_github(csv_file)
