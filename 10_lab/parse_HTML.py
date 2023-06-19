from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass


@dataclass
class Teacher:
    name: str
    email: str


def get_teachers(letter: str):
    url = f"https://wit.pwr.edu.pl/en/faculty/structure/employees?letter={letter}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    teachers = []
    for teacher in soup.find_all("div", class_="news-box"):
        name = teacher.find("a", class_="title").text
        email = teacher.find("p").text.split(": ")[1]
        teachers.append(Teacher(name, email))
    return teachers


def print_teachers(letter: str):
    teachers = get_teachers(letter)
    if not teachers:
        print(f"No teachers found with last name starting with {letter}")
        return
    print(f"The list of researchers - {letter}")
    for teacher in teachers:
        print(f"{teacher.name} - {teacher.email}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--teachers",
        help="Print list of teachers with last name starting with given letter",
    )
    args = parser.parse_args()
    if args.teachers:
        print_teachers(args.teachers)

# python parse_HTML.py --teachers P
