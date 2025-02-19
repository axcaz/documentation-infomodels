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
### Patientscenario 9: Olle Jansson, 70 år
Patienten har hosta sedan flera veckor tillbaka. Han har inte KOL. 
Han är osäker på om han haft lunginflammation tidigare.
""")

# Enkla alternativ för dokumentation med förvald "(Välj ett alternativ)"
options = ["(Välj ett alternativ)", "Ja", "Nej", "Vet ej"]  

# Funktion för att visa en fråga med stor rubrik och dropdown (utan upprepning)
def document_question(label, key_prefix):
    st.write(f"### {label}")  # Behåller stora rubriken
    return st.selectbox("", options, key=key_prefix, index=0)  # Tar bort liten text i dropdown

# Frågor för Olle Jansson
cough = document_question("Har patienten hosta?", "cough")
copd = document_question("Har patienten KOL?", "copd")
pneumonia = document_question("Har patienten haft lunginflammation?", "pneumonia")
oxygenation = document_question("Hur syresätter sig patienten?", "oxygenation")

# Sammanfattning av data
st.write("### Sammanfattning av dokumentation")
st.write(f"- Hosta: {cough if cough != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- KOL: {copd if copd != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Lunginflammation: {pneumonia if pneumonia != '(Välj ett alternativ)' else 'Ej angiven'}")
st.write(f"- Syresättning: {oxygenation if oxygenation != '(Välj ett alternativ)' else 'Ej angiven'}")

# Skicka in svaren
if st.button("Skicka in"):
    # Skapa en rad med svaren
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Datum och tid
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],  # Ange koden eller "Ej angiven"
        "Hosta": [cough if cough != "(Välj ett alternativ)" else "Ej angiven"],
        "KOL": [copd if copd != "(Välj ett alternativ)" else "Ej angiven"],
        "Lunginflammation": [pneumonia if pneumonia != "(Välj ett alternativ)" else "Ej angiven"],
        "Syresättning": [oxygenation if oxygenation != "(Välj ett alternativ)" else "Ej angiven"]
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
