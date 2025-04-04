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
st.markdown("""### Säg gärna högt vad du gör och tänker på när du läser texten nedan.""")

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
    patient_entries = df[df["Studiekod"] == selected_code]

    if patient_entries.empty:
        st.warning("Ingen dokumentation hittades för denna kod.")
    else:
        for idx, row in patient_entries.iterrows():
            patient_case = row.get("Patientfall", f"Fall {idx+1}")
            st.markdown(f"---\n### Dokumentation för {patient_case}")

            # Exkludera metadata
            exclude = ["Datum", "Studiekod", "Patientfall", "Dokumentationssäkerhet"]
            relevant_data = row.drop(labels=[col for col in exclude if col in row.index])
            filled = {k: v for k, v in relevant_data.items() if pd.notna(v) and v.strip() != ""}

            # Förklaring om Aktiv/Inaktiv
            status_values = " / ".join(filled.values())
            if "Aktiv" in status_values or "Inaktiv" in status_values:
                with st.expander("ℹ️ Vad betyder statusen Aktiv/Inaktiv?"):
                    st.markdown("""
                    **Aktiv**: Problem där patienten upplever symtom eller där det finns evidens för att problemet föreligger.  
                    **Inaktiv**: Problem som inte längre påverkar patienten eller där det saknas evidens för fortsatt existens.
                    """)

            # Visa dokumentationen
            doc_text = "\n".join([f"- **{key}:** {val}" for key, val in filled.items()])
            st.markdown(doc_text if doc_text else "_Inga dokumenterade variabler hittades._")

            # Tolkningsfråga
            if filled:
                st.markdown("### Tolkningsfråga")
                st.markdown("""Texten ovan är din kollegas dokumentation om symtom/diagnos/läkemedel/behandling existerar eller inte.  
                Uppfattar du utifrån informationen ovan att patienten har följande symtom/diagnos/läkemedel/behandling?  
                Du får svara med vilka ord du vill.""")

                for key in filled.keys():
                    st.write(f"– {key}")

                # Självskattning
                st.markdown("<h3 style='margin-top: 3.5rem; margin-bottom: 0.5rem;'>Självskattad upplevelse av dokumentationsstrukturen</h3>", unsafe_allow_html=True)
                st.markdown("<p style='margin-top: -0.5rem;'>📊 Markera på skalan hur du uppfattar den struktur du nyss använde:</p>", unsafe_allow_html=True)
                confidence = st.slider(f"Skala för {patient_case}", min_value=1, max_value=7, value=4, format=" ", key=f"slider_{idx}")

                st.markdown("""
                <div style='font-size: 1rem; color: #1f77b4; font-weight: bold; display: flex; justify-content: space-between; margin-bottom: 1.5rem;'>
                    <span>Svårtydd</span>
                    <span>Begriplig</span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"<p style='font-size: 0.95rem; color: gray;'>Du skattade: <strong>{confidence}</strong> på skalan 1–7</p>", unsafe_allow_html=True)
