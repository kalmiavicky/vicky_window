from crontab import CronTab
import os
cron = CronTab(user=True)
path = os.path.abspath("./lesson2.py")
job = cron.new(command=f"/home/pi/Documents/vicky_window/insert_youbike_data '{path}'")

job.minute.every(2)
job.set_comment("Output hello world")
cron.write()