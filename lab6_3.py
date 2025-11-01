import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import date

CSV_PATH = "employees.csv"

def calculate_age(birthdate):
    if pd.isna(birthdate):
        return None
    if isinstance(birthdate, str):
        birthdate = pd.to_datetime(birthdate).date()
    elif isinstance(birthdate, pd.Timestamp):
        birthdate = birthdate.date()
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def categorize_age(age):
    if age is None:
        return None
    if age <= 17:
        return "younger_18"
    elif 18 <= age <= 45:
        return "18-45"
    elif 46 <= age <= 70:
        return "45-70"
    else:
        return "older_70"

def safe_read_csv(path):
    if not os.path.exists(path):
        print("Помилка: CSV файл відсутній або неможливо відкрити.")
        return None
    try:
        df = pd.read_csv(path, encoding="utf-8-sig", delimiter=';')
        print("Ok")
        return df
    except Exception as e:
        print("Помилка при відкритті CSV:", e)
        return None

def plot_pie(labels, sizes, title):
    plt.figure()
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title(title)
    plt.show()

def plot_bar(x, y, title, xlabel=None, ylabel=None):
    plt.figure()
    plt.bar(x, y)
    plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    plt.show()

def main():
    df = safe_read_csv(CSV_PATH)
    if df is None:
        return

    gender_map = {"Ж": "Female", "Ч": "Male", "F": "Female", "M": "Male"}
    df["Стать_Норм"] = df["Стать"].map(lambda s: gender_map.get(s, "Unknown"))

    gender_counts = df["Стать_Норм"].value_counts()
    print("Кількість по статі:")
    print(gender_counts.rename_axis(None).to_string())
    plot_pie(gender_counts.index.tolist(), gender_counts.values.tolist(), "Розподіл статі")

    df["Дата народження"] = pd.to_datetime(df["Дата народження"], errors="coerce")
    df["Вік"] = df["Дата народження"].apply(calculate_age)
    df["Вікова_група"] = df["Вік"].apply(categorize_age)

    age_group_counts = df["Вікова_група"].value_counts().reindex(["younger_18","18-45","45-70","older_70"]).fillna(0).astype(int)
    print("\nКількість по віковим групам:")
    print(age_group_counts.rename_axis(None).to_string())
    plot_bar(age_group_counts.index.tolist(), age_group_counts.values.tolist(), "Кількість співробітників за віковими групами", xlabel="Група", ylabel="Кількість")

    groups = ["younger_18","18-45","45-70","older_70"]
    for g in groups:
        sub = df[df["Вікова_група"] == g]
        counts = sub["Стать_Норм"].value_counts()
        print(f"\nГрупа {g} - статі:")
        print(counts.rename_axis(None).to_string())
        if counts.sum() > 0:
            plot_pie(counts.index.tolist(), counts.values.tolist(), f"Стать у групі {g}")

    pivot = pd.crosstab(df["Вікова_група"], df["Стать_Норм"]).reindex(index=groups).fillna(0)
    print("\nТаблиця кількостей (вік x стать):")
    print(pivot.rename_axis(None).to_string())
    pivot.plot(kind='bar', stacked=False)
    plt.title("Кількість по вікових групах та статі")
    plt.xlabel("Вікова група")
    plt.ylabel("Кількість")
    plt.show()

if __name__ == "__main__":
    main()
