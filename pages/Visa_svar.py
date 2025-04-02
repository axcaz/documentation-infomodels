import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Visa insamlade svar  📊", page_icon="📊", layout="centered")

# Filnamn för data
csv_file = "responses.csv"  # Fil med insamlade svar

# 🔹 **Titel**
st.title("📊 Visa insamlade svar")

# 🔹 **Ladda in data**
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file, dtype=str)
    df.columns = df.columns.str.strip()  # Tar bort eventuella mellanslag i kolumnnamn
else:
    st.warning("Ingen data hittades. Vänta tills det finns insamlade svar.")
    df = pd.DataFrame()

# 🔹 **Filtrera på studiekod**
st.write("### Sök efter en specifik studiekod")
user_search = st.text_input("Ange en studiekod (001-020) för att filtrera svar:")

if user_search:
    user_search = user_search.zfill(3)  # Säkerställ att studiekoden är i format 001-020
    filtered_df = df[df["Studiekod"] == user_search]
    
    if filtered_df.empty:
        st.warning(f"Inga svar hittades för studiekod {user_search}.")
    else:
        st.write(f"### Svar för studiekod {user_search}")
        
        # 🔹 **Visa vilka patientfall personen har svarat på**
        answered_cases = sorted(filtered_df["Patientfall"].unique())
        st.write(f"📌 **Patientfall besvarade:** {', '.join(answered_cases)}")
        
        # Visa datatabellen
        st.dataframe(filtered_df)

# 🔹 **Visa hela tabellen om ingen studiekod är angiven**
if user_search == "":
    st.write("### Alla insamlade svar")
    st.dataframe(df)

# 🔹 **Ladda ner data som CSV**
if not df.empty:
    st.download_button(
        label="📥 Ladda ner all data som CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name="insamlade_svar.csv",
        mime='text/csv'
    )
