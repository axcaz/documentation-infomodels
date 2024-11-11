import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Dokumentationstolkning")

# Låt användaren ange användarkoden för att välja en annan persons dokumentation att tolka
other_user_code = st.text_input("Ange användarkoden för den dokumentation du vill tolka").strip()

if other_user_code:
    try:
        # Läs in dokumentationsfilen och ta bort eventuella mellanslag från användarkoderna
        data = pd.read_csv("negation_data_all.csv", encoding="utf-8-sig")
        
        # Fyll i alla NaN-värden med texten "Saknas"
        data.fillna("Saknas", inplace=True)
        
        # Konvertera alla användarkoder i datafilen till strängar och ta bort eventuella mellanslag
        data["Användarkod"] = data["Användarkod"].astype(str).str.strip()
        
        # Debug: Visa hela datasetet för att kontrollera att det laddas korrekt och användarkoderna är strängar
        st.write("### Hela dokumentationsdatasetet:")
        st.write(data)

        # Kontrollera om användarkoden finns i datasetet efter trimning och konvertering till sträng
        if other_user_code not in data["Användarkod"].values:
            st.warning(f"Användarkoden '{other_user_code}' finns inte i dokumentationen.")
        else:
            # Filtrera för den valda användarkoden
            selected_data = data[data["Användarkod"] == other_user_code]
            
            # Debug: Visa de filtrerade raderna för att se om de visas korrekt
            st.write("### Filtrerad dokumentation för angiven användarkod:")
            st.write(selected_data)
            
            if selected_data.empty:
                st.warning("Ingen dokumentation hittades för den angivna användarkoden.")
            else:
                st.write("### Dokumentation att tolka")
                
                # Ge möjlighet att skriva en tolkning för varje rad
                interpretations = []
                for index, row in selected_data.iterrows():
                    st.write(f"#### Scenario: {row['Scenario']} ({row['Modell']})")
                    st.write(f"- Dokumentation: {row['Kommentar']}")
                    
                    # Inputfält för att tolka denna rad
                    interpretation = st.text_area(f"Tolkning för {row['Scenario']} ({row['Modell']})", key=f"interpretation_{index}")
                    
                    # Spara tolkningen till en lista
                    interpretations.append({
                        "Användarkod": row["Användarkod"],
                        "Scenario": row["Scenario"],
                        "Modell": row["Modell"],
                        "Original kommentar": row["Kommentar"],
                        "Tolkning": interpretation,
                        "Tolkad av": st.session_state.get("user_code", "Ej angivet"),
                        "Tidpunkt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                # Spara tolkningarna till en separat CSV-fil
                if st.button("Spara tolkningar"):
                    interp_df = pd.DataFrame(interpretations)
                    
                    # Försök att läsa in tidigare tolkningar och uppdatera
                    try:
                        existing_interpretations = pd.read_csv("interpretations.csv", encoding="utf-8-sig")
                        updated_interpretations = pd.concat([existing_interpretations, interp_df], ignore_index=True)
                    except FileNotFoundError:
                        # Om filen inte finns, skapa en ny
                        updated_interpretations = interp_df

                    # Spara uppdaterade tolkningar till CSV-fil
                    updated_interpretations.to_csv("interpretations.csv", index=False, encoding="utf-8-sig")
                    st.success("Tolkningar har sparats.")
                    
    except FileNotFoundError:
        st.error("Ingen dokumentation hittades. Se till att dokumentationsfilen finns och att användarkoden är korrekt.")
else:
    st.info("Ange en användarkod för att hämta och tolka dokumentation.")
