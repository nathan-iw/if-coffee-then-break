from crontab import CronTab

my_cron = CronTab(user='nathanhart')
job = my_cron.new(command='python3 /home/nathanhart/Documents/Data_Academy/IF-COFFEE-THEN-BREAK/if-coffee-then-break/myface.py',comment='comment')
job.minute.every(1) # generates: */2 * * * *
my_cron.write()
# my_cron.remove_all(comment='testing')

for job in my_cron:
    print(job)

# 