import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Patientscenario 8 – Maja Lind", layout="centered")
st.title("Patientscenario 8")

# 🩺 Patientfall
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

# ✅ Radioknappar utan fritext
def simple_presence_question(label, key):
    options = ["(Välj)", "Ja", "Nej", "Vet ej"]
    return st.radio(f"**{label}**", options, key=key)

# ❓ Frågor
dizziness = simple_presence_question("Upplever patienten yrsel?", "dizziness")
spinning = simple_presence_question("Upplever patienten karusellyrsel?", "spinning")
low_bp = simple_presence_question("Har patienten lågt blodtryck?", "low_bp")
medication = simple_presence_question("Tar patienten någon medicinering?", "medication")

# 📏 Dokumentationssäkerhet
confidence = st.slider("Hur säker är du på din dokumentation?", 1, 7, 4)

# 📋 Sammanfattning
st.subheader("📋 Sammanfattning")
st.write(f"- Yrsel: {dizziness}")
st.write(f"- Karusellyrsel: {spinning}")
st.write(f"- Lågt blodtryck: {low_bp}")
st.write(f"- Medicinering: {medication}")
st.write(f"- Dokumentationssäkerhet: {confidence}")

# 💾 Spara
csv_file = "maja_lind_svar.csv"

if st.button("Skicka in"):
    if not user_code:
        st.error("Vänligen ange din studiekod.")
    elif "(Välj)" in [dizziness, spinning, low_bp, medication]:
        st.error("Vänligen svara på alla frågor.")
    else:
        row = pd.DataFrame({
            "Datum": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Studiekod": [user_code],
            "Yrsel": [dizziness],
            "Karusellyrsel": [spinning],
            "Lågt blodtryck": [low_bp],
            "Medicinering": [medication],
            "Dokumentationssäkerhet": [confidence]
        })

        if os.path.exists(csv_file):
            existing = pd.read_csv(csv_file)
            data = pd.concat([existing, row], ignore_index=True)
        else:
            data = row

        data.to_csv(csv_file, index=False)
        st.success("Svar sparade! ✨")
