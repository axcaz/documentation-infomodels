import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Patientscenario 7 – Erik Eriksson", layout="centered")
st.title("Patientscenario 7")

# ✏️ Patientfall
st.markdown("""
🩺 **Erik Eriksson, 62 år**

Du träffar Erik Eriksson, 62 år, när han söker akut för kraftig ryggsmärta mellan skulderbladen som kom plötsligt.  
Han står inte på antikoagulantia.  
Han tror att hans farfar kanske hade något liknande, men är osäker på om någon i familjen haft just aneurysm i bröstkorgsaortan.
""")

# 💬 Studiekod
user_code = st.text_input("Ange din studiekod som du får av intervjuaren och tryck enter:")
if user_code:
    user_code = user_code.zfill(3)
    st.success(f"Studiekod registrerad: {user_code}")

# 📋 Alternativ
problem_status_options = ["(Välj)", "Aktiv", "Inaktiv"]
verification_status_options = [
    "(Välj klinisk status för problemet eller diagnosen)",
    "Misstänkt", "Känt möjligt", "Bekräftad närvarande",
    "Känt frånvarande", "Okänt"
]

# 💡 Funktion: ZIB-fråga med 2 radioknappar + infotext
def zib_radio_question(label, key_prefix):
    st.markdown(f"**{label}**")
    status = st.radio("Problemstatus:", problem_status_options, key=f"{key_prefix}_status")

    if status == "Aktiv":
        st.markdown("<p style='font-size: 0.85em; color: #555; font-style: italic;'>Aktivt: Patienten upplever symtom eller evidens finns för tillståndet.</p>", unsafe_allow_html=True)
    elif status == "Inaktiv":
        st.markdown("<p style='font-size: 0.85em; color: #555; font-style: italic;'>Inaktivt: Påverkar ej längre patienten eller har ingen evidens längre.</p>", unsafe_allow_html=True)

    verification = st.radio("Verifieringsstatus:", verification_status_options, key=f"{key_prefix}_ver")

    return status, verification

# ❓ Frågor
pain_status, pain_ver = zib_radio_question("Har patienten ryggsmärta?", "pain")
anticoag_status, anticoag_ver = zib_radio_question("Står patienten på antikoagulantia?", "anticoag")
hered_status, hered_ver = zib_radio_question("Finns ärftlighet för aortaaneurysm?", "heredity")
hyper_status, hyper_ver = zib_radio_question("Har patienten hypertoni?", "hypertension")

# 📏 Dokumentationssäkerhet
confidence = st.slider("Hur säker är du på din dokumentation?", 1, 7, 4)

# 📋 Sammanfattning
st.subheader("📋 Sammanfattning")
st.write(f"- Ryggsmärta: {pain_status} / {pain_ver}")
st.write(f"- Antikoagulantia: {anticoag_status} / {anticoag_ver}")
st.write(f"- Ärftlighet aortaaneurysm: {hered_status} / {hered_ver}")
st.write(f"- Hypertoni: {hyper_status} / {hyper_ver}")
st.write(f"- Dokumentationssäkerhet: {confidence}")

# 💾 Spara till CSV
csv_file = "erik_eriksson_svar.csv"

if st.button("Skicka in"):
    if not user_code:
        st.error("Vänligen ange din studiekod.")
    elif any(x == "(Välj)" for x in [pain_status, pain_ver, anticoag_status, anticoag_ver, hered_status, hered_ver, hyper_status, hyper_ver]):
        st.error("Vänligen besvara alla frågor.")
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = pd.DataFrame({
            "Datum": [current_time],
            "Kod": [user_code],
            "Ryggsmärta - Status": [pain_status],
            "Ryggsmärta - Verifiering": [pain_ver],
            "Antikoagulantia - Status": [anticoag_status],
            "Antikoagulantia - Verifiering": [anticoag_ver],
            "Ärftlighet - Status": [hered_status],
            "Ärftlighet - Verifiering": [hered_ver],
            "Hypertoni - Status": [hyper_status],
            "Hypertoni - Verifiering": [hyper_ver],
            "Dokumentationssäkerhet": [confidence]
        })

        if os.path.exists(csv_file):
            existing = pd.read_csv(csv_file)
            data = pd.concat([existing, row], ignore_index=True)
        else:
            data = row

        data.to_csv(csv_file, index=False)
        st.success("Svar sparade! ✨")
