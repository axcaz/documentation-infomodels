import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Tolkning 👨‍💻", page_icon="👨‍💻", layout="centered")

# Filnamn
doc_csv_file = "responses.csv"
interpret_csv_file = "interpretations.csv"

# Titel
st.title("Tolkning av dokumenterat patientscenario")

# Studiekod för tolkare
col1, col2 = st.columns([1, 1])
with col1:
    user_code = st.text_input("Ange din egen studiekod (den du fått av intervjuaren):")
if user_code:
    user_code = user_code.zfill(3)
    st.success(f"Studiekod registrerad: {user_code}")

# Ladda in data
if os.path.exists(doc_csv_file):
    df = pd.read_csv(doc_csv_file, dtype=str)
    df.columns = df.columns.str.strip()
    df["Studiekod"] = df["Studiekod"].astype(str).str.zfill(3)
else:
    st.error("Kunde inte hitta responses.csv.")
    st.stop()

# Lista med alla koder
all_codes = [str(i).zfill(3) for i in range(1, 21)]

# Välj dokumentationskod
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    selected_code = st.selectbox("Välj dokumentationskod att tolka:", ["Välj dokumentationskod"] + all_codes)

if selected_code and selected_code != "Välj dokumentationskod":
    patient_data = df[df["Studiekod"] == selected_code].dropna(how="all")

    if not patient_data.empty:
        patient_data = patient_data.tail(1).iloc[0]
        patient_case = patient_data.get("Patientfall", "Okänt fall")
        st.write(f"### Dokumentation för {patient_case}")

        exclude = ["Datum", "Studiekod", "Patientfall", "Dokumentationssäkerhet"]
        relevant_data = patient_data.drop(labels=[col for col in exclude if col in patient_data.index])
        filled = {k: v for k, v in relevant_data.items() if pd.notna(v) and v != ""}
        doc_text = "\n".join([f"- **{key}:** {val}" for key, val in filled.items()])
        st.markdown(doc_text if doc_text else "_Inga dokumenterade variabler hittades._")
    else:
        st.warning("Ingen dokumentation hittades för denna kod.")
        doc_text = ""

    # Tolkningsfrågor
    st.write("### Tolkningsfrågor")
    st.write("Uppfattar du utifrån informationen ovan att patienten har följande symtom/diagnoser/behandlingar?")
    for key in filled.keys():
        st.write(f"**{key}?**")

    # Skattning 1–7
    st.write("### Hur säker är du på din tolkning?")
    confidence = st.slider("Skatta säkerhet", 1, 7, 4)

    # Tolkningsfält
    st.write("### Skriv eller diktera tolkningen")
    st.markdown('*"Patienten har .............., har inte .............., osäkert om .............., vi känner inte till om .............."*')
    user_interpretation = st.text_area("")

    oral_interpretation = st.checkbox("Jag har berättat muntligt istället för att skriva.")

    # Spara tolkning
    if st.button("Skicka in"):
        if user_interpretation.strip() == "" and not oral_interpretation:
            st.warning("Du måste skriva något eller markera att du berättat muntligt.")
        else:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_data = pd.DataFrame({
                "Datum": [current_time],
                "Tolkens studiekod": [user_code],
                "Dokumentationskod": [selected_code],
                "Patientfall": [patient_case],
                "Dokumentation": [doc_text],
                "Tolkning": [user_interpretation if user_interpretation.strip() != "" else "Muntlig tolkning"],
                "Muntlig tolkning markerad": ["Ja" if oral_interpretation else "Nej"],
                "Tolkningssäkerhet": [confidence]
            })

            if os.path.exists(interpret_csv_file):
                existing_data = pd.read_csv(interpret_csv_file, dtype=str)
                updated_data = pd.concat([existing_data, new_data], ignore_index=True)
            else:
                updated_data = new_data

            updated_data.to_csv(interpret_csv_file, index=False)
            st.success("Tolkningen har sparats och skickats in! ✨")
