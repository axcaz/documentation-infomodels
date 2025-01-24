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

# Titel och introduktion
st.title("Dokumentera enligt Socialstyrelsens NIM hälsotillstånd")
st.write("""
### Patientscenario 1: Anna Andersson, 45 år
Anna söker vårdcentralen r/t förhöjt blodtryck som hon märkt av hemma själv med sin blodtrycksmätare. 
Hon har aldrig haft någon stroke. Hon är osäker på om hon reagerat på penicillin som barn.
""")

# Alternativ med beskrivningar
nim_options = {
    "Misstänkt": "Tillståndet eller diagnosen är misstänkt men ännu inte bekräftad. Det finns en misstanke om att tillståndet kan förekomma baserat på de tillgängliga symtomen eller fynden.",
    "Känt möjligt": "Tillståndet är känt som en möjlig diagnos, men det är inte bekräftat. Det finns en övervägning eller ett antagande om att tillståndet kan vara närvarande.",
    "Bekräftad närvarande": "Tillståndet eller diagnosen har bekräftats som närvarande genom medicinska undersökningar, tester eller observationer. Det är fastställt att patienten har tillståndet.",
    "Känt frånvarande": "Tillståndet eller diagnosen är känd att vara frånvarande eller utesluten genom diagnostiska tester eller bedömningar. Detta till skillnad från att inget dokumenterats om ett specifikt tillstånd vilket kan innebära att man inte utrett det överhuvudtaget.",
    "Okänt": "Informationen om tillståndet är okänd eller oidentifierad. Det finns ingen information tillgänglig om huruvida tillståndet är närvarande eller inte."
}

# Funktion för att visa en dropdown med info-ikoner för varje alternativ
def select_with_tooltips(label, options, key_prefix):
    st.write(f"### {label}")
    selected = st.selectbox(
        "Välj ett alternativ:", 
        list(options.keys()), 
        key=f"{key_prefix}_selectbox"
    )
    st.markdown(f"""
        **Valt alternativ:** {selected}  
        ℹ️ **Beskrivning:** {options[selected]}
    """)
    return selected

# Socialstyrelsens NIM Hälsotillstånd
nim_bp = select_with_tooltips("Har patienten förhöjt blodtryck?", nim_options, "nim_bp")
nim_stroke = select_with_tooltips("Har patienten haft stroke?", nim_options, "nim_stroke")
nim_pc_allergy = select_with_tooltips("Har patienten allergi mot penicillin?", nim_options, "nim_pc_allergy")
nim_surgery = select_with_tooltips("Är patienten opererad i buken?", nim_options, "nim_surgery")

# Skicka in svaren
if st.button("Skicka in"):
    # Skapa en rad med svaren
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Datum och tid
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],  # Ange koden eller "Ej angiven"
        "Förhöjt blodtryck": [nim_bp],
        "Stroke": [nim_stroke],
        "Allergi mot penicillin": [nim_pc_allergy],
        "Operation i buken": [nim_surgery]
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
