import smtplib
import json
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email():
    with open('config.json', 'r+') as config_file:
        config = json.load(config_file)

    curs = sqlite3.connect(config["db_path"])
    if config["pointer"] == 0:
        data = curs.execute("SELECT email, login FROM users").fetchall()
    else:
        data = curs.execute("SELECT email, login FROM users LIMIT 10000, (?)", (config["pointer"],)).fetchall()

    message = ""
    for line in [" ".join(tpl) for tpl in data]:
        message += line + "\n"

    msg = MIMEMultipart()
    msg['From'] = config['from']['email']
    msg['To'] = config['to']
    msg['Subject'] = "New users"
    msg.attach(MIMEText(message, 'plain'))
    text = msg.as_string()

    server = smtplib.SMTP("smtp.yandex.ru", 587)
    server.ehlo()
    server.starttls()
    server.login(config['from']['email'], config['from']['password'])
    server.auth_plain()
    server.sendmail(config['from']['email'], config['to'], text)
    server.quit()

    config["pointer"] += len(data)
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file)


send_email()
