# -*- coding: utf-8 -*-
"""
Created on Sun May 22 05:55:52 2022

@author: dcmol
"""

import re
import os
import numpy as np
import pandas as pd
#1. Nombre de archivo
def filenames():
    """Computes the names of all the files in the directory"""
    names=[]
    files=[file for file in os.listdir() if os.path.isfile(file)]
    #print(files)
    for file in files:
        namematch=re.search(r"^.*\.", file)
        print(type(namematch))
        if namematch is None:
            names.append(file)
        else:
            name=namematch.group(0)[:-1]
            names.append(name)
    print(names)
    return names
#2. Fecha en español
def date_in_spanish(dateinenglish):
    """Translates date in English"""
    monthsinenglish=['Jan','Apr','Aug','Dec']
    monthsinspanish=['Ene','Abr','Ago','Dic']
    monthmatch=re.search("[A-Z][a-z]{2}", dateinenglish)
    month=monthmatch.group(0)
    if month in monthsinenglish:
        index=monthsinenglish.index(month)
        return dateinenglish.replace(month,monthsinspanish[index])
    return dateinenglish
print(date_in_spanish("01-Dec-2010"))
#3. Convert from standard equity option convention to record rep.
def from_standard_equity_option_convention(code):
    """ Returns
        -------
        dict
        A dictionary containing:
        'symbol': Symbol name
        'expire': Option expiration base_date
        'right': Put (P) or Call (C).
        'strike': Option strike
    """
    symbol=re.match("[A-Z]*",code).group(0)
    symbol_length=len(symbol)
    code=re.sub(r'.', '', code, count = symbol_length)
    date="20"+re.match("[0-9]{6}",code).group(0)
    code=re.sub(r'.', '', code, count = 6)
    right=code[0]
    code=re.sub(r'.', '', code, count = 1)
    number=int(code)//1000
    strike=str(number)
    result={}
    result["symbol"]=symbol
    result["expire"]=date
    result["right"]=right
    result["strike"]=strike
    return result
CODIGO="YHOO150416C00030000"
print(from_standard_equity_option_convention(CODIGO))
#4. Instrucción
SYMBOLS="'hola'"
print(SYMBOLS)
SYMBOLS_STR = re.sub(r"'", "''", str(SYMBOLS))
print(SYMBOLS_STR)
#La instrucción reemplaza las ocurrencias de ' por ''
#5. Escribir una cadena que haga que la siguiente instrucción se ejecute:
ACCOUNT="DU1234567"
if re.match(r'DU[0-9]{7}', ACCOUNT):
    print("Account: ", ACCOUNT)
#6. Simpliicar la expresión regulr.
TEXT="123456"
if re.match('^([0-9][0-9][0-9][0-9][0-9][0-9])$', TEXT):
    print(re.match('^([0-9][0-9][0-9][0-9][0-9][0-9])$', TEXT).group(0))
if re.match('([0-9]{6})$', TEXT):
    print(re.match('([0-9]{6})$', TEXT).group(0))
#re.match busca el patrón al principio del string, así que ^ no es necesario.
#Sí sería necesario al usar re.search.
#7. ¿Cuál es el valor de 'REG_EXP' que hace funcionar el código siguiente?
TEXT="111,2,3,4,33,44,11,22232"
REG_EXP='(([0-9])*,)*[0-9]*$'
if re.match(REG_EXP, TEXT) is None:
    ERROR_MESSAGE = \
        "Try again, your answer does not correspond to a comma " + \
        "separated integers list. Type something like '1, 2, 3' " + \
        "without the apostrophes."
    print(ERROR_MESSAGE)
else:
    print(re.match(REG_EXP, TEXT).group(0))
