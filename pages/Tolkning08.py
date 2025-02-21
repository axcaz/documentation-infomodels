import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Filnamn för datafiler
doc_csv_file = "responses.csv"  # Filen med dokumenterade patientfall
interpret_csv_file = "interpretations.csv"  # Här sparas tolkningarna

# 🔹 **Titel**
st.title("Tolkning av Patientscenario 8")

# 🔹 **Ange studiekod och begränsa bredden till 50% med columns**
col1, col2 = st.columns([1, 1])  # 50% / 50%
with col1:
    user_code = st.text_input("Ange din egen studiekod (den du fått av intervjuaren):")
if user_code:
    st.success("Studiekod registrerad!")

# Ladda in data
if os.path.exists(doc_csv_file):
    df = pd.read_csv(doc_csv_file, dtype=str)
    df["Kod"] = df["Kod"].astype(str).str.strip()  # Rensa mellanslag från koder
else:
    df = pd.DataFrame()

# Om det finns data, låt tolken välja en dokumentationskod att tolka
if not df.empty:
    available_codes = df["Kod"].unique()

    # 🔹 **Välj dokumentationskod med 30% bredd**
    col1, col2, col3 = st.columns([1, 1.5, 1])  # 30% av bredden på mittenkolumnen
    with col2:
        selected_code = st.selectbox(
            "Intervjuaren ger dig en dokumentationskod att tolka:", 
            options=["Välj dokumentationskod"] + list(available_codes), 
            index=0
        )

    if selected_code and selected_code != "Välj dokumentationskod":
        # Hämta dokumentationen för det valda fallet
        patient_data = df[df["Kod"] == selected_code].dropna(how="all").tail(1)

        if not patient_data.empty:
            st.write("### Dokumenterad information att tolka:")
            st.write("Vi läser nu vad en kollega dokumenterat om patient Maja Lind, 48 år, som sökt sig till vårdcentralen.")

            # Hämta de 4 frågor som hör till detta patientfall
            relevant_cols = ["Yrsel", "Migrän", "Lågt blodtryck", "Blodförtunnande medicinering"]
            doc_text = "\n".join(
                [f"- **{col}:** {patient_data.iloc[-1][col]}" for col in relevant_cols if col in patient_data.columns]
            )

            st.markdown(doc_text)

            # 🔹 **Tolkningsfrågor**
            st.write("### Tolkningsfrågor")
            st.write("Uppfattar du utifrån informationen ovan att patienten har följande symtom/diagnoser/behandlingar?")
            for col in relevant_cols:
                st.write(f"**{col}?**")

            # 🔹 **Skriv eller diktera tolkningen**
            st.write("### Skriv, eller berätta muntligt, din tolkning (som om du dikterar journalanteckning):")
            st.write("Skriv/berätta i stil med:")

            # Lägg till ett kursiverat exempel på diktatformulering
            st.markdown('*"Patienten har .............., har inte .............., osäkert om .............., vi känner inte till om .............."*')

            user_interpretation = st.text_area("")

            # 🔹 **Lägger till checkbox för muntlig tolkning**
            oral_interpretation = st.checkbox("Jag har berättat muntligt istället för att skriva.")

            # 🔹 **Skicka in-knappen**
            if st.button("Skicka in"):
                if user_interpretation.strip() == "" and not oral_interpretation:
                    st.warning("Du måste skriva något innan du kan skicka in (om du inte berättat muntligt).")
                else:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    new_data = pd.DataFrame({
                        "Datum": [current_time],
                        "Tolkens studiekod": [user_code],
                        "Dokumentationskod": [selected_code],
                        "Dokumentation": [doc_text],
                        "Tolkning": [user_interpretation if user_interpretation.strip() != "" else "Muntlig tolkning"],
                        "Muntlig tolkning markerad": ["Ja" if oral_interpretation else "Nej"]
                    })

                    # Kontrollera om filen redan finns
                    if os.path.exists(interpret_csv_file):
                        existing_data = pd.read_csv(interpret_csv_file, dtype=str)
                        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
                    else:
                        updated_data = new_data

                    updated_data.to_csv(interpret_csv_file, index=False)  # Spara utan index
                    st.success("Tolkningen har sparats och skickats in!")
