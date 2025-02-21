import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Filnamn för datafiler
doc_csv_file = "responses.csv"  # Filen med dokumenterade patientfall
interpret_csv_file = "interpretations.csv"  # Här sparas tolkningarna

# 🔹 **Titel**
st.title("Tolkning av Patientscenario 6")

# 🔹 **Ange studiekod och begränsa bredden till 50% med columns**
col1, col2 = st.columns([1, 1])  # 50% / 50%
with col1:
    user_code = st.text_input("Ange din egen studiekod (den du fått av intervjuaren):")
if user_code:
    st.success("Studiekod registrerad!")

# 🔹 **Ladda in data och rensa kolumnnamn från dolda mellanslag**
if os.path.exists(doc_csv_file):
    df = pd.read_csv(doc_csv_file, dtype=str)
    df.columns = df.columns.str.strip()  # Tar bort eventuella mellanslag i kolumnnamn
    df["Kod"] = df["Kod"].astype(str).str.strip()  # Rensa mellanslag från koder
else:
    df = pd.DataFrame()

# 🔹 **Om det finns data, låt tolken välja en dokumentationskod att tolka**
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
        # 🔹 **Definiera variabeln relevant_cols**
        relevant_cols = ["Andfåddhet", "Astma", "Betablockerare", "Lungröntgen"]

        # 🔹 **Hämta den senaste dokumenterade raden med faktiska värden**
        patient_data = df[df["Kod"] == selected_code].dropna(subset=relevant_cols).tail(1)

        # Om data hittas, konvertera till Series för enkel åtkomst
        if not patient_data.empty:
            patient_data = patient_data.iloc[0]

            st.write("### Dokumenterad information att tolka:")
            st.write("Vi läser nu vad en kollega dokumenterat om patient Aaro Niemi, 80 år, som inkommit till sjukhuset.")

            # 🔹 **Lista med dokumenterade uppgifter, ersätter 'Lungröntgen' med 'Finns svar på lungröntgen'**
            column_rename = {
                "Andfåddhet": "Andfåddhet",
                "Astma": "Astma",
                "Betablockerare": "Betablockerare",
                "Lungröntgen": "Finns svar på lungröntgen"  # Ändring här!
            }

            doc_text = "\n".join(
                [f"- **{column_rename.get(col, col)}:** {patient_data[col]}" 
                 for col in relevant_cols if col in patient_data and pd.notna(patient_data[col])]
            )

            st.markdown(doc_text)

            # 🔹 **Lägg till en beskrivning av statusarna under dokumentationen**
            st.markdown("""
            #### <span style='font-size:18px;'>Förklaring av statusar</span>

            - **Bekräftad** – *Det finns tillräckligt med bevis för att fastställa förekomsten av patientens tillstånd.*  
            - **Motbevisad** – *Detta tillstånd har uteslutits av efterföljande diagnostiska och kliniska bevis.*  
            - **Obekräftad** – *Det finns inte tillräckligt med bevis för att fastställa förekomsten av patientens tillstånd.*  
            - **Provisorisk** – *Detta är en preliminär diagnos - fortfarande en kandidat som övervägs.*  
            - **Differential** – *En av en uppsättning potentiella (och vanligtvis ömsesidigt uteslutande) diagnoser som anges för att ytterligare vägleda den diagnostiska processen och preliminär behandling.*  
            """, unsafe_allow_html=True)

            # 🔹 **Tolkningsfrågor**
            st.write("### Tolkningsfrågor")
            st.write("Uppfattar du utifrån informationen ovan att patienten har följande symtom/diagnoser/behandlingar?")
            for col in relevant_cols:
                st.write(f"**{column_rename.get(col, col)}?**")  # Ändrar även här!

            # 🔹 **Skriv eller diktera tolkningen**
            st.write("### Skriv, eller berätta muntligt, din tolkning (som om du dikterar journalanteckning):")
            st.write("Skriv/berätta i stil med:")

            # 🔹 **Lägg till ett kursiverat exempel på diktatformulering**
            st.markdown('*"Patienten har .............., har inte .............., osäkert om .............., vi känner inte till om .............."*')

            user_interpretation = st.text_area("")

            # 🔹 **Checkbox för muntlig tolkning**
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
