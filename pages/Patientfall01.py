import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import base64
import os

# GitHub och CSV
csv_file = "responses.csv"
GITHUB_REPO = "axcaz/documentation-infomodels"
GITHUB_BRANCH = "main"
GITHUB_FILE_PATH = "responses.csv"
GITHUB_TOKEN = os.getenv("github_token")

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
        "branch": GITHUB_BRANCH,
    }
    if sha:
        data["sha"] = sha

    response = requests.put(url, json=data, headers=headers)

    if response.status_code in [200, 201]:
        st.success("Svaren har sparats och laddats upp!")
    else:
        st.error(f"Något gick fel vid uppladdning: {response.json()}")

def load_data():
    try:
        return pd.read_csv(csv_file)
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "Datum", "Kod", "Huvudvärk", "Migrän", "Högt blodtryck", "Nackstelhet", "Dokumentationssäkerhet"
        ])

def save_data(df):
    df.to_csv(csv_file, index=False)

data = load_data()

st.set_page_config(page_title="Patientscenario 1 – Anna Andersson", layout="centered")
st.title("Patientscenario 1")

# ✏️ Patientfall
st.markdown("""
🩺 **Anna Andersson, 70 år**

Du är vårdpersonal på vårdcentral och möter Anna Andersson, 70, som söker för konstant huvudvärk som varierar i styrka.  
Hon har aldrig fått diagnosen migrän. Hon är osäker på om hon har högt blodtryck, eftersom det var länge sedan hon kontrollerade det.
""")

# 💬 Studiekod
user_code = st.text_input("Ange din studiekod som du får av intervjuaren och tryck enter:")
if user_code:
    user_code = user_code.zfill(3)
    st.success(f"Studiekod registrerad: {user_code}")

# 🎯 Alternativ
alternativ = ["(Välj)", "Ja", "Nej", "Vet ej"]

# 💡 Frågor i Stina-style
headache = st.radio("**Upplever patienten huvudvärk?**", alternativ, key="headache")
migraine = st.radio("**Har patienten diagnosen migrän?**", alternativ, key="migraine")
hypertension = st.radio("**Har patienten högt blodtryck?**", alternativ, key="hypertension")
stiff_neck = st.radio("**Upplever patienten nackstelhet?**", alternativ, key="stiff_neck")

# 📏 Dokumentationssäkerhet
confidence = st.slider("Hur säker är du på din dokumentation?", 1, 7, 4)

# 📝 Sammanfattning
st.subheader("📋 Sammanfattning av dokumentation")
st.write(f"- Huvudvärk: {headache or 'Ej angiven'}")
st.write(f"- Migrän: {migraine or 'Ej angiven'}")
st.write(f"- Högt blodtryck: {hypertension or 'Ej angiven'}")
st.write(f"- Nackstelhet: {stiff_neck or 'Ej angiven'}")
st.write(f"- Dokumentationssäkerhet: {confidence}")

# 🚀 Skicka in
if st.button("Skicka in"):
    if not user_code:
        st.error("Vänligen ange din studiekod.")
    elif any(x == "(Välj)" or x is None for x in [headache, migraine, hypertension, stiff_neck]):
        st.error("Vänligen besvara alla frågor.")
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data = pd.DataFrame({
            "Datum": [current_time],
            "Kod": [user_code],
            "Huvudvärk": [headache],
            "Migrän": [migraine],
            "Högt blodtryck": [hypertension],
            "Nackstelhet": [stiff_neck],
            "Dokumentationssäkerhet": [confidence]
        })
        data = pd.concat([data, new_data], ignore_index=True)
        save_data(data)
        upload_to_github(csv_file)
