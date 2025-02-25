import pandas as pd

# Ange sökvägen till din responses.csv-fil
file_path = "C:/Users/PC/OneDrive/Dokument/Master i Hälsoinformatik/KI/Master Thesis Prep/Streamlit/Trial/responses.csv"

# Läs in CSV-filen
df = pd.read_csv(file_path, dtype=str)

# Uppdatera patientfall 5
df.loc[(df["Studiekod"] == "002") & (df["Patientfall"] == "5"), "Feber - infektion"] = "Finns (Bekräftad diagnos eller tillstånd)"
df.loc[(df["Studiekod"] == "002") & (df["Patientfall"] == "5"), "Lunginflammation"] = "Uteslutet (Tillståndet har aktivt bedömts som frånvarande)"
df.loc[(df["Studiekod"] == "002") & (df["Patientfall"] == "5"), "Astma"] = "Preliminärt, bedöm som kliniskt relevant men inte verifierat"
df.loc[(df["Studiekod"] == "002") & (df["Patientfall"] == "5"), "Rökning"] = "Information saknas (Det finns ingen tillgänglig information om tillståndet)"

# Uppdatera patientfall 7 (rökning/röker)
df.loc[(df["Studiekod"] == "002") & (df["Patientfall"] == "7"), "Rökning"] = "Bekräftat närvarande"

# Spara filen
df.to_csv(file_path, index=False)
print("Uppdateringen är klar!")
