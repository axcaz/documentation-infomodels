import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Filnamn för CSV
csv_file = "responses.csv"

# CSS för att styra layouten så att kryssrutan ligger DIREKT EFTER texten
st.markdown("""
    <style>
        .checkbox-label {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 16px;
        }
        .tooltip {
            position: relative;
            display: inline-block;
            cursor: pointer;
            font-weight: 
        }
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 250px;
            background-color: black;
            color: #fff;
            text-align: center;
            padding: 5px;
            border-radius: 5px;
            position: absolute;
            z-index: 1;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            opacity: 0;
            transition: opacity 0.3s;
        }
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        .checkbox-inline {
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Fråga om en unik kod
user_code = st.text_input("Ange din unika kod som du får av intervjuaren och tryck enter:")

# Titel och patientscenario
# Dokumenterat enligt HL7 FHIR ConditionVerificationStatus
st.write("""
### Patientscenario 3: Kent Persson, 67 år
Patienten kommer till akuten med bröstsmärta. Han har aldrig haft en stroke. Han vet inte om han har högt blodtryck.
""")

# HL7 FHIR-alternativ med hierarki och rätt ordning
fhir_main_options = {
    "Confirmed": {
        "description": "There is sufficient diagnostic and/or clinical evidence to treat this as a confirmed condition.",
        "suboptions": None
    },
    "Refuted": {
        "description": "This condition has been ruled out by subsequent diagnostic and clinical evidence.",
        "suboptions": None
    },
    "Unconfirmed": {
        "description": "There is not sufficient diagnostic and/or clinical evidence to treat this as a confirmed condition.",
        "suboptions": {
            "Provisional": "This is a tentative diagnosis - still a candidate that is under consideration.",
            "Differential": "One of a set of potential (and typically mutually exclusive) diagnoses asserted to further guide the diagnostic process and preliminary treatment."
        }
    }
}

# Funktion för att hantera kryssrutor med hover-info och KORREKT placering av kryssrutan
def select_fhir_with_checkbox(label, main_options, key_prefix):
    st.write(f"### {label}")

    selected_main = None
    selected_sub = None

    for option, details in main_options.items():
        # Skapa en flex-container där texten och kryssrutan ligger PÅ SAMMA RAD
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            <div class="tooltip">{option}
                <span class="tooltiptext">{details['description']}</span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            checked = st.checkbox("", key=f"{key_prefix}_{option}")

        if checked:
            selected_main = option

            # Om "Unconfirmed" väljs, visa underval
            if option == "Unconfirmed" and details["suboptions"]:
                st.write("#### Välj ett underalternativ:")
                for suboption, sub_desc in details["suboptions"].items():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"""
                        <div class="tooltip">{suboption}
                            <span class="tooltiptext">{sub_desc}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        sub_checked = st.checkbox("", key=f"{key_prefix}_{suboption}")

                    if sub_checked:
                        selected_sub = suboption

    # Returnera valda alternativ
    if selected_main and selected_sub:
        return f"{selected_main} - {selected_sub}"
    elif selected_main:
        return selected_main
    else:
        return ""

# HL7 FHIR ConditionVerificationStatus
fhir_pain = select_fhir_with_checkbox("Har patienten bröstsmärta?", fhir_main_options, "fhir_pain")
fhir_stroke = select_fhir_with_checkbox("Har patienten haft en stroke tidigare?", fhir_main_options, "fhir_stroke")
fhir_bp = select_fhir_with_checkbox("Har patienten högt blodtryck?", fhir_main_options, "fhir_bp")
fhir_medication = select_fhir_with_checkbox("Finns det information om patientens aktuella medicinering i journalen?", fhir_main_options, "fhir_medication")

# Skicka in svaren
if st.button("Skicka in"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({
        "Datum": [current_time],
        "Kod": [user_code if user_code else "Ej angiven"],
        "Bröstsmärta": [fhir_pain],
        "Stroke": [fhir_stroke],
        "Högt blodtryck": [fhir_bp],
        "Aktuell medicinering": [fhir_medication]
    })

    if os.path.exists(csv_file):
        existing_data = pd.read_csv(csv_file)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(csv_file, index=False)
    st.success("Dina svar har sparats!")
