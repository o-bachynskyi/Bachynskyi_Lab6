import csv
import random
from faker import Faker
from datetime import date

fake = Faker(locale='uk_UA')

NUM_RECORDS = 500
FEMALE_RATIO = 0.40 
MALE_RATIO = 1 - FEMALE_RATIO

START_YEAR = 1938
END_YEAR = 2008

MALE_PATRONYMICS = [
    "Іванович","Петрович","Сергійович","Олександрович","Миколайович",
    "Вікторович","Андрійович","Павлович","Григорович","Володимирович",
    "Юрійович","Степанович","Олегович","Михайлович","Дмитрович",
    "Ігорович","Арсенович","Романoвич","Тарасович","Борисович",
    "Леонідович","Євгенович"
]

FEMALE_PATRONYMICS = [
    "Іванівна","Петрівна","Сергіївна","Олександрівна","Миколаївна",
    "Вікторівна","Андріївна","Павлівна","Григорівна","Володимирівна",
    "Юріївна","Степанівна","Олегівна","Михайлівна","Дмитрівна",
    "Ігорівна","Арсенівна","Романівна","Тарасівна","Борисівна",
    "Леонідівна","Євгенівна"
]

def random_birthdate(year_start=START_YEAR, year_end=END_YEAR):
    year = random.randint(year_start, year_end)
    month = random.randint(1, 12)
    from calendar import monthrange
    day = random.randint(1, monthrange(year, month)[1])
    return date(year, month, day)

def generate_records(num_records):
    records = []
    num_female = int(num_records * FEMALE_RATIO)
    num_male = num_records - num_female

    genders = ['F'] * num_female + ['M'] * num_male
    random.shuffle(genders)

    for i, g in enumerate(genders, start=1):
        if g == 'F':
            first = fake.first_name_female()
            last = fake.last_name_female()
            patronym = random.choice(FEMALE_PATRONYMICS)
            gender_str = "Ж"
        else:
            first = fake.first_name_male()
            last = fake.last_name_male()
            patronym = random.choice(MALE_PATRONYMICS)
            gender_str = "Ч"

        bdate = random_birthdate()
        position = fake.job()
        city = fake.city()
        address = fake.street_address()
        phone = fake.phone_number()
        email = fake.email()

        records.append({
            "№": i,
            "Прізвище": last,
            "Ім'я": first,
            "По-батькові": patronym,
            "Стать": gender_str,
            "Дата народження": bdate.isoformat(),
            "Посада": position,
            "Місто проживання": city,
            "Адреса проживання": address,
            "Телефон": phone,
            "Email": email
        })
    return records

def save_csv(records, path="employees.csv"):
    fieldnames = ["№","Прізвище","Ім'я","По-батькові","Стать","Дата народження","Посада","Місто проживання","Адреса проживання","Телефон","Email"]
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for r in records:
            writer.writerow(r)

def main():
    records = generate_records(NUM_RECORDS)
    save_csv(records)
    print(f"CSV згенеровано: employees.csv ({len(records)} записів)")

if __name__ == "__main__":
    main()
