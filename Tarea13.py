# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 01:09:13 2022

@author: dcmol
"""
import time
import re
import csv
import datetime
import requests

while True:
    hours=[7,8,9,10,11,12,13,14,15,16]
    cur_time=datetime.datetime.today()
    current_time=[cur_time.hour,cur_time.minute,cur_time.second]
    if cur_time.hour<16:
        distances=[a-cur_time.hour if a-cur_time.hour>0 else 25 for a in hours]
        closehour=hours[distances.index(min(distances))]
        wait_time=[closehour-1-current_time[0],59-current_time[1],60-current_time[2]]
        if wait_time[2]==60:
            wait_time[2]=0
            wait_time[1]+=1
        if wait_time[1]==60:
            wait_time[1]=0
            wait_time[0]+=1
        time.sleep(wait_time[2]+wait_time[1]*60+wait_time[0]*3600)
    else:
        time.sleep(60-current_time[2])
        time.sleep(60*(60-current_time[1]))
        time.sleep(3600*(31-current_time[0]))
    cur_time=datetime.datetime.today()
    a=requests.get('https://www.exchangeratewidget.com/converter.php?v=1')
    CONTENT=str(a.content)
    c=re.search('..MXN..=[0-9]+.[0-9]+;',CONTENT)
    d=float(re.search('[0-9]+.[0-9]+',c.group(0)).group(0))
    with open('curex.csv', mode='a',newline='') as f:
        row=[str(cur_time.date()),str(cur_time.time()),d]
        writer = csv.writer(f)
        writer.writerow(row)
        f.close()
    