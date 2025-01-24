import streamlit as st
import pandas as pd
import json

# Titel och patientfall
st.title("Patientfall - Dokumentation av Negationer")

# Patientinformation
st.header("Patientfall")
st.write("""
- **Namn:** Anna Svensson  
- **Ålder:** 45 år  
- **Kön:** Kvinna  
- **Planerad åtgärd:** Laparoskopisk galloperation
- **Bakgrund:** Patienten är inbokad för operation på grund av återkommande gallstensanfall.
""")

# Preoperativ dokumentation (användarvänlig text)
st.header("Preoperativ Dokumentation")
st.write("""
1. **Allergier:** Inga kända allergier  
2. **Blödningssjukdomar:** Ingen historia av blödningssjukdomar  
""")

# Interaktiv dokumentation
st.subheader("Dokumentera negationer")

# Användaren fyller i data
allergies = st.radio("Allergier", ["Inga kända allergier", "Ej dokumenterad"])
bleeding = st.radio("Blödningssjukdomar", ["Ingen historia av blödningssjukdomar", "Ej dokumenterad"])

# När användaren klickar på knappen
if st.button("Spara och exportera dokumentation"):
    # Skapa OpenEHR-representation
    openehr_data = {
        "archetype": "openEHR-EHR-OBSERVATION.problem_diagnosis.v1",
        "data": {
            "allergies": {"value": "No" if allergies == "Inga kända allergier" else "Unknown"},
            "bleeding_disorders": {"value": "No" if bleeding == "Ingen historia av blödningssjukdomar" else "Unknown"}
        }
    }

    # Skapa FHIR-representation
    fhir_data = {
        "resourceType": "Condition",
        "verificationStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                    "code": "refuted" if bleeding == "Ingen historia av blödningssjukdomar" else "unknown",
                    "display": "Refuted" if bleeding == "Ingen historia av blödningssjukdomar" else "Unknown"
                }
            ]
        },
        "code": {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "266569009",  # SNOMED-kod för "Bleeding disorder"
                    "display": "Bleeding disorder"
                }
            ]
        }
    }

    # Visa OpenEHR- och FHIR-data
    st.subheader("OpenEHR-representation")
    st.json(openehr_data)
    
    st.subheader("FHIR-representation")
    st.json(fhir_data)

    # Exportera OpenEHR och FHIR till JSON-filer
    openehr_json = json.dumps(openehr_data, indent=4).encode('utf-8')
    fhir_json = json.dumps(fhir_data, indent=4).encode('utf-8')

    st.download_button(
        label="Ladda ner OpenEHR-data som JSON",
        data=openehr_json,
        file_name="openehr_data.json",
        mime="application/json"
    )

    st.download_button(
        label="Ladda ner FHIR-data som JSON",
        data=fhir_json,
        file_name="fhir_data.json",
        mime="application/json"
    )
