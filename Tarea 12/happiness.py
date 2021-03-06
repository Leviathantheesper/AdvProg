# -*- coding: utf-8 -*-
"""
Download world happiness time series from hedonometer project.
See https://hedonometer.org/timeseries/en_all/?from=2020-08-24&to=2022-02-23
Created on Tue Feb 24 15:35:23 2022
@author: Feliú Sagols
CDMX
"""
import datetime
import csv
import requests
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
def retrieve_happiness(list_of_date_intervals):
    #pylint: disable=too-many-locals
    """
    Retrieve happiness records from .csv file generated by download_happiness
    Parameter:
        list_of_date_intervals: [date_interval]
        date_interval=[start_date_string,end_date_string,optional_jump]
    """
    list_of_happiness=[]
    for interval in list_of_date_intervals:
        happinessin=[]
        with open('happiness.csv', mode='r',newline='') as happiness_file:
            reader=csv.reader(happiness_file)
            add_that=False
            continuing=True
            for row in reader:
                start=[int(interval[0][0:4]),int(interval[0][5:7]),
                       int(interval[0][8:10])]
                limit=[int(interval[1][0:4]),int(interval[1][5:7]),
                       int(interval[1][8:10])]
                row_int=[int(row[0][0:4]),int(row[0][5:7]),
                       int(row[0][8:10])]
                gex1=row_int[0]>start[0]
                gex2=row_int[0]==start[0] and row_int[1]>start[1]
                gex3=(row_int[0]==start[0] and row_int[1]==start[1]
                      and row_int[2]>=start[2])
                if gex1 or gex2 or gex3:
                    add_that=True
                if add_that:
                    happinessin.append(row)
                    if len(interval)==3:
                        #pylint doesn't like unused variables so _a instead of a.
                        for _a in range(interval[2]-1):
                            try:
                                row=next(reader)
                            except StopIteration:
                                continuing=False
                row_int=[int(row[0][0:4]),int(row[0][5:7]),
                       int(row[0][8:10])]
                lex1=row_int[0]>limit[0]
                lex2=row_int[0]==limit[0] and row_int[1]>limit[1]
                lex3=(row_int[0]==limit[0] and row_int[1]==limit[1]
                                  and row_int[2]>=limit[2])
                if lex1 or lex2 or lex3:
                    continuing=False
                if not continuing:
                    break
        list_of_happiness.append(happinessin)
    return list_of_happiness
def download_happiness(start_date, records):
    """
    Download happiness records from the url below. Happiness records are stored
    into happiness database table.
    Parameters
    ----------
    start_date : datetime.pyi
        Initial downloading base_date.
    records : int
        Maximum number of records after start_date to download.
    """
    data_json = requests.get(
        'https://hedonometer.org/api/v1/happiness/?format=json&timeseries__'
        f'title=en_all&date__gte='
        f'{start_date.strftime("%Y-%m-%d")}&limit={records}')
    data = data_json.json()
    data = [[
        datetime.datetime.strptime(d['date'], "%Y-%m-%d"), d['frequency'],
        float(d['happiness'])
    ] for d in data['objects']]
    data_strings=[]
    for please_dont_pylint in data:
        data_strings.append([please_dont_pylint[0].strftime("%Y-%m-%d"),
                             str(please_dont_pylint[1]),
                             str(please_dont_pylint[2])])
    with open('happiness.csv', mode='w',newline='') as happiness_file:
        data_writer = csv.writer(happiness_file, delimiter=',', quotechar='"',
                                 quoting=csv.QUOTE_MINIMAL)
        for data_s in data_strings:
            data_writer.writerow(data_s)
if __name__ == "__main__":
    date = datetime.datetime(2022, 1, 1)
    download_happiness(date, 5000)
    #print(retrieve_happiness([['2022-03-24','2022-04-06',3],['2022-03-24','2022-04-06']]))
    #lisa=retrieve_happiness([['2018-01-01', '2022-05-24']])
    ys=[]
    xs=[]
    dates=[]
    equis=0
    with open('happiness.csv', mode='r',newline='') as happiness_file:
        reader=csv.reader(happiness_file)
        for row in reader:
            ys.append(float(row[2]))
            xs.append(equis)
            dates.append(row[0])
            equis+=1
    print(xs)
    print (ys)
    xarrange=np.arange(0, len(xs), 50)
    datearrange=[dates[x] for x in xarrange]
    plt.scatter(xs,ys,s=1)
    plt.yticks(np.arange(min(ys), max(ys)+0.2, 0.05))
    plt.xticks(xarrange,datearrange)
    plt.show()

