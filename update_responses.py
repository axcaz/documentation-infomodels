import pandas as pd
import os

# Ange sökvägen till din responses.csv-fil
csv_file = "responses.csv"

# Kontrollera om filen existerar
if not os.path.exists(csv_file):
    print(f"Filen {csv_file} hittades inte. Kontrollera att den finns i samma mapp som detta skript.")
    exit()

# Läs in filen
try:
    df = pd.read_csv(csv_file, dtype=str)
    print("Laddade in responses.csv")
except Exception as e:
    print(f"Fel vid inläsning av filen: {e}")
    exit()

# Korrekt kolumnordning
correct_columns = [
    "Förhöjt blodtryck", "Stroke", "Allergi mot penicillin", "Operation i buken", "Datum", "Studiekod", "Patientfall", 
    "Blodförtunnande mediciner", "Slagit i huvudet", "Huvudvärk", "Synpåverkan", "Yrsel", "Migrän", "Lågt blodtryck", 
    "Blodförtunnande medicinering", "Feber", "Lunginflammation", "Astma", "Rökning", "Andfåddhet", "Betablockerare", "Lungröntgen", 
    "Ryggsmärta", "Ärftlighet för reumatism", "Hypertoni", "Aktuell medicinering", "Bröstsmärta", "Högt blodtryck", 
    "Ledsmärta", "Reumatism", "Ärftlighet för aortaaneurysm"
]

# Säkerställ att alla kolumner existerar i rätt ordning
for col in correct_columns:
    if col not in df.columns:
        df[col] = ""

# Omordna kolumner
df = df[correct_columns]

# Spara den uppdaterade filen
updated_csv_file = "responses_updated.csv"
df.to_csv(updated_csv_file, index=False)
print(f"Filen har uppdaterats och sparats som {updated_csv_file}")
