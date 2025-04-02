import streamlit as st

# 🛠️ Sidkonfiguration: titel + emoji-ikon (fungerar i fliken!)
st.set_page_config(
    page_title="Negationsprojekt",
    page_icon="👋",  # Detta är emojin som syns i fliken
    layout="centered"
)

# 🩺 Titel och innehåll
st.title("Projekt för dokumentation och hantering av negationer inom vård och omsorg")

st.header("Välkommen!")
st.write("""
Med detta projekt vill vi bidra till att möjligtvis förbättra dokumentationen och hanteringen av negationer inom vården.
Negationer, som att en patient inte har en viss sjukdom eller att inga kända allergier finns, är viktiga
för att skapa en korrekt och säker medicinsk journal. Genom att strukturera denna information
på ett standardiserat sätt kan vi förbättra informationsutbytet och säkerställa att viktiga 
negationer bevaras korrekt.
""")

st.header("Syfte")
st.write("""
Det övergripande syftet med denna studie är att undersöka hur olika informationsmodeller stödjer dokumentation och tolkning av negationer inom hälso- och sjukvården, med fokus på upplevd användbarhet och semantisk interoperabilitet. Resultaten förväntas bidra till en ökad förståelse för hur strukturerad dokumentation kan främja interoperabilitet i kliniska sammanhang.
""")

st.header("Bakgrund")
st.write("""
Inom vården är det avgörande att kunna dokumentera inte bara positiva fynd, som att en patient har en viss sjukdom,
utan också negationer, såsom "ingen känd hjärtsjukdom" eller "inga tidigare operationer". Informationen om negationer 
är ofta otydligt strukturerad eller dokumenteras i fritext, vilket gör det svårt att återanvända den korrekt.

Genom detta projekt strävar vi efter att utforska strukturerade metoder för att dokumentera negationer på ett sätt
som möjliggör säkrare användning av data och ett bättre informationsutbyte mellan vårdpersonal och system.
""")

# 📬 Kontakt
st.header("Kontaktinformation")
st.write("""
Om du har frågor om projektet eller vill veta mer, vänligen kontakta anna.axell@stud.ki.se eller anna.rossander@ki.se  
""")
