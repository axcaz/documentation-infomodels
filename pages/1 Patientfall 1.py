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
# Dokumentation enligt pappersblankett
st.write("""
### Patientscenario 1: Anna Andersson, 45 år
Patienten uppger att hon själv uppmätt förhöjt blodtryck hemma. Hon har aldrig fått diagnosen stroke och har inte haft några kända stroke-relaterade symtom. Det finns en osäkerhet kring eventuell penicillinallergi i barndomen, men ingen tidigare dokumenterad allergisk reaktion.
""")

# Enkla alternativ för dokumentation med tom förvald rad
options = ["(Välj ett alternativ)", "Ja", "Nej", "Vet ej"]  # Tomt alternativ som standard

# Funktion för att visa en fråga med dropdown
def document_question(label, key_prefix):
    st.write(f"### {label}")
    answer = st.selectbox(label, options, key=key_prefix, index=0)  # Förvalt tom
    return answer

# Frågor med tom förvald rad
blood_pressure = document_question("Har patienten förhöjt blodtryck?", "blood_pressure")
stroke = document_question("Har patienten haft stroke?", "stroke")
pc_allergy = document_question("Har patienten allergi mot penicillin?", "pc_allergy")
abdominal_surgery = document_question("Är patienten opererad i buken?", "abdominal_surgery")

# Sammanfattning av data
st.write("### Sammanfattning av dokumentation")
st.write(f"- Förhöjt blodtryck: {blood_pressure if blood_pressure else 'Ej angiven'}")
st.write(f"- Stroke: {stroke if stroke else 'Ej angiven'}")
st.write(f"- Allergi mot penicillin: {pc_allergy if pc_allergy else 'Ej angiven'}")
st.write(f"- Operation i buken: {abdominal_surgery if abdominal_surgery else 'Ej angiven'}")

# Skicka in svaren
if st.button("Skicka in"):
    # Skapa en rad med svaren
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Datum och tid
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],  # Ange koden eller "Ej angiven"
        "Förhöjt blodtryck": [blood_pressure if blood_pressure else "Ej angiven"],
        "Stroke": [stroke if stroke else "Ej angiven"],
        "Allergi mot penicillin": [pc_allergy if pc_allergy else "Ej angiven"],
        "Operation i buken": [abdominal_surgery if abdominal_surgery else "Ej angiven"]
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
