import streamlit as st
import pandas as pd
import os
import re

# Måste vara första Streamlit-raden på sidan
st.set_page_config(page_title="Visa insamlade svar 📊", page_icon="📊", layout="centered")

# 🔐 Lösenord (unik key)
correct_password = "annaanna"
password = st.text_input("Ange lösenord för att visa denna sida:", type="password", key="pw_visasvar")
if password != correct_password:
    st.warning("Denna sida är lösenordsskyddad.")
    st.stop()

csv_file = "responses.csv"

st.title("📊 Visa insamlade svar")
st.markdown("""
Här kan du granska inskickade svar från patientscenarierna.  
Du kan söka på studiekod eller visa hela listan, och ladda ner datan som CSV-fil för analys eller dokumentation.
""")

# 🔍 Läs data
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file, dtype=str, encoding="utf-8")
    df.columns = df.columns.str.strip()
    if "Studiekod" in df.columns:
        # Normalisera kolumnen i filen till 3-siffrig sträng
        df["Studiekod"] = (
            df["Studiekod"]
            .astype(str).str.strip()
            .str.extract(r"(\d+)", expand=False)  # ta bara siffror
            .fillna("").str.zfill(3)
        )
else:
    st.warning("Ingen data hittades. Vänta tills någon har skickat in svar.")
    df = pd.DataFrame()

# 🔎 Input för studiekod (unik key)
st.subheader("Sök efter en specifik studiekod")
code_input = st.text_input("Ange exakt tre siffror (001–100), t.ex. 011:", max_chars=3, key="studiekod_visasvar").strip()

# Standard: visa allt
df_view = df
export_name = "insamlade_svar.csv"
show_all_header = True

# Strikt validering – filtrera bara vid exakt tre siffror
if code_input:
    if re.fullmatch(r"\d{3}", code_input):
        code = code_input  # INGEN zfill på användarens input
        df_view = df[df["Studiekod"] == code]
        show_all_header = False
        if df_view.empty:
            st.warning(f"Inga svar hittades för studiekod {code}.")
        else:
            st.write(f"### Svar för studiekod {code}")
            if "Patientfall" in df_view.columns:
                answered = sorted(df_view["Patientfall"].dropna().unique())
                if answered:
                    st.write(f"📌 **Patientfall besvarade:** {', '.join(answered)}")
            export_name = f"svar_{code}.csv"
    else:
        st.error("Ange **exakt tre siffror** (t.ex. 005, 011).")

# Visa tabell
if show_all_header:
    st.write("### Alla insamlade svar")
st.dataframe(df_view, use_container_width=True)

# 💾 Ladda ner exakt det som visas
if not df_view.empty:
    st.markdown("#### Ladda ner visade svar som CSV")
    st.download_button(
        label="📥 Klicka här för att ladda ner",
        data=df_view.to_csv(index=False).encode("utf-8-sig"),  # BOM → snyggt i svensk Excel
        file_name=export_name,
        mime="text/csv",
    )
