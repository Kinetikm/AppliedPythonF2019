import smtplib
from data_processing import get_last_users
import json


def send_new_users():
    server = "localhost"

    config = None

    with open("config.json", "r") as f:
        config = json.loads(f.read())

    fromm = "flights_service@example.com"
    to = [config["address"]]
    subject = "New users"

    text = get_last_users(config["already_sent"])
    config["already_sent"] += len(text)
    text = ", ".join(["{}: {}".format(i.login, i.email) for i in text])
    print(text)
    # with open("config.json", "w") as f:
    #     json.dump(config, f)

    # message = """\
    # from: %s
    # to: %s
    # subject: %s

    # %s
    # """ % (fromm, ", ".join(to), subject, text)

    # server = smtplib.SMTP(server)
    # server.sendmail(fromm, to, message)
    # server.quit()
