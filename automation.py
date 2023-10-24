from crontab import CronTab
import json
cron  = CronTab(user=True)  # current users cron

def script(next_game):
    cron_cmd = "cd /home/matt/coding/jubilant-broccoli && /usr/bin/python3 main.py"
    job = cron.new(command=cron_cmd)
    # 1. get next fixture
    date = next_game['response'][0]['fixture']['date']
    print(date)
    # 2. set cron schedule to run script on next fixture date
    job.setall(f'30 20 {date[8:10]} {date[5:7]} *')
    cron.write()
