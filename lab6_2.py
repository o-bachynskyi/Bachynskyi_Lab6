import pandas as pd
from datetime import date
import sys
import os

CSV_PATH = "employees.csv"
XLSX_PATH = "employees_by_age.xlsx"

def calculate_age(birthdate):
    if isinstance(birthdate, str):
        birthdate = pd.to_datetime(birthdate).date()
    elif isinstance(birthdate, pd.Timestamp):
        birthdate = birthdate.date()
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def categorize_age(age):
    if age <= 17:
        return "younger_18"
    elif 18 <= age <= 45:
        return "18-45"
    elif 46 <= age <= 70:
        return "45-70"
    else:
        return "older_70"

def main():
    if not os.path.exists(CSV_PATH):
        print("Помилка: CSV файл не знайдено або проблеми при відкритті CSV.")
        sys.exit(1)

    try:
        df = pd.read_csv(CSV_PATH, encoding="utf-8-sig", delimiter=';')
    except Exception as e:
        print("Помилка при відкритті CSV:", e)
        sys.exit(1)

    try:
        df["Дата народження"] = pd.to_datetime(df["Дата народження"])
    except Exception as e:
        print("Помилка при розборі дат народження:", e)
        sys.exit(1)

    df["Вік"] = df["Дата народження"].apply(calculate_age)
    df_simple = df[["№","Прізвище","Ім'я","По-батькові","Дата народження","Вік"]].copy()

    df_simple["Група"] = df_simple["Вік"].apply(categorize_age)

    try:
        with pd.ExcelWriter(XLSX_PATH, engine="openpyxl") as writer:
            df_simple.to_excel(writer, sheet_name="all", index=False)
            df_simple[df_simple["Група"] == "younger_18"].to_excel(writer, sheet_name="younger_18", index=False)
            df_simple[df_simple["Група"] == "18-45"].to_excel(writer, sheet_name="18-45", index=False)
            df_simple[df_simple["Група"] == "45-70"].to_excel(writer, sheet_name="45-70", index=False)
            df_simple[df_simple["Група"] == "older_70"].to_excel(writer, sheet_name="older_70", index=False)
    except Exception as e:
        print("Помилка при створенні XLSX файлу:", e)
        sys.exit(1)

    print("Ok")

if __name__ == "__main__":
    main()
