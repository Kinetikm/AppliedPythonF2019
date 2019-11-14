from crontab import CronTab
from time import time
import sys
import os

new_cron = CronTab(user=True)
job = new_cron.new(
    command='python3 {}/mail_cron.py'.format(os.path.dirname(os.path.abspath(__file__))))
job.hour.on(8)
job.day.every(1)
new_cron.write()
