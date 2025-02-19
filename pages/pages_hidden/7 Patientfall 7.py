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
# Dokumentation enligt Socialstyrelsens NIM
st.write("""
### Patientscenario 7: Erik Eriksson, 62 år
Patienten söker akut för kraftig ryggsmärta mellan skulderbladen som kom plötsligt. 
Han har aldrig rökt. Han är osäker på om någon i familjen haft aneurysm i bröstkorgsaortan.
""")

# NIM-alternativ med förvald "(Välj detta alternativ)"
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
    st.write(f"### {label}")
    choice = st.selectbox(
        "",  # Tar bort rubriken ovanför dropdown-menyn
        nim_options,
        key=f"{key_prefix}_nim",
        index=0  # Förvalt som "(Välj detta alternativ)"
    )
    return choice

# NIM-status för Erik Eriksson
nim_pain = select_nim_status("Har patienten ryggsmärta?", "nim_pain")
nim_smoking = select_nim_status("Röker patienten?", "nim_smoking")
nim_aneurysm = select_nim_status("Finns ärftlighet för aortaaneurysm?", "nim_aneurysm")
nim_hypertension = select_nim_status("Har patienten hypertoni?", "nim_hypertension")

# Sammanfattning av data
st.write("### Sammanfattning av dokumentation")
st.write(f"- Ryggsmärta: {nim_pain if nim_pain != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Rökning: {nim_smoking if nim_smoking != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Ärftlighet för aortaaneurysm: {nim_aneurysm if nim_aneurysm != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Hypertoni: {nim_hypertension if nim_hypertension != '(Välj ett alternativ)' else 'Ej angiven'}")

# Skicka in svaren
if st.button("Skicka in"):
    # Skapa en rad med svaren
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Datum och tid
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],  # Ange koden eller "Ej angiven"
        "Ryggsmärta": [nim_pain if nim_pain != "(Välj ett alternativ)" else "Ej angiven"],
        "Diabetes": [nim_diabetes if nim_diabetes != "(Välj ett alternativ)" else "Ej angiven"],
        "Ärftlighet för aortaaneurysm": [nim_aneurysm if nim_aneurysm != "(Välj ett alternativ)" else "Ej angiven"],
        "Hypertoni": [nim_hypertension if nim_hypertension != "(Välj ett alternativ)" else "Ej angiven"]
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
