import pandas as pd

# Ange sökvägen till din CSV-fil
csv_file_path = r"C:\Users\PC\OneDrive\Dokument\Master i Hälsoinformatik\KI\Master Thesis Prep\Streamlit\Trial\responses.csv"

# Läs in filen
df = pd.read_csv(csv_file_path, dtype=str)

# Svara på patientfall 1
df.loc[df["Patientfall"] == "1", ["Förhöjt blodtryck", "Stroke", "Allergi mot penicillin", "Operation i buken"]] = [
    "Ja", "Nej", "Vet ej", "Vet ej"
]

# Svara på patientfall 2
df.loc[df["Patientfall"] == "2", ["Blodförtunnande mediciner", "Slagit i huvudet", "Huvudvärk", "Synpåverkan"]] = [
    "Okänt", "Misstänkt", "Bekräftat", "Känt frånvarande"
]

# Svara på patientfall 3
df.loc[df["Patientfall"] == "3", ["Aktuell medicinering", "Bröstsmärta", "Högt blodtryck", "Stroke"]] = [
    "Obekräftad - Provisorisk", "Bekräftad", "Obekräftad - Differential", "Motbevisad"
]

# Svara på patientfall 4
df.loc[df["Patientfall"] == "4", ["Feber", "Ärftlighet för aortaaneurysm", "Ledsmärta", "Konstaterad reumatism"]] = [
    "Bekräftad - Motbevisad", "Misstänkt - Preliminär", "Bekräftad - Arbetsdiagnos", "Misstänkt - Preliminär"
]

# Spara den uppdaterade filen
df.to_csv(csv_file_path, index=False, encoding="utf-8")

print("responses.csv har uppdaterats med rätt svar!")
