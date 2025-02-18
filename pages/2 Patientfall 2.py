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
st.write("""
### Patientscenario 2: Mats Matsson 73 år
Patienten söker för huvudvärk, ramlat för ett par veckor sedan, upplever inga förändringar i synen. Han tror inte han har slagit i huvudet.
""")

# Alternativ med beskrivningar
nim_options = {
    "Misstänkt": "Tillståndet eller diagnosen är misstänkt men ännu inte bekräftad.",
    "Känt möjligt": "Tillståndet är känt som en möjlig diagnos, men det är inte bekräftat.",
    "Bekräftad närvarande": "Tillståndet eller diagnosen har bekräftats som närvarande.",
    "Känt frånvarande": "Tillståndet eller diagnosen är känd att vara frånvarande.",
    "Okänt": "Informationen om tillståndet är okänd eller oidentifierad."
}

# Funktion för att visa en dropdown med ett tomt förvalt alternativ
def select_with_tooltips(label, options, key_prefix):
    st.write(f"### {label}")
    options_with_empty = ["(Välj ett alternativ)"] + list(options.keys())
    selected = st.selectbox("", options_with_empty, key=f"{key_prefix}_selectbox")
    if selected and selected != "(Välj ett alternativ)":
        st.markdown(f"""
            **Valt alternativ:** {selected}  
            ℹ️ **Beskrivning:** {options[selected]}
        """)
    return selected if selected != "(Välj ett alternativ)" else None

# Socialstyrelsens NIM Hälsotillstånd
nim_pain = select_with_tooltips("Har patienten huvudvärk?", nim_options, "nim_pain")
nim_eyes = select_with_tooltips("Har patienten synpåverkan?", nim_options, "nim_eyes")
nim_headtrauma = select_with_tooltips("Har patienten slagit i huvudet?", nim_options, "nim_headtrauma")
nim_bloodthinners = select_with_tooltips("Tar patienten blodförtunnande mediciner?", nim_options, "nim_bloodthinners")

# Sammanfattning av valda alternativ
st.write("### Sammanfattning av dokumentation")
st.write(f"- Huvudvärk: {nim_pain if nim_pain else 'Ej angiven'}")
st.write(f"- Synpåverkan: {nim_eyes if nim_eyes else 'Ej angiven'}")
st.write(f"- Slagit i huvudet: {nim_headtrauma if nim_headtrauma else 'Ej angiven'}")
st.write(f"- Blodförtunnande mediciner: {nim_bloodthinners if nim_bloodthinners else 'Ej angiven'}")
# Skicka in svaren
if st.button("Skicka in"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],
        "Huvudvärk": [nim_pain if nim_pain else "Ej angivet"],
        "Synpåverkan": [nim_eyes if nim_eyes else "Ej angivet"],
        "Slagit i huvudet": [nim_headtrauma if nim_headtrauma else "Ej angivet"],
        "Blodförtunnande mediciner": [nim_bloodthinners if nim_bloodthinners else "Ej angivet"]
    })

    if os.path.exists(csv_file):
        existing_data = pd.read_csv(csv_file)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(csv_file, index=False)
    st.success("Dina svar har sparats!")