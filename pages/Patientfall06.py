import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Patientscenario 6 👩‍💻", page_icon="👩‍💻", layout="centered")
st.title("Patientscenario 6")

# 🩺 Patientbeskrivning
st.markdown("""
🩺 **Aaro Niemi, 80 år**

Aaro, från Finland, inkommer till sjukhuset med svår andfåddhet när han hälsar på sitt barnbarn i Stockholm.  
Han har aldrig haft KOL. Han tar någon medicin pga tidigare hjärtinfarkt men minns inte namnet.  
Han gjorde en lungröntgen i Helsingfors för någon månad sedan.
            
*Du har i detta fall endast informationen ovan. Utgå från att du litar på patientens berättelse samt inte har mer information för tillfället.*
""")

# 📋 Studiekod
user_code = st.text_input("Ange din studiekod som du får av intervjuaren och tryck enter:")
if user_code:
    user_code = user_code.zfill(3)
    st.success(f"Studiekod registrerad: {user_code}")

# 💡 Funktion för FHIR-frågor med indrag och förklaringar
def select_fhir_status(label, key_prefix):
    options = ["(Välj)", "Bekräftad", "Motbevisad", "Obekräftad"]
    suboptions = ["(Välj)", "Provisorisk", "Differential"]

    selected_main = st.radio(f"**{label}**", options, key=f"{key_prefix}_main")

    explanation = {
        "Bekräftad": "Det finns tillräckligt med bevis för att fastställa förekomsten av tillståndet.",
        "Motbevisad": "Tillståndet har uteslutits av efterföljande diagnostiska och kliniska bevis.",
        "Obekräftad": "Det finns inte tillräckligt med bevis för att fastställa förekomsten av tillståndet."
    }

    if selected_main == "Obekräftad":
        st.markdown('<p style="font-size: 0.85rem; color: #0078D7; font-style: italic;">'
                    '(Om du väljer "Obekräftad" måste du välja ett underalternativ)</p>', unsafe_allow_html=True)

    if selected_main in explanation:
        st.markdown(f'<p style="font-size: 0.85rem; color: #555; font-style: italic;">{explanation[selected_main]}</p>',
                    unsafe_allow_html=True)

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
                st.markdown(f'<div style="margin-left: 30px;"><p style="font-size: 0.85rem; color: #555; font-style: italic;">{subdesc[selected_sub]}</p></div>',
                            unsafe_allow_html=True)

    if selected_main == "(Välj)":
        return None
    elif selected_main == "Obekräftad" and selected_sub not in [None, "(Välj)"]:
        return f"{selected_main} - {selected_sub}"
    elif selected_main == "Obekräftad":
        return None
    else:
        return selected_main

# ❓ Frågor
dyspnea = select_fhir_status("Är patienten andfådd?", "dyspnea")
copd = select_fhir_status("Har patienten KOL?", "copd")
beta_blockers = select_fhir_status("Tar patienten betablockerare?", "beta_blockers")
lung_scan = select_fhir_status("Visar lungröntgen något?", "lung_scan")

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
st.write(f"- Andfåddhet: {dyspnea or 'Ej angiven'}")
st.write(f"- KOL: {copd or 'Ej angiven'}")
st.write(f"- Betablockerare: {beta_blockers or 'Ej angiven'}")
st.write(f"- Lungröntgen: {lung_scan or 'Ej angiven'}")
st.write(f"- Dokumentationssäkerhet: {confidence}")

# 💾 Spara
csv_file = "responses.csv"

if st.button("Skicka in"):
    if not user_code:
        st.error("Vänligen ange din studiekod.")
    elif None in [dyspnea, copd, beta_blockers, lung_scan]:
        st.error("Vänligen besvara alla frågor.")
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = pd.DataFrame({
            "Datum": [current_time],
            "Studiekod": [user_code],
            "Patientfall": ["Fall 6"],
            "andfåddhet": [dyspnea],
            "KOL": [copd],
            "betablockerare": [beta_blockers],
            "lungröntgen": [lung_scan],
            "Dokumentationssäkerhet": [confidence]
        })

        if os.path.exists(csv_file):
            existing = pd.read_csv(csv_file)
            data = pd.concat([existing, row], ignore_index=True)
        else:
            data = row

        data.to_csv(csv_file, index=False)
        st.success("Svar sparade! ✨")
