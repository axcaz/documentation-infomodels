import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Patientscenario 3 👩‍💻", page_icon="👩‍💻", layout="centered")
st.title("Patientscenario 3")

# 🩺 Patientbeskrivning
st.markdown("""
🩺 **Kent Persson, 67 år**

När du arbetar kväll på akuten kommer Kent Persson, 67 år, in med ambulans.  
Han söker med akuta buksmärtor. Han har aldrig tidigare haft gallsten.  
Han är osäker på om han har blod i avföringen.

*Du har i detta fall endast informationen ovan. Utgå från att du litar på patientens berättelse samt inte har mer information för tillfället.*
""")

# 📋 Studiekod
user_code = st.text_input("Ange din studiekod som du får av intervjuaren och tryck enter:")
if user_code:
    user_code = user_code.zfill(3)
    st.success(f"Studiekod registrerad: {user_code}")

# 💡 FHIR-frågefunktion
def select_fhir_status(label, key_prefix):
    options = ["(Välj)", "Bekräftad", "Motbevisad", "Obekräftad"]
    suboptions = ["(Välj)", "Provisorisk", "Differential"]

    selected_main = st.radio(f"**{label}**", options, key=f"{key_prefix}_main")

    explanation = {
        "Bekräftad": "Det finns tillräckligt med bevis för att fastställa förekomsten av patientens tillstånd.",
        "Motbevisad": "Tillståndet har uteslutits av efterföljande diagnostiska och kliniska bevis.",
        "Obekräftad": "Det finns inte tillräckligt med bevis för att fastställa förekomsten av tillståndet."
    }

    if selected_main == "Obekräftad":
        st.markdown('<p style="font-size: 0.8rem; color: #0078D7; font-style: italic;">(Om du väljer "Obekräftad" måste du välja ett underalternativ)</p>', unsafe_allow_html=True)

    if selected_main in explanation:
        st.markdown(f'<p style="font-size: 0.85rem; color: #555; font-style: italic;">{explanation[selected_main]}</p>', unsafe_allow_html=True)

    selected_sub = None
    if selected_main == "Obekräftad":
        with st.container():
            st.markdown('<div style="margin-left: 30px;">', unsafe_allow_html=True)
            selected_sub = st.radio("**Underalternativ för Obekräftad:**", suboptions, key=f"{key_prefix}_sub", index=0)
            st.markdown('</div>', unsafe_allow_html=True)

            subdesc = {
                "Provisorisk": "Detta är en preliminär diagnos som fortfarande övervägs.",
                "Differential": "En möjlig diagnos bland flera, för att vägleda vidare utredning."
            }

            if selected_sub in subdesc:
                st.markdown(f'<div style="margin-left: 30px;"><p style="font-size: 0.85rem; color: #555; font-style: italic;">{subdesc[selected_sub]}</p></div>', unsafe_allow_html=True)

    if selected_main == "(Välj)":
        return None
    elif selected_main == "Obekräftad" and selected_sub not in [None, "(Välj)"]:
        return f"{selected_main} - {selected_sub}"
    elif selected_main == "Obekräftad":
        return None
    else:
        return selected_main

# ❓ Frågor
pain = select_fhir_status("Har patienten buksmärta?", "pain")
gallstones = select_fhir_status("Har patienten haft gallsten tidigare?", "gallstones")
blood_stool = select_fhir_status("Har patienten blod i avföringen?", "blood_stool")
chest_pain = select_fhir_status("Har patienten bröstsmärta?", "chest_pain")

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
st.write(f"- Buksmärta: {pain or 'Ej angiven'}")
st.write(f"- Gallsten: {gallstones or 'Ej angiven'}")
st.write(f"- Blod i avföring: {blood_stool or 'Ej angiven'}")
st.write(f"- Bröstsmärta: {chest_pain or 'Ej angiven'}")
st.write(f"- Dokumentationssäkerhet: {confidence}")

# 💾 Spara
csv_file = "responses.csv"

if st.button("Skicka in"):
    if not user_code:
        st.error("Vänligen ange din studiekod.")
    elif None in [pain, gallstones, blood_stool, chest_pain]:
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
            "Patientfall": "Fall 3",
            "buksmärta": pain,
            "gallsten": gallstones,
            "avföring": blood_stool,
            "bröstsmärta": chest_pain,
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
