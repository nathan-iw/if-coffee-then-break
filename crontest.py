#!/usr/bin/python
import datetime

with open('/Users/nathanhart/Documents/Data_Academy/IF-COFFEE-THEN-BREAK/if-coffee-then-break/requirements.txt','a') as outFile:
    outFile.write('\n' + str(datetime.datetime.now()) + ' it worked with cron')