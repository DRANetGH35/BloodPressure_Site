from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid, formatdate
import os, smtplib, datetime

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
login_manager = LoginManager()
bootstrap = Bootstrap5()


def send_verification_email(code, address):
    my_email = "bloodpressure@dradigital.net"
    password = os.environ.get('EMAIL_PASSWORD')

    msg = MIMEText(f"Your verification code is {code}")
    msg["Subject"] = "DRADigital Account Verification"
    msg["From"] = formataddr(("BloodPressure", my_email))
    msg["To"] = address
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dradigital.net")

    with smtplib.SMTP("mail.dradigital.net", 587, timeout=20) as server:
        server.starttls()
        server.login(my_email, password)
        server.sendmail(my_email, [msg["To"]], msg.as_string())


def send_reset_link(link, address):
    my_email = "bloodpressure@dradigital.net"
    password = os.environ.get('EMAIL_PASSWORD')

    msg = MIMEText(f"To reset you password, visit the following link \n {link} \n\n If you did not request a password reset, please ignore this email")
    msg["Subject"] = "DRADigital Password Reset"
    msg["From"] = formataddr(("BloodPressure", my_email))
    msg["To"] = address
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dradigital.net")

    with smtplib.SMTP("mail.dradigital.net", 587, timeout=20) as server:
        server.starttls()
        server.login(my_email, password)
        server.sendmail(my_email, [msg["To"]], msg.as_string())