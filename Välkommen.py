import streamlit as st
import requests
from msal import PublicClientApplication

# Autentisera och hämta åtkomsttoken
def authenticate_graph():
    CLIENT_ID = "d3590ed6-52b3-4102-aeff-aad2292ab01c"  # Microsofts standardklient
    TENANT_ID = "common"  # Använd 'common' för att stödja flera typer av konton
    SCOPES = ["Files.ReadWrite"]  # Behörighet för OneDrive

    app = PublicClientApplication(CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}")
    result = app.acquire_token_interactive(scopes=SCOPES)  # Öppnar en webbläsare för inloggning
    return result["access_token"]

# Funktion för att ladda upp en fil till OneDrive
def upload_to_onedrive(access_token, file_name, file_content):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.put(
        f"https://graph.microsoft.com/v1.0/me/drive/root:/{file_name}:/content",
        headers=headers,
        data=file_content
    )
    if response.status_code == 201:
        return "Filen har laddats upp till OneDrive!"
    else:
        return f"Något gick fel: {response.json()}"


st.title("Projekt för dokumentation och hantering av negationer inom vård och omsorg")

st.header("Välkommen!")
st.write("""
Detta projekt syftar till att förbättra dokumentationen och hanteringen av negationer inom vården.
Negationer, som att en patient inte har en viss sjukdom eller att inga kända allergier finns, är viktiga
för att skapa en korrekt och säker medicinsk journal. Genom att strukturera denna information
på ett standardiserat sätt kan vi förbättra informationsutbytet och säkerställa att viktiga 
negationer bevaras korrekt.
""")

st.header("Syfte")
st.write("""
Syftet med detta projekt är att utforska och jämföra olika informationsmodeller för dokumentation av negationer
inom vården. Genom att testa flera modeller, inklusive **FHIR**, **openEHR**, **NIM Hälsotillstånd** och
**eHälsospecifikationer**, vill vi undersöka vilken modell som bäst stödjer säker och effektiv dokumentation av
negationer. Projektet kan förhoppningsvis bidra till framtida standardisering av hur negationer dokumenteras.
""")

st.header("Bakgrund")
st.write("""
Inom vården är det avgörande att kunna dokumentera inte bara positiva fynd, som att en patient har en viss sjukdom,
utan också negationer, såsom "ingen känd hjärtsjukdom" eller "inga tidigare operationer". Informationen om negationer 
är ofta otydligt strukturerad eller dokumenteras i fritext, vilket gör det svårt att återanvända den korrekt.

Genom detta projekt strävar vi efter att utforska strukturerade metoder för att dokumentera negationer på ett sätt
som möjliggör säkrare användning av data och ett bättre informationsutbyte mellan vårdpersonal och system.
""")
