import sqlite3
import pandas as pd

# CSV faylını oxu
df = pd.read_csv(r"webScraping.csv", header = None, skip_blank_lines=False, encoding="utf-8")  # Sənin CSV faylının adı buraya gəlməlidir

# SQLite verilənlər bazasına qoşul (Əgər "masinlar.db" yoxdursa, yaradılacaq)
conn = sqlite3.connect("trucks.db")
cursor = conn.cursor()

# Cədvəli yaradın (Əgər artıq varsa, bu hissəni əlavə etməyə ehtiyac yoxdur)
for index, row in df.iterrows():
    cursor.execute(
        (row["price"], row["year"], row["motor"], row["distance"])
    )

# CSV-dən gələn məlumatları SQL-ə yaz
df.to_sql("webScraping", conn, if_exists="append", index=False)

# Bağlantını bağla
conn.commit()
conn.close()

print("Məlumatlar uğurla SQLite bazasına yazıldı!")