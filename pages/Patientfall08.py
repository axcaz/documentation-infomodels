import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Patientscenario 8 👩‍💻", page_icon="👩‍💻", layout="centered")
st.title("Patientscenario 8")

# 🩺 Patientfall
st.markdown("""
🩺 **Maja Lind, 48 år**

Maja Lind, 48 år, söker vårdcentralen för återkommande yrsel.  
Hon har inte karusellyrsel (att rummet snurrar).  
Hon är osäker på om hon har lågt blodtryck för det var så längesedan hon kontrollerade det.

*Du har i detta fall endast informationen ovan. Utgå från att du litar på patientens berättelse samt inte har mer information för tillfället.*
            """)

# 📋 Studiekod
user_code = st.text_input("Ange din studiekod som du får av intervjuaren och tryck enter:")
if user_code:
    user_code = user_code.zfill(3)
    st.success(f"Studiekod registrerad: {user_code}")

# ✅ Radioknappar utan fritext
def simple_presence_question(label, key):
    options = ["(Välj)", "Ja", "Nej", "Vet ej"]
    return st.radio(label, options, key=key, label_visibility="collapsed")

# ❓ Frågor
st.markdown("**Upplever patienten yrsel?**")
dizziness = simple_presence_question("Upplever patienten yrsel?", "dizziness")

st.markdown("**Upplever patienten karusellyrsel?**")
spinning = simple_presence_question("Upplever patienten karusellyrsel?", "spinning")

st.markdown("**Har patienten lågt blodtryck?**")
low_bp = simple_presence_question("Har patienten lågt blodtryck?", "low_bp")

st.markdown("**Tar patienten någon medicinering?**")
medication = simple_presence_question("Tar patienten någon medicinering?", "medication")

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
st.write(f"- Yrsel: {dizziness}")
st.write(f"- Karusellyrsel: {spinning}")
st.write(f"- Lågt blodtryck: {low_bp}")
st.write(f"- Medicinering: {medication}")
st.write(f"- Dokumentationssäkerhet: {confidence}")

# 💾 Spara i gemensam responses.csv
csv_file = "responses.csv"

if st.button("Skicka in"):
    if not user_code:
        st.error("Vänligen ange din studiekod.")
    elif "(Välj)" in [dizziness, spinning, low_bp, medication]:
        st.error("Vänligen besvara alla frågor.")
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Fyll i tomma kolumner enligt den gemensamma strukturen
        row = {
            "Datum": current_time,
            "Studiekod": user_code,
            "Patientfall": "Fall 8",
            "yrsel": dizziness,
            "karusellyrsel": spinning,
            "lågt blodtryck": low_bp,
            "medicinering": medication,
            "Dokumentationssäkerhet": confidence
        }

        # Lägg till tomma kolumner som inte används i detta fall
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
        for col in all_columns:
            row.setdefault(col, "")

        new_row = pd.DataFrame([row])

        if os.path.exists(csv_file):
            existing = pd.read_csv(csv_file)
            updated = pd.concat([existing, new_row], ignore_index=True)
        else:
            updated = new_row

        updated.to_csv(csv_file, index=False)
        st.success("Svar sparade! ✨")