#8. Programar el método siguiente
def collect_commission_adjustment(data):
    """
    Retrieve a commision adjustment record from the section "Commission
    Adjustments" in one Interactive Brokers activity report.

    PARAMETERS
    ----------
    data : list[]
        Line from the activity report in the "Commission Adjustment" section
        in list format. That is, each element in the list is a comma
        separated item from the line.

    RETURNS
    -------
        dict
        Containing the open position information in dictionary format.

    Examples
    --------
    >>> collect_commission_adjustment(['Commission Adjustments', 'Data', 'USD',
    ... '2021-04-23',
    ... 'Commission Computed After Trade Reported (C     210430C00069000)',
    ... '-1.0906123', '\\n'])
    {'end_date': '20210423', 'symbol': 'C', 'expire': '20210430', \
'right': 'C', 'strike': 69.0, 'sectype': 'OPT', 'amount': -1.0906123}
    >>> collect_commission_adjustment(
    ... ['Commission Adjustments', 'Data', 'USD', '2021-02-19',
    ... 'Commission Computed After Trade Reported (ALB)', '-0.4097', '\\n'])
    {'end_date': '20210219', 'symbol': 'ALB', 'sectype': 'STK', \
'amount': -0.4097}
    >>> collect_commission_adjustment(
    ... ['Commission Adjustments', 'Data', 'USD', '2021-02-19',
    ... 'Commission Computed After Trade Reported (ALB)', '-0.4097', '\\n'])
    {'end_date': '20210219', 'symbol': 'ALB', 'sectype': 'STK', \
'amount': -0.4097}
    """
    end_date_raw=data[3]
    string_containing_transaction=data[4]
    weird_number=data[5]
    codematch=re.search(r"\(.*\w", string_containing_transaction)
    adjustment={}
    code=codematch.group(0)[1:]
    if len(code)>3:
        freoc=from_standard_equity_option_convention(code)
        adjustment['sectype']='OPT'
        adjustment['symbol']=freoc['symbol']
        adjustment['expire']=freoc['expire']
        adjustment['right']=freoc['right']
        adjustment['strike']=freoc['strike']
    else:
        adjustment['sectype']='STK'
        adjustment['symbol']=code
    adjustment['end_date']=end_date_raw.replace("-","")
    adjustment['amount']=weird_number
    return adjustment

d=collect_commission_adjustment(['Commission Adjustments', 'Data', 'USD',
                                 '2021-02-19',
                                 'Commission Computed After Trade Reported (ALB)',
                                 '-0.4097', '\\n'])
c=collect_commission_adjustment(['Commission Adjustments', 'Data', 'USD',
                                 '2021-04-23',
                                 'Commission Computed After Trade Reported (C210430C00069000)',
                                 '-1.0906123', '\\n'])
print(d)
print(c)
#9. Dar dos ejemplos del uso de este método.  Uno donde regrese un float y otro
#un nan
def banxico_value(tag, data):
    """
    Get data values from Banxico portals.
    Parameters
    ----------
    tag : str
        Internal tag name of the variable to retrieve.
    data : str
        Html page to locate the tag value.

    Returns
    --------
        float
        The associated tag value.
    """
    float_nt = "[^0-9-]*([-]*[0-9]+.[0-9]+)[^0-9]"
    try:
        res = float(re.search(tag + float_nt, data).group(1))
    except AttributeError:
        res = np.nan
    return res
#float
TAG="Hola"
DATA="Hola#ABCNOSE-0166A"
print(banxico_value(TAG, DATA))
#nan
TAG="Hola"
DATA="Hol#ABCNOSE-0166A"
print(banxico_value(TAG, DATA))
#10. Describa en palabras qué hace el siguiente código.
dat_df=pd.read_csv("cosas.csv")
col_sel = list(
        map(
            lambda s: s if re.match("[Ii][Mm][Ff][0-9]+", s) else None,
            dat_df.columns,
        ))
print(col_sel)
col_sel = [c for c in col_sel if c is not None]
print(col_sel)
#El código guara los nombres de las columnas de un archivo .csv que sigan el
#patrón "imfx" donde x es un número y las letras pueden ser mayúsculas o
#minúsculas.
