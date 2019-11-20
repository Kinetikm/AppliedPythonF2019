from crontab import Crontab

cron = Crontab(user=True)
job = cron.new(command='python mail.py')
job.hour.on(8)
job.day.every(1)
cron.write()
