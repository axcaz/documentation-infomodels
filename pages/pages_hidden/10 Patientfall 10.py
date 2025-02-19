import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Filnamn för CSV
csv_file = "responses.csv"

# Lägg till anpassad CSS för att minska bredden på dropdown-menyerna
st.markdown("""
    <style>
    .stSelectbox {
        width: 30% !important;  /* Justerar bredden till 30% */
    }
    </style>
    """, unsafe_allow_html=True)

# Fråga om en unik kod
user_code = st.text_input("Ange din unika kod som du får av intervjuaren och tryck enter:")

# Titel och patientscenario
st.write("""
### Patientscenario 10: Fia Andersson, 34 år
Patienten söker för magont. Hon har inte celiaki. 
Hon är osäker på om hennes smärtor kan bero på laktosintolerans.
""")

# NIM-alternativ med förvald "(Välj ett alternativ)"
nim_options = [
    "(Välj ett alternativ)",  # Förvalt alternativ
    "Misstänkt",
    "Känt möjligt",
    "Bekräftat närvarande",
    "Känt frånvarande",
    "Okänt"
]

# Funktion för att visa en fråga med dropdown
def select_nim_status(label, key_prefix):
    st.write(f"### {label}")  # Behåller rubriken
    choice = st.selectbox(
        "",  # Tar bort rubriken ovanför dropdown-menyn
        nim_options,
        key=f"{key_prefix}_nim",
        index=0  # Förvalt som "(Välj ett alternativ)"
    )
    return choice

# NIM-status för Fia Andersson
nim_pain = select_nim_status("Har patienten magont?", "nim_pain")
nim_celiac = select_nim_status("Har patienten celiaki?", "nim_celiac")
nim_lactose = select_nim_status("Har patienten laktosintolerans?", "nim_lactose")
nim_diarrhea = select_nim_status("Har patienten diarré?", "nim_diarrhea")

# Sammanfattning av data
st.write("### Sammanfattning av dokumentation")
st.write(f"- Magont: {nim_pain if nim_pain != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Celiaki: {nim_celiac if nim_celiac != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Laktosintolerans: {nim_lactose if nim_lactose != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Diarré: {nim_diarrhea if nim_diarrhea != '(Välj ett alternativ)' else 'Ej angiven'}")

# Skicka in svaren
if st.button("Skicka in"):
    # Skapa en rad med svaren
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Datum och tid
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],  # Ange koden eller "Ej angiven"
        "Magont": [nim_pain if nim_pain != "(Välj ett alternativ)" else "Ej angiven"],
        "Celiaki": [nim_celiac if nim_celiac != "(Välj ett alternativ)" else "Ej angiven"],
        "Laktosintolerans": [nim_lactose if nim_lactose != "(Välj ett alternativ)" else "Ej angiven"],
        "Diarré": [nim_diarrhea if nim_diarrhea != "(Välj ett alternativ)" else "Ej angiven"]
    })

    # Kontrollera om filen redan finns
    if os.path.exists(csv_file):
        # Om filen finns, läs in den och lägg till nya svar
        existing_data = pd.read_csv(csv_file)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        # Om filen inte finns, skapa en ny
        updated_data = new_data

    # Spara tillbaka till CSV-filen
    updated_data.to_csv(csv_file, index=False)
    st.success("Dina svar har sparats!")

# Visa insamlade svar
if st.button("Visa insamlade svar"):
    if os.path.exists(csv_file):
        data = pd.read_csv(csv_file)
        st.write(data)
    else:
        st.warning("Inga svar har samlats in ännu.")
