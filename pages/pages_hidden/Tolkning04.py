import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Tolkning 👨‍💻", page_icon="👨‍💻", layout="centered")
# Filnamn för datafiler
doc_csv_file = "responses.csv"  # Filen med dokumenterade patientfall
interpret_csv_file = "interpretations.csv"  # Här sparas tolkningarna

# 🔹 **Titel**
st.title("Tolkning av Patientscenario 4")

# 🔹 **Ange studiekod och begränsa bredden till 50% med columns**
col1, col2 = st.columns([1, 1])  # 50% / 50%
with col1:
    user_code = st.text_input("Ange din egen studiekod (den du fått av intervjuaren):")

# Om en kod matas in, säkerställ att den har rätt format (001-020)
if user_code:
    user_code = user_code.zfill(3)  # Konverterar t.ex. "2" till "002"
    st.success(f"Studiekod registrerad: {user_code}")

# 🔹 **Ladda in data och rensa kolumnnamn från dolda mellanslag**
if os.path.exists(doc_csv_file):
    df = pd.read_csv(doc_csv_file, dtype=str)
    df.columns = df.columns.str.strip()  # Tar bort eventuella mellanslag i kolumnnamn
    df["Studiekod"] = df["Studiekod"].astype(str).str.strip().str.zfill(3)  # Säkerställ att alla koder har tre siffror
else:
    df = pd.DataFrame(columns=["Studiekod", "Feber - reumatologi", "Ärftlighet för reumatism", "Ledsmärta", "Reumatism"])

# 🔹 **Generera alla möjliga koder (001-020)**
all_codes = [str(i).zfill(3) for i in range(1, 21)]

# 🔹 **Välj dokumentationskod med 30% bredd**
col1, col2, col3 = st.columns([1, 1.5, 1])  # 30% av bredden på mittenkolumnen
with col2:
    selected_code = st.selectbox(
        "Intervjuaren ger dig en dokumentationskod att tolka:", 
        options=["Välj dokumentationskod"] + all_codes, 
        index=0
    )

if selected_code and selected_code != "Välj dokumentationskod":
    # 🔹 **Definiera relevanta kolumner**
    relevant_cols = ["Feber - reumatologi", "Ärftlighet för reumatism", "Ledsmärta", "Reumatism"]

    # 🔹 **Hämta dokumentationen för det valda fallet**
    patient_data = df[df["Studiekod"] == selected_code]

    st.write("### Dokumenterad information att tolka:")
    st.write("Vi läser nu vad en kollega dokumenterat om patient Stina Eriksson, 52 år, som sökt sig till vårdcentralen.")

    if not patient_data.empty:
        # Ta senaste dokumentationen där minst ett värde är ifyllt
        patient_data = patient_data.dropna(subset=relevant_cols, how="all").tail(1)

        if not patient_data.empty:
            patient_data = patient_data.iloc[0]

            # 🔹 **Lista med dokumenterade uppgifter**
            doc_text = "\n".join(
                [f"- **{col}:** {patient_data[col] if pd.notna(patient_data[col]) else 'NaN'}" 
                 for col in relevant_cols if col in patient_data]
            )
            st.markdown(doc_text)

        else:
            # Om dokumentationskoden finns men saknar data, visa NaN
            doc_text = "\n".join([f"- **{col}:** NaN" for col in relevant_cols])
            st.markdown(doc_text)

    else:
        # Om koden inte finns alls i filen, visa NaN
        doc_text = "\n".join([f"- **{col}:** NaN" for col in relevant_cols])
        st.markdown(doc_text)

    # 🔹 **Förklaring av de olika valen**
    st.markdown("""
    #### <span style='font-size:18px;'>Förklaring av valen</span>

    **Säkerhet**  
    - **Misstänkt**  
      - *Preliminär* - Den initiala diagnosen, som vanligtvis är kopplad till en låg klinisk säkerhet. Den kan förändras när testresultat eller ytterligare råd blir tillgängliga.  
    - **Sannolik**  
      - *Arbetsdiagnos* - En interimistisk diagnos, baserad på en rimlig klinisk säkerhetsnivå men där ytterligare testresultat eller klinisk rådgivning avvaktas. Diagnosen kan fortfarande ändras när mer information blir tillgänglig.  
    - **Bekräftad**  
      - *Fastställd* - Den slutliga och bekräftade diagnosen, baserad på en hög klinisk säkerhet. Den kan inkludera kliniska bevis från testresultat och förväntas inte ändras.  
      - *Motbevisad* - En tidigare registrerad diagnos har kliniskt omvärderats och motbevisats, eller en diagnos har direkt motbevisats med hög klinisk säkerhet. Denna status används för att korrigera fel i patientjournalen.  
    """, unsafe_allow_html=True)

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
