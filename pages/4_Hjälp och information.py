import streamlit as st

st.title("Hjälp och Information")

# Projektets syfte
st.header("Projektets Syfte")
st.write("""
Detta projekt undersöker hur man bäst kan dokumentera och hantera negationer inom hälso- och sjukvården.
Genom att skapa strukturerade och standardiserade format för att uttrycka negationer, exempelvis "inga kända allergier" eller
"ingen tidigare hjärtsjukdom", strävar projektet efter att förbättra informationsutbyte och patientsäkerhet.
Målet är att identifiera vilka informationsmodeller som ger de mest användbara och säkra sätten att dokumentera denna information.
""")

# Beskrivning av informationsmodellerna
st.header("Informationsmodeller")
st.write("""
Följande informationsmodeller används i projektet för att strukturera dokumentation om negationer:

- **FHIR (Fast Healthcare Interoperability Resources)**: En global standard för vårdinformation som möjliggör delning av information mellan olika system.
- **openEHR**: Ett ramverk och en standard som används för att representera och hantera elektronisk hälsoinformation på ett strukturerat sätt.
- **NIM Hälsotillstånd**: En svensk modell utvecklad av Socialstyrelsen som specificerar standardiserade sätt att dokumentera hälsotillstånd inom vården.
- **eHälsospecifikationer**: En specifikation från eHälsomyndigheten som syftar till att underlätta säker och effektiv hantering av hälsoinformation i Sverige.

Varje modell har olika styrkor och begränsningar, och projektet utforskar deras användbarhet för att dokumentera negationer.
""")

# Kort användarguide
st.header("Användarguide")
st.write("""
### Navigering
Använd sidomenyn till vänster för att navigera mellan de olika flikarna i applikationen.

### Funktioner i applikationen
1. **Dokumentation**: På denna sida kan du dokumentera olika negationer för scenarier, t.ex., "inga kända allergier", enligt olika informationsmodeller.
2. **Dokumentationstolkning**: Här kan du välja en användarkod för att se och tolka en annan användares dokumentation.
3. **Visa och hantera svar**: Här kan du visa sparad data och rensa data om det behövs.

### Att tolka dokumentation
För att tolka en annan användares dokumentation:
1. Gå till **Dokumentationstolkning** och ange användarkoden för dokumentationen du vill tolka.
2. Följ instruktionerna för att granska och skriva din tolkning, som sedan kan sparas för analys.

### Hantering av saknade värden
Alla saknade värden i applikationen visas som "Saknas" för att säkerställa tydlighet och kvalitet i dokumentationen.
""")

# Kontaktinformation
st.header("Kontaktinformation")
st.write("""
Om du har frågor om projektet eller vill veta mer, vänligen kontakta anna.rossander@vgregion.se eller anna.axell@stud.ki.se 
""")
