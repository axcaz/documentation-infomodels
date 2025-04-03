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

*Du har i detta fall endast informationen ovan. Utgå från att du litar på patientens berättelse samt inte har mer information för tillfället.*
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
    "Misstänkt", "Känt möjlig", "Bekräftad förekomst",
    "Känt frånvarande", "Okänt"
]

# 🧠 ZIB-frågefunktion
def zib_radio_question(label, key_prefix):
    st.markdown(f"**{label}**")
    status = st.radio("Status:", problem_status_options, key=f"{key_prefix}_status", label_visibility="collapsed")

    if status == "Aktiv":
        st.markdown("<p style='font-size: 0.85rem; color: #555; margin-left: 10px;'>Aktiva problem är problem där patienten upplever symtom eller problem för vilka det finns evidens.</p>", unsafe_allow_html=True)
    elif status == "Inaktiv":
        st.markdown("<p style='font-size: 0.85rem; color: #555; margin-left: 10px;'>Problem med statusen 'Inaktiv' refererar till problem som inte påverkar patienten längre eller för vilka det inte finns någon evidens att de längre existerar.</p>", unsafe_allow_html=True)

    verification = st.radio("Verifiering:", verification_status_options, key=f"{key_prefix}_ver", label_visibility="collapsed")
    return status, verification

# ❓ Frågor
pain_status, pain_ver = zib_radio_question("Har patienten ryggsmärta?", "pain")
anticoag_status, anticoag_ver = zib_radio_question("Står patienten på antikoagulantia?", "anticoag")
aneurysm_status, aneurysm_ver = zib_radio_question("Finns ärftlighet för aortaaneurysm?", "aneurysm")
hyper_status, hyper_ver = zib_radio_question("Har patienten hypertoni?", "hypertension")

# 📏 Dokumentationssäkerhet
# 🧼 Extra luft före slidern
st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)


st.markdown("<h3 style='margin-top: 3.5rem; margin-bottom: 0.5rem;'> Självskattad upplevelse av dokumentationsstrukturen</h3>", unsafe_allow_html=True)

    # Flytta slidertexten utanför st.slider() för kontroll
st.markdown("<p style='margin-top: -0.5rem;'>📊 Markera på skalan hur du uppfattar den struktur du nyss använde:</p>", unsafe_allow_html=True)

    # Slider utan synliga siffror
confidence = st.slider("", min_value=1, max_value=7, value=4, format=" ")

    # Etiketter under slidern
st.markdown("""
        <div style='font-size: 1rem; color: #1f77b4; font-weight: bold; display: flex; justify-content: space-between; margin-bottom: 1.5rem;'>
            <span>Svårtydd</span>
            <span>Begriplig</span>
        </div>
        """, unsafe_allow_html=True)

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

        all_columns = [
            "Datum", "Studiekod", "Patientfall",
            "nackstelhet", "högt blodtryck", "migrän", "huvudvärk",
            "svaghet", "stroke", "blodförtunnande", "synpåverkan",
            "buksmärta", "gallsten", "avföring", "bröstsmärta",
            "hudutslag", "psoriasis", "ärftlighet utslag", "klåda",
            "feber", "lunginflammation", "astma", "luftvägsinfektion",
            "andfåddhet", "KOL", "betablockerare", "lungröntgen",
            "ryggsmärta", "antikoagulantia", "aortaaneurysm", "hypertoni",
            "yrsel", "karusellyrsel", "lågt blodtryck", "medicinering",
            "Dokumentationssäkerhet"
        ]

        row = {
            "Datum": current_time,
            "Studiekod": user_code,
            "Patientfall": "Fall 7",
            "ryggsmärta": f"{pain_status} / {pain_ver}",
            "antikoagulantia": f"{anticoag_status} / {anticoag_ver}",
            "aortaaneurysm": f"{aneurysm_status} / {aneurysm_ver}",
            "hypertoni": f"{hyper_status} / {hyper_ver}",
            "Dokumentationssäkerhet": confidence
        }

        for col in all_columns:
            row.setdefault(col, "")

        new_data = pd.DataFrame([row])

        if os.path.exists(csv_file):
            existing = pd.read_csv(csv_file)
            updated = pd.concat([existing, new_data], ignore_index=True)
        else:
            updated = new_data

        updated.to_csv(csv_file, index=False)
        st.success("Svar sparade! ✨")
