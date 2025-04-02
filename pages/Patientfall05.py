import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Patientscenario 5 👩‍💻", page_icon="👩‍💻", layout="centered")
st.title("Patientscenario 5")

# ✏️ Patientfall
st.markdown("""
🩺 **Faduma Ali, 29 år**

Faduma Ali, 29 år, träffar dig på vårdcentralen för långvarig hosta och feber.  
Hon har aldrig tidigare blivit diagnostiserad med lunginflammation.  
Hon är osäker på om hon kanske har astma.
""")

# 📋 Funktion för fråga + eventuell kommentar
def presence_question_with_comment(label, key_prefix):
    options = ["(Välj)", "Ja", "Nej", "Vet ej"]
    response = st.radio(f"**{label}**", options, key=f"{key_prefix}_response")

    comment = ""
    if response in ["Nej", "Vet ej"]:
        comment = st.text_area("Kommentar (frivilligt):", key=f"{key_prefix}_comment")
    return response, comment

# 🧑‍💻 Studiekod
user_code = st.text_input("Ange din studiekod som du får av intervjuaren och tryck enter:")
if user_code:
    user_code = user_code.zfill(3)
    st.success(f"Studiekod registrerad: {user_code}")

# ❓ Frågor
fever, fever_comment = presence_question_with_comment("Har patienten feber?", "fever")
pneumonia, pneumonia_comment = presence_question_with_comment("Har patienten tidigare fått diagnosen lunginflammation?", "pneumonia")
asthma, asthma_comment = presence_question_with_comment("Har patienten astma?", "asthma")
airway_inf, airway_inf_comment = presence_question_with_comment("Har patienten haft en luftvägsinfektion nyligen?", "airway")

# 📏 Dokumentationssäkerhet
confidence = st.slider("Hur säker är du på din dokumentation?", 1, 7, 4)

# 📝 Sammanfattning
st.subheader("📋 Sammanfattning")
st.write(f"- Feber: {fever} — Kommentar: {fever_comment}")
st.write(f"- Lunginflammation: {pneumonia} — Kommentar: {pneumonia_comment}")
st.write(f"- Astma: {asthma} — Kommentar: {asthma_comment}")
st.write(f"- Luftvägsinfektion: {airway_inf} — Kommentar: {airway_inf_comment}")
st.write(f"- Dokumentationssäkerhet: {confidence}")

# 💾 Spara till gemensam responses.csv
csv_file = "responses.csv"

if st.button("Skicka in"):
    if not user_code:
        st.error("Vänligen ange din studiekod.")
    elif "(Välj)" in [fever, pneumonia, asthma, airway_inf]:
        st.error("Vänligen besvara alla frågor.")
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = pd.DataFrame({
            "Datum": [current_time],
            "Studiekod": [user_code],
            "feber": [fever],
            "feber kommentar": [fever_comment],
            "lunginflammation": [pneumonia],
            "lunginflammation kommentar": [pneumonia_comment],
            "astma": [asthma],
            "astma kommentar": [asthma_comment],
            "luftvägsinfektion": [airway_inf],
            "luftvägsinfektion kommentar": [airway_inf_comment],
            "Dokumentationssäkerhet": [confidence]
        })

        if os.path.exists(csv_file):
            existing = pd.read_csv(csv_file)
            data = pd.concat([existing, row], ignore_index=True)
        else:
            data = row

        data.to_csv(csv_file, index=False)
        st.success("Svar sparade! ✨")
