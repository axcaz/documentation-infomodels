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
all_codes = sorted(df["Studiekod"].unique().tolist())

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

        # Exkludera metadata
        exclude = ["Datum", "Studiekod", "Patientfall", "Dokumentationssäkerhet"]
        relevant_data = patient_data.drop(labels=[col for col in exclude if col in patient_data.index])
        filled = {k: v for k, v in relevant_data.items() if pd.notna(v) and v.strip() != ""}

        # 🔍 Visa förklaring om "Aktiv/Inaktiv" används
        status_values = " / ".join(filled.values())
        if "Aktiv" in status_values or "Inaktiv" in status_values:
            with st.expander("ℹ️ Vad betyder statusen Aktiv/Inaktiv?"):
                st.markdown("""
                **Aktiv**: Problem där patienten upplever symtom eller där det finns evidens för att problemet föreligger.  
                **Inaktiv**: Problem som inte längre påverkar patienten eller där det saknas evidens för fortsatt existens.
                """)

        # Visa dokumenterad text
        doc_text = "\n".join([f"- **{key}:** {val}" for key, val in filled.items()])
        st.markdown(doc_text if doc_text else "_Inga dokumenterade variabler hittades._")
    else:
        st.warning("Ingen dokumentation hittades för denna kod.")
        filled = {}
        doc_text = ""

    if filled:
        # Fråga
        st.markdown("""
        ### Tolkningsfråga
        Texten ovan är din kollegas dokumentation om symtom existerar eller inte.  
        Uppfattar du utifrån informationen ovan att patienten har följande symtom/diagnoser/behandlingar?  
        Du får svara med vilka ord du vill.
        """)

        for key in filled.keys():
            st.write(f"– {key}")

        # Självskattad upplevelse av dokumentationsstrukturen
        st.markdown("<h3 style='margin-top: 3.5rem; margin-bottom: 0.5rem;'>Självskattad upplevelse av dokumentationsstrukturen</h3>", unsafe_allow_html=True)

        # Flytta slidertexten utanför st.slider() för kontroll
        st.markdown("<p style='margin-top: -0.5rem;'>📊 Markera på skalan hur du uppfattar den struktur du nyss använde:</p>", unsafe_allow_html=True)

        # Slider utan synliga siffror
        confidence = st.slider("", min_value=1, max_value=7, value=4, format=" ")

        # Etiketter under slidern
        st.markdown("""
        <div style='font-size: 1rem; color: #1f77b4; font-weight: bold; display: flex; justify-content: space-between; margin-bottom: 1.5rem;'>
            <span>Svårtydd</span>
            <span>Begriplig</span>
        </div>
        """, unsafe_allow_html=True)

        # Visa det valda värdet
        st.markdown(f"<p style='font-size: 0.95rem; color: gray;'>Du skattade: <strong>{confidence}</strong> på skalan 1–7</p>", unsafe_allow_html=True)
