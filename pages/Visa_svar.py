import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Visa insamlade svar 📊", page_icon="📊", layout="centered")

# 🔐 Enkel lösenordsspärr
correct_password = "annaanna"
password = st.text_input("Ange lösenord för att visa denna sida:", type="password")

if password != correct_password:
    st.warning("Denna sida är lösenordsskyddad.")
    st.stop()

# 📁 Filnamn
csv_file = "responses.csv"

# 🧾 Introduktion
st.title("📊 Visa insamlade svar")
st.markdown("""
Här kan du granska inskickade svar från patientscenarierna.  
Du kan söka på studiekod eller visa hela listan, och ladda ner datan som CSV-fil för analys eller dokumentation.
""")

# 🔍 Ladda in datan
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file, dtype=str)
    df.columns = df.columns.str.strip()
else:
    st.warning("Ingen data hittades. Vänta tills någon har skickat in svar.")
    df = pd.DataFrame()

# 🔎 Sök på studiekod
st.write("### Sök efter en specifik studiekod")
user_search = st.text_input("Ange en studiekod (001–020):")

if user_search:
    user_search = user_search.zfill(3)
    filtered_df = df[df["Studiekod"] == user_search]

    if filtered_df.empty:
        st.warning(f"Inga svar hittades för studiekod {user_search}.")
    else:
        st.write(f"### Svar för studiekod {user_search}")
        answered_cases = sorted(filtered_df["Patientfall"].dropna().unique())
        st.write(f"📌 **Patientfall besvarade:** {', '.join(answered_cases)}")
        st.dataframe(filtered_df)

# 📋 Visa alla svar
elif not df.empty:
    st.write("### Alla insamlade svar")
    st.dataframe(df)

# 💾 Ladda ner CSV
if not df.empty:
    st.markdown("#### Ladda ner alla svar som CSV")
    st.download_button(
        label="📥 Klicka här för att ladda ner",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="insamlade_svar.csv",
        mime="text/csv"
    )
