import random
import string
import time
import datetime
import smtplib
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import enviroment_settings


class EmailActions:
    def send(email, code):
        sender = f"no-reply@{enviroment_settings.YOUR_DOMAIN}"
        receiver = email
        subject = f"{enviroment_settings.YOUR_DOMAIN} - Registration Code"

        custom_email_template_info = {
            "reg_code": str(code),
            "domain": str(enviroment_settings.YOUR_DOMAIN),
            "timestamp": str(datetime.datetime.now(datetime.timezone.utc)),
        }

        with open("./util/assets/email_template.html", "r") as file:
            html_template = file.read()
        soup = BeautifulSoup(html_template, "html.parser")

        for placeholder, value in custom_email_template_info.items():
            for tag in soup.find_all(
                string=lambda text: f"{{{placeholder}}}" in str(text)
            ):
                new_text = tag.replace(f"{{{{{placeholder}}}}}", value)
                tag.replace_with(new_text)
            html_content = str(soup)

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = receiver
        message["Message-Id"] = (
            f"<{time.time()}.{''.join(random.choices(string.ascii_letters + string.digits, k=8))}@mail.pancakepuncher.com>"
        )

        part = MIMEText(html_content, "html")
        message.attach(part)

        with smtplib.SMTP("127.0.0.1:1587") as server:
            server.sendmail(sender, receiver, message.as_string())

        return
