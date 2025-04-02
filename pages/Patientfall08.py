import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Patientscenario 8 – Maja Lind", layout="centered")
st.title("Patientscenario 8")

# ✏️ Patientfall
st.markdown("""
🩺 **Maja Lind, 48 år**

Maja Lind, 48 år, söker vårdcentralen för återkommande yrsel.  
Hon har inte karusellyrsel (att rummet snurrar).  
Hon är osäker på om hon har lågt blodtryck för det var så längesedan hon kontrollerade det.
""")

# 💬 Studiekod
user_code = st.text_input("Ange din studiekod som du får av intervjuaren och tryck enter:")
if user_code:
    user_code = user_code.zfill(3)
    st.success(f"Studiekod registrerad: {user_code}")

# 📋 Radioknappar med kommentar
def presence_question_with_comment(label, key_prefix):
    options = ["(Välj)", "Ja", "Nej", "Vet ej"]
    response = st.radio(f"**{label}**", options, key=f"{key_prefix}_response")

    comment = ""
    if response in ["Nej", "Vet ej"]:
        comment = st.text_area(f"Beskrivning / kommentar för '{label.lower()}' (frivillig):", key=f"{key_prefix}_comment")

    return response, comment

# ❓ Frågor
dizziness, dizziness_comment = presence_question_with_comment("Upplever patienten yrsel?", "dizziness")
spinning, spinning_comment = presence_question_with_comment("Upplever patienten karusellyrsel?", "spinning")
low_bp, low_bp_comment = presence_question_with_comment("Har patienten lågt blodtryck?", "low_bp")
medication, medication_comment = presence_question_with_comment("Tar patienten någon medicinering?", "medication")

# 📏 Dokumentationssäkerhet
confidence = st.slider("Hur säker är du på din dokumentation?", 1, 7, 4)

# 📋 Sammanfattning
st.subheader("📋 Sammanfattning")
st.write(f"- Yrsel: {dizziness} — Kommentar: {dizziness_comment}")
st.write(f"- Karusellyrsel: {spinning} — Kommentar: {spinning_comment}")
st.write(f"- Lågt blodtryck: {low_bp} — Kommentar: {low_bp_comment}")
st.write(f"- Medicinering: {medication} — Kommentar: {medication_comment}")
st.write(f"- Dokumentationssäkerhet: {confidence}")

# 💾 Spara till CSV
csv_file = "maja_lind_svar.csv"

if st.button("Skicka in"):
    if not user_code:
        st.error("Vänligen ange din studiekod.")
    elif "(Välj)" in [dizziness, spinning, low_bp, medication]:
        st.error("Vänligen svara på alla frågor.")
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = pd.DataFrame({
            "Datum": [current_time],
            "Kod": [user_code],
            "Yrsel": [dizziness],
            "Yrsel kommentar": [dizziness_comment],
            "Karusellyrsel": [spinning],
            "Karusellyrsel kommentar": [spinning_comment],
            "Lågt blodtryck": [low_bp],
            "Lågt blodtryck kommentar": [low_bp_comment],
            "Medicinering": [medication],
            "Medicinering kommentar": [medication_comment],
            "Dokumentationssäkerhet": [confidence]
        })

        if os.path.exists(csv_file):
            existing = pd.read_csv(csv_file)
            data = pd.concat([existing, row], ignore_index=True)
        else:
            data = row

        data.to_csv(csv_file, index=False)
        st.success("Svar sparade! ✨")
