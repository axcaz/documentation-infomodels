import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Patientscenario 1 👩‍💻", page_icon="👩‍💻", layout="centered")
st.title("Patientscenario 1")

# 🩺 Patientfall
st.markdown("""
🩺 **Anna Andersson, 70 år**

Du är vårdpersonal på vårdcentral och möter Anna Andersson, 70, som söker för konstant huvudvärk som varierar i styrka.  
Hon har aldrig fått diagnosen migrän.  
Hon är osäker på om hon har högt blodtryck, eftersom det var länge sedan hon kontrollerade det.

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
    return st.radio(f"**{label}**", options, key=key)

# ❓ Frågor
headache = simple_presence_question("Upplever patienten huvudvärk?", "headache")
migraine = simple_presence_question("Har patienten diagnosen migrän?", "migraine")
hypertension = simple_presence_question("Har patienten högt blodtryck?", "hypertension")
stiff_neck = simple_presence_question("Upplever patienten nackstelhet?", "stiff_neck")

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
st.write(f"- Huvudvärk: {headache}")
st.write(f"- Migrän: {migraine}")
st.write(f"- Högt blodtryck: {hypertension}")
st.write(f"- Nackstelhet: {stiff_neck}")
st.write(f"- Dokumentationssäkerhet: {confidence}")

# 💾 Spara
csv_file = "responses.csv"  

if st.button("Skicka in"):
    if not user_code:
        st.error("Vänligen ange din studiekod.")
    elif "(Välj)" in [headache, migraine, hypertension, stiff_neck]:
        st.error("Vänligen svara på alla frågor.")
    else:
        row = pd.DataFrame({
            "Datum": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Studiekod": [user_code],
            "Patientfall": ["Fall 1"],
            "Dokumentationssäkerhet": [confidence],
            # Patientfall 1
            "huvudvärk": [headache],
            "migrän": [migraine],
            "högt blodtryck": [hypertension],
            "nackstelhet": [stiff_neck],
            # Alla övriga variabler lämnas tomma
            "svaghet": [""], "stroke": [""], "blodförtunnande": [""], "synpåverkan": [""],
            "buksmärta": [""], "gallsten": [""], "avföring": [""], "bröstsmärta": [""],
            "hudutslag": [""], "psoriasis": [""], "ärftlighet utslag": [""], "klåda": [""],
            "feber": [""], "lunginflammation": [""], "astma": [""], "luftvägsinfektion": [""],
            "andfåddhet": [""], "KOL": [""], "betablockerare": [""], "lungröntgen": [""],
            "ryggsmärta": [""], "antikoagulantia": [""], "aortaaneurysm": [""], "hypertoni": [""],
            "yrsel": [""], "karusellyrsel": [""], "lågt blodtryck": [""], "medicinering": [""]
        })

        if os.path.exists(csv_file):
            existing = pd.read_csv(csv_file)
            data = pd.concat([existing, row], ignore_index=True)
        else:
            data = row

        data.to_csv(csv_file, index=False)
        st.success("Svar sparade! ✨")
