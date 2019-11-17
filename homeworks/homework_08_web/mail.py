from auth import db, Cookies
import json
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'zakhar@yandex.ru'
PASSWORD = 'my-VeRyy_secret-p@ssw0rd'
with open("cron_data.json", "r") as f:
    data = json.loads(f.read())
users = [f'user={r.username}, email={r.email}' for r in db.session.query(Cookies).filter_by(id_ < data[1]).distinct()]
data[1] += len(usernames)
with open("cron_data.json", "w") as f:
    json.dump(data, f)
users = '; '.join(users)
message = users
s = smtplib.SMTP(host=, port=your_port_here)
s.starttls()
s.login(MY_ADDRESS, PASSWORD)
msg = MIMEMultipart()
msg['From'] = MY_ADDRESS
msg['To'] = data[0]
msg['Subject'] = "New Users"
msg.attach(MIMEText(message, 'plain'))
s.send_message(msg)
del msg
s.quit()
