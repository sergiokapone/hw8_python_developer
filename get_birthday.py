import csv
from datetime import datetime, timedelta


""" Зчитуванні інформації про дати народження з csv-файлу та формування
    на його основі списка словників users
"""

filename = "birthdays.csv"

users = []

with open(filename, "r") as data:
    for line in csv.DictReader(data, delimiter=";"):
        line["Born"] = datetime.strptime(line["Born"], "%d.%m.%Y").date()
        users.append(line)


def get_birthdays_per_week(users):
    """Функція виводить список колег, яких потрібно привітати з днем народження на тижні."""

    # Береться опорний день -- субота. Всі дні народження будуть виводитись,
    # починаючи з цього дня і далі.

    saturday = get_last_saturday()

    user_birthdays = map(
        lambda user: (
            user["Born"].replace(year=saturday.year).strftime("%A"),
            user["Name"],
        ),
        filter(
            lambda user: -6
            <= (saturday - user["Born"].replace(year=saturday.year)).days
            <= 0,
            users,
        ),
    )

    d = {}
    for k, v in user_birthdays:
        if k in ("Saturday", "Sunday"):
            k = "Monday"
        d.setdefault(k, []).append(v)

    m = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    for i in m:
        if d.get(i):
            print(i, end=": ")
            print(*d[i], sep=", ")


def get_last_saturday():
    current_time = datetime.now()
    last_saturday = (
        current_time.date()
        - timedelta(days=current_time.weekday())
        + timedelta(days=5, weeks=0)
    )
    return last_saturday


if __name__ == "__main__":

    get_birthdays_per_week(users)
