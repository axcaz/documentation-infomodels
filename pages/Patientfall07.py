import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Patientscenario 7 👩‍💻", page_icon="👩‍💻", layout="centered")
st.title("Patientscenario 7")

# 🩺 Patientbeskrivning
st.markdown("""
🩺 **Erik Eriksson, 62 år**

Du träffar Erik Eriksson, 62 år, när han söker akut för kraftig ryggsmärta mellan skulderbladen som kom plötsligt.  
Han står inte på antikoagulantia.  
Han tror att hans farfar kanske hade något liknande, men är osäker på om någon i familjen haft just aneurysm i bröstkorgsaortan.
""")

# 📋 Studiekod
user_code = st.text_input("Ange din studiekod som du får av intervjuaren och tryck enter:")
if user_code:
    user_code = user_code.zfill(3)
    st.success(f"Studiekod registrerad: {user_code}")

# 🔄 Alternativ
problem_status_options = ["(Välj)", "Aktiv", "Inaktiv"]
verification_status_options = [
    "(Välj klinisk status för problemet eller diagnosen)",
    "Misstänkt", "Känt möjligt", "Bekräftad närvarande",
    "Känt frånvarande", "Okänt"
]

# 🧠 ZIB-frågefunktion
def zib_radio_question(label, key_prefix):
    st.markdown(f"**{label}**")
    status = st.radio("Status:", problem_status_options, key=f"{key_prefix}_status", label_visibility="collapsed")

    if status == "Aktiv":
        st.markdown("<p style='font-size: 0.85rem; color: #555; margin-left: 10px;'>Aktiva problem innebär att patienten har symtom eller att bevis föreligger.</p>", unsafe_allow_html=True)
    elif status == "Inaktiv":
        st.markdown("<p style='font-size: 0.85rem; color: #555; margin-left: 10px;'>Inaktiva problem påverkar inte längre patienten eller har inte längre evidens.</p>", unsafe_allow_html=True)

    verification = st.radio("Verifiering:", verification_status_options, key=f"{key_prefix}_ver", label_visibility="collapsed")
    return status, verification

# ❓ Frågor
pain_status, pain_ver = zib_radio_question("Har patienten ryggsmärta?", "pain")
anticoag_status, anticoag_ver = zib_radio_question("Står patienten på antikoagulantia?", "anticoag")
aneurysm_status, aneurysm_ver = zib_radio_question("Finns ärftlighet för aortaaneurysm?", "aneurysm")
hyper_status, hyper_ver = zib_radio_question("Har patienten hypertoni?", "hypertension")

# 📏 Dokumentationssäkerhet
confidence = st.slider("Hur säker är du på din dokumentation?", 1, 7, 4)

# 📋 Sammanfattning
st.subheader("📋 Sammanfattning")
st.write(f"- Ryggsmärta: {pain_status} / {pain_ver}")
st.write(f"- Antikoagulantia: {anticoag_status} / {anticoag_ver}")
st.write(f"- Aortaaneurysm: {aneurysm_status} / {aneurysm_ver}")
st.write(f"- Hypertoni: {hyper_status} / {hyper_ver}")
st.write(f"- Dokumentationssäkerhet: {confidence}")

# 💾 Spara till responses.csv
csv_file = "responses.csv"
if st.button("Skicka in"):
    if not user_code:
        st.error("Vänligen ange din studiekod.")
    elif any(x == "(Välj)" for x in [
        pain_status, pain_ver, anticoag_status, anticoag_ver,
        aneurysm_status, aneurysm_ver, hyper_status, hyper_ver
    ]):
        st.error("Vänligen besvara alla frågor.")
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = pd.DataFrame({
            "Datum": [current_time],
            "Studiekod": [user_code],
            "Patientfall": ["Fall 7"],
            "ryggsmärta - status": [pain_status],
            "ryggsmärta - verifiering": [pain_ver],
            "antikoagulantia - status": [anticoag_status],
            "antikoagulantia - verifiering": [anticoag_ver],
            "aortaaneurysm - status": [aneurysm_status],
            "aortaaneurysm - verifiering": [aneurysm_ver],
            "hypertoni - status": [hyper_status],
            "hypertoni - verifiering": [hyper_ver],
            "Dokumentationssäkerhet": [confidence]
        })

        if os.path.exists(csv_file):
            existing = pd.read_csv(csv_file)
            data = pd.concat([existing, row], ignore_index=True)
        else:
            data = row

        data.to_csv(csv_file, index=False)
        st.success("Svar sparade! ✨")
