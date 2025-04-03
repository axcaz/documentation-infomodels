import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Patientscenario 4 👩‍💻", page_icon="👩‍💻", layout="centered")
st.title("Patientscenario 4")

# ✏️ Patientfall
st.markdown("""
🩺 **Stina Eriksson, 52 år**

På vårdcentralen träffar du en nylistad patient, Stina Eriksson, 52 år, som söker med hudutslag.  
Hon har aldrig diagnostiserats med psoriasis.  
Hon är osäker på om utslagen kan vara ärftliga.
""")

# Funktion för val och eventuell fritext vid osäkerhet/negation
def presence_question_with_comment(label, key_prefix):
    options = ["(Välj)", "Ja", "Nej", "Vet ej"]
    response = st.radio(f"**{label}**", options, key=f"{key_prefix}_response")

    comment = ""
    if response in ["Nej", "Vet ej"]:
        comment = st.text_area(
            f"Kommentar (frivilligt):",
            key=f"{key_prefix}_comment"
        )
    return response, comment

# 📋 Studiekod
user_code = st.text_input("Ange din studiekod som du får av intervjuaren och tryck enter:")
if user_code:
    user_code = user_code.zfill(3)
    st.success(f"Studiekod registrerad: {user_code}")

# 🧪 Frågor
rash, rash_comment = presence_question_with_comment("Har patienten hudutslag?", "rash")
psoriasis, psoriasis_comment = presence_question_with_comment("Har patienten diagnosen psoriasis?", "psoriasis")
heredity, heredity_comment = presence_question_with_comment("Finns ärftlighet för liknande besvär?", "heredity")
itching, itching_comment = presence_question_with_comment("Upplever patienten klåda?", "itching")

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

# 🧾 Sammanfattning
st.subheader("📋 Sammanfattning")
st.write(f"- Hudutslag: {rash} — Kommentar: {rash_comment}")
st.write(f"- Psoriasis: {psoriasis} — Kommentar: {psoriasis_comment}")
st.write(f"- Ärftlighet utslag: {heredity} — Kommentar: {heredity_comment}")
st.write(f"- Klåda: {itching} — Kommentar: {itching_comment}")
st.write(f"- Dokumentationssäkerhet: {confidence}")

# 💾 Spara till responses.csv (samlingsfil)
csv_file = "responses.csv"

if st.button("Skicka in"):
    if not user_code:
        st.error("Vänligen ange din studiekod.")
    elif "(Välj)" in [rash, psoriasis, heredity, itching]:
        st.error("Vänligen svara på alla frågor.")
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data = pd.DataFrame({
            "Datum": [current_time],
            "Studiekod": [user_code],
            "Patientfall": ["Fall 4"],
            "hudutslag": [rash],
            "hudutslag kommentar": [rash_comment],
            "psoriasis": [psoriasis],
            "psoriasis kommentar": [psoriasis_comment],
            "ärftlighet utslag": [heredity],
            "ärftlighet utslag kommentar": [heredity_comment],
            "klåda": [itching],
            "klåda kommentar": [itching_comment],
            "Dokumentationssäkerhet": [confidence]
        })

        # 🧩 Spara eller uppdatera responses.csv
        if os.path.exists(csv_file):
            existing_data = pd.read_csv(csv_file)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        updated_data.to_csv(csv_file, index=False)
        st.success("Svar sparade! ✨")
