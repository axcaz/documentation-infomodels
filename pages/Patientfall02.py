import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Patientscenario 2 👩‍💻", page_icon="👩‍💻", layout="centered")
st.title("Patientscenario 2")

# 🩺 Patientfall
st.markdown("""
🩺 **Mats Matsson, 73 år**

Du arbetar på akuten och träffar Mats Matsson, 73 år, som söker för nyuppkommen svaghet i ena armen.  
Han har aldrig tidigare haft stroke.  
Han upplevs något förvirrad och är osäker på om han tar blodförtunnande läkemedel.
""")

# 📋 Studiekod
user_code = st.text_input("Ange din studiekod som du får av intervjuaren och tryck enter:")
if user_code:
    user_code = user_code.zfill(3)
    st.success(f"Studiekod registrerad: {user_code}")

# ⚙️ ZIB-koncept – med kompakt stil
problem_status_options = ["(Välj)", "Aktiv", "Inaktiv"]
verification_status_options = ["(Välj)", "Misstänkt", "Känt möjlig", "Bekräftad förekomst", "Känt frånvarande", "Okänt"]

def zib_question(label, key_prefix):
    status = st.radio(f"**{label}:**", problem_status_options, key=f"{key_prefix}_status")

    # Infotext
    if status == "Aktiv":
        st.markdown("<p style='font-size: 0.85em; color: #555; margin-left: 10px;'>Aktivt: Patienten har symtom eller evidens föreligger.</p>", unsafe_allow_html=True)
    elif status == "Inaktiv":
        st.markdown("<p style='font-size: 0.85em; color: #555; margin-left: 10px;'>Inaktivt: Påverkar ej längre patienten eller saknar evidens.</p>", unsafe_allow_html=True)

    verif = st.radio(f"**{label}:**", verification_status_options, key=f"{key_prefix}_ver")
    return status, verif

# ❓ Frågor
arm_status, arm_ver = zib_question("Svaghet i armen", "arm")
stroke_status, stroke_ver = zib_question("Tidigare stroke", "stroke")
blood_status, blood_ver = zib_question("Blodförtunnande läkemedel", "blood")
vision_status, vision_ver = zib_question("Synpåverkan", "vision")

# 📏 Dokumentationssäkerhet
confidence = st.slider("Hur säker är du på din dokumentation?", 1, 7, 4)

# 📝 Sammanfattning
st.subheader("📋 Sammanfattning")
st.write(f"- Svaghet: {arm_status} / {arm_ver}")
st.write(f"- Stroke: {stroke_status} / {stroke_ver}")
st.write(f"- Blodförtunnande: {blood_status} / {blood_ver}")
st.write(f"- Synpåverkan: {vision_status} / {vision_ver}")
st.write(f"- Dokumentationssäkerhet: {confidence}")

# 💾 Spara till responses.csv
csv_file = "responses.csv"
if st.button("Skicka in"):
    if not user_code:
        st.error("Vänligen ange din studiekod.")
    elif any(x == "(Välj)" for x in [arm_status, arm_ver, stroke_status, stroke_ver, blood_status, blood_ver, vision_status, vision_ver]):
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
            "Patientfall": "Fall 2",
            "svaghet": f"{arm_status} / {arm_ver}",
            "stroke": f"{stroke_status} / {stroke_ver}",
            "blodförtunnande": f"{blood_status} / {blood_ver}",
            "synpåverkan": f"{vision_status} / {vision_ver}",
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
