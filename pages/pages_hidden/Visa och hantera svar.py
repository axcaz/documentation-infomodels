import streamlit as st
import pandas as pd
import os

st.title("Visa och hantera svar")

# Knapp för att visa gemensam data om den finns
if st.button("Visa sparad data"):
    if os.path.exists("negation_data_all.csv"):
        saved_data = pd.read_csv("negation_data_all.csv", encoding="utf-8-sig")
        st.write("### Innehåll i negation_data_all.csv:")
        st.write(saved_data)
    else:
        st.info("Ingen data att visa.")

# Mellanrum mellan knapparna
st.write("")  # En tom rad för att skapa mellanrum
st.markdown("<br><br>", unsafe_allow_html=True)  # Extra mellanrum med HTML

# Knapp för att rensa all data i CSV-filen
if st.button("Rensa all sparad data"):
    if os.path.exists("negation_data_all.csv"):
        os.remove("negation_data_all.csv")  # Ta bort filen
        st.success("All data har raderats.")
    else:
        st.warning("Ingen datafil hittades att rensa.")
