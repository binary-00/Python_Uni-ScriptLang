import smtplib
import argparse
from configparser import ConfigParser
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import pandas as pd


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


def send_email(to, subject, body, attachment=None):
    config = ConfigParser()
    config.read("config.ini")
    username = config.get("email", "username")
    password = config.get("email", "password")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(username, password)

    message = f"Subject: {subject}\n\n{body}\n\nSent at {datetime.now()}"

    if attachment:
        from email.mime.multipart import MIMEMultipart
        from email.mime.base import MIMEBase
        from email.mime.text import MIMEText
        from email.utils import COMMASPACE, formatdate
        from email import encoders

        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = to
        msg["Date"] = formatdate(localtime=True)
        msg["Subject"] = subject

        msg.attach(MIMEText(body))

        part = MIMEBase("application", "octet-stream")
        part.set_payload(open(attachment, "rb").read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment", filename=attachment)
        msg.attach(part)

        server.sendmail(username, to, msg.as_string())
    else:
        server.sendmail(username, to, message)

    server.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", required=True)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--mail", required=True)
    parser.add_argument("--letter", required=True)
    args = parser.parse_args()

    teachers = get_teachers(args.letter)

    if not teachers:
        print(f"No teachers found with last name starting with {args.letter}")

    else:
        df = pd.DataFrame(
            [{"Name": teacher.name, "Email": teacher.email} for teacher in teachers]
        )

        filename = f"teachers_{args.letter}.xlsx"

        df.to_excel(filename, index=False)

        send_email(args.to, args.topic, args.mail, attachment=filename)

# python script.py --to "recipient@example.com" --topic "List of Teachers" --mail "Here is the list of teachers." --letter A
