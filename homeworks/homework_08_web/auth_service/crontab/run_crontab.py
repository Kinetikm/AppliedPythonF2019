from crontab import CronTab
import os

cron = CronTab(user=True)
job = cron.new(command='python3 {}/smtp_service.py'.format(os.getcwd()))
job.hour.on(8)
job.day.every(1)
cron.write()
