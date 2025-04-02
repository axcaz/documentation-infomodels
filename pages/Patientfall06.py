import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Patientscenario 6 – Aaro Niemi", layout="centered")
st.title("Patientscenario 6")

# ✏️ Patientfall
st.markdown("""
🩺 **Aaro Niemi, 80 år**

Aaro, från Finland, inkommer till sjukhuset med svår andfåddhet när han hälsar på sitt barnbarn i Stockholm.  
Han har aldrig haft KOL. Han tar någon medicin pga tidigare hjärtinfarkt men minns inte namnet.  
Han gjorde en lungröntgen i Helsingfors för någon månad sedan.
""")

# 💬 Studiekod
user_code = st.text_input("Ange din studiekod som du får av intervjuaren och tryck enter:")
if user_code:
    user_code = user_code.zfill(3)
    st.success(f"Studiekod registrerad: {user_code}")

# 💡 Funktion för HL7 FHIR-status
def select_fhir_status(label, key_prefix):
    st.markdown(f"**{label}**")
    options = ["(Välj)", "Bekräftad", "Motbevisad", "Obekräftad"]
    suboptions = ["(Välj)", "Provisorisk", "Differential"]

    main_selection = st.radio("", options, key=f"{key_prefix}_main")

    if main_selection == "Obekräftad":
        st.markdown('<p style="font-size: 0.8rem; color: #0078D7; font-style: italic;">(Om du väljer "Obekräftad" måste du välja ett underalternativ)</p>', unsafe_allow_html=True)

    explanation = {
        "Bekräftad": "Det finns tillräckligt med bevis för att fastställa förekomsten av tillståndet.",
        "Motbevisad": "Tillståndet har uteslutits av efterföljande diagnostiska och kliniska bevis.",
        "Obekräftad": "Det finns inte tillräckligt med bevis för att fastställa förekomsten av tillståndet."
    }

    if main_selection in explanation:
        st.markdown(f'<p style="font-size: 0.85rem; color: #555; font-style: italic;">{explanation[main_selection]}</p>', unsafe_allow_html=True)

    sub_selection = None
    if main_selection == "Obekräftad":
        sub_selection = st.radio("**Underalternativ för Obekräftad:**", suboptions, key=f"{key_prefix}_sub")

        sub_desc = {
            "Provisorisk": "Detta är en preliminär diagnos som fortfarande övervägs.",
            "Differential": "En möjlig diagnos bland flera, för att vägleda vidare utredning."
        }

        if sub_selection in sub_desc:
            st.markdown(f'<p style="font-size: 0.85rem; color: #555; font-style: italic;">{sub_desc[sub_selection]}</p>', unsafe_allow_html=True)

    if main_selection == "(Välj)":
        return None
    elif main_selection == "Obekräftad" and sub_selection and sub_selection != "(Välj)":
        return f"{main_selection} - {sub_selection}"
    elif main_selection == "Obekräftad":
        return None
    else:
        return main_selection

# ❓ Frågor
dyspnea = select_fhir_status("Är patienten andfådd?", "dyspnea")
copd = select_fhir_status("Har patienten KOL?", "copd")
beta_blockers = select_fhir_status("Tar patienten betablockerare?", "beta_blockers")
lung_scan = select_fhir_status("Har patienten genomgått lungröntgen nyligen?", "lung_scan")

# 📏 Dokumentationssäkerhet
confidence = st.slider("Hur säker är du på din dokumentation?", 1, 7, 4)

# 📋 Sammanfattning
st.subheader("📋 Sammanfattning")
st.write(f"- Andfåddhet: {dyspnea or 'Ej angiven'}")
st.write(f"- KOL: {copd or 'Ej angiven'}")
st.write(f"- Betablockerare: {beta_blockers or 'Ej angiven'}")
st.write(f"- Lungröntgen: {lung_scan or 'Ej angiven'}")
st.write(f"- Dokumentationssäkerhet: {confidence}")

# 💾 CSV och spara
csv_file = "aaro_niemi_svar.csv"

if st.button("Skicka in"):
    if not user_code:
        st.error("Vänligen ange din studiekod.")
    elif None in [dyspnea, copd, beta_blockers, lung_scan]:
        st.error("Vänligen besvara alla frågor.")
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = pd.DataFrame({
            "Datum": [current_time],
            "Kod": [user_code],
            "Andfåddhet": [dyspnea],
            "KOL": [copd],
            "Betablockerare": [beta_blockers],
            "Lungröntgen": [lung_scan],
            "Dokumentationssäkerhet": [confidence]
        })

        if os.path.exists(csv_file):
            existing = pd.read_csv(csv_file)
            data = pd.concat([existing, row], ignore_index=True)
        else:
            data = row

        data.to_csv(csv_file, index=False)
        st.success("Svar sparade! ✨")
