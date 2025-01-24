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
st.title("Dokumentation som på pappersblankett.")
st.write("""
### Patientscenario 1: Anna Andersson, 45 år
Anna söker vårdcentralen på grund av förhöjt blodtryck som hon har mätt hemma. 
Hon har aldrig haft någon stroke och är osäker på om hon reagerade på penicillin som barn.
""")

# Enkla alternativ för dokumentation
options = ["Ja", "Nej", "Vet ej"]

# Funktion för att visa en fråga med dropdown
def document_question(label, key_prefix):
    st.write(f"### {label}")
    answer = st.selectbox("Välj ett alternativ:", options, key=key_prefix)
    return answer

# Frågor
options = ["Ja", "Nej", "Vet ej"]
blood_pressure = st.selectbox("Har patienten förhöjt blodtryck?", options, key="blood_pressure")
stroke = st.selectbox("Har patienten haft stroke?", options, key="stroke")
pc_allergy = st.selectbox("Har patienten allergi mot penicillin?", options, key="pc_allergy")
abdominal_surgery = st.selectbox("Är patienten opererad i buken?", options, key="abdominal_surgery")

# Sammanfattning av data
st.write("### Sammanfattning av dokumentation")
st.write(f"- Förhöjt blodtryck: {blood_pressure}")
st.write(f"- Stroke: {stroke}")
st.write(f"- Allergi mot penicillin: {pc_allergy}")
st.write(f"- Operation i buken: {abdominal_surgery}")

# Skicka in svaren
if st.button("Skicka in"):
    # Skapa en rad med svaren
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Datum och tid
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],  # Ange koden eller "Ej angiven"
        "Förhöjt blodtryck": [blood_pressure],
        "Stroke": [stroke],
        "Allergi mot penicillin": [pc_allergy],
        "Operation i buken": [abdominal_surgery]
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