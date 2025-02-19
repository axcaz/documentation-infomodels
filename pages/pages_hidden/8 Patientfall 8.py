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
#Blankett
st.write("""
### Patientscenario 8: Maja Lind, 48 år
Patienten söker för yrsel. Hon har aldrig haft migrän. Hon är osäker på om hon har lågt blodtryck. 
Det finns ingen information om hon tar blodförtunnande läkemedel.
""")

# Enkla alternativ för dokumentation med förvald "(Välj ett alternativ)"
options = ["(Välj ett alternativ)", "Ja", "Nej", "Vet ej"]  

# Funktion för att visa en fråga med stor rubrik och dropdown (utan upprepning)
def document_question(label, key_prefix):
    st.write(f"### {label}")  # Behåller stora rubriken
    return st.selectbox("", options, key=key_prefix, index=0)  # Tar bort liten text i dropdown


# Frågor för Maja Lind
dizziness = document_question("Upplever patienten yrsel?", "dizziness")
migraine = document_question("Har patienten migrän?", "migraine")
low_bp = document_question("Har patienten lågt blodtryck?", "low_bp")
anticoagulants = document_question("Står patienten på blodförtunnande medicinering?", "anticoagulants")

# Sammanfattning av data
st.write("### Sammanfattning av dokumentation")
st.write(f"- Yrsel: {dizziness if dizziness != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Migrän: {migraine if migraine != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Lågt blodtryck: {low_bp if low_bp != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Blodförtunnande medicinering: {anticoagulants if anticoagulants != '(Välj ett alternativ)' else 'Ej angiven'}")

# Skicka in svaren
if st.button("Skicka in"):
    # Skapa en rad med svaren
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Datum och tid
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],  # Ange koden eller "Ej angiven"
        "Yrsel": [dizziness if dizziness != "(Välj ett alternativ)" else "Ej angiven"],
        "Migrän": [migraine if migraine != "(Välj ett alternativ)" else "Ej angiven"],
        "Lågt blodtryck": [low_bp if low_bp != "(Välj ett alternativ)" else "Ej angiven"],
        "Blodförtunnande medicinering": [anticoagulants if anticoagulants != "(Välj ett alternativ)" else "Ej angiven"]
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
