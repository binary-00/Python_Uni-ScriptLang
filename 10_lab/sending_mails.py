import smtplib
import argparse
from configparser import ConfigParser
from datetime import datetime


def send_email(to, subject, body):
    config = ConfigParser()
    config.read("config.ini")
    username = config.get("email", "username")
    password = config.get("email", "password")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(username, password)

    message = f"Subject: {subject}\n\n{body}\n\nSent at {datetime.now()}"
    server.sendmail(username, to, message)
    server.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", required=True)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--mail", required=True)
    args = parser.parse_args()

    send_email(args.to, args.topic, args.mail)

## python sending_mails.py --mail "Test Message" --topic "Mails using python" --to "someone@gmail.com"
