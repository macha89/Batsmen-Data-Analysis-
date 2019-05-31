from xlrd import open_workbook
import pandas as pd
from datetime import datetime
from copy import copy
#importing modules for data manuplation

wb = open_workbook('data.xlsx') #loading excel file
for s in wb.sheets():#reading the excel row by row
    values = []
    for row in range(3,s.nrows):
        col_value = []
        for col in range(s.ncols):
            value  = (s.cell(row,col).value)
            if col==0:
                value=int(value)
            if col==2:
                if value=='TDNB' or value=='DNB' or value=='':# replacing unnecessary details by 0
                    value=0
                try:
                    value=int(value)
                except ValueError:
                    value=value[:-1]
                try:
                    value=int(value)
                except ValueError: #throws exception if value out of bound
                    value=0
            if col == 3:
                value = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(value) - 2)#converting the date into standard format
                value=value.year#extracting year
            col_value.append(value)
        values.append(col_value)
d={}
for i in values:
    if i[1] not in d:
        d[i[1]]=[0]*50
    d[i[1]][i[3]-1970]+=i[2]
# print(d)
res=[]
res.append(['NAME','COUNTRY']+['Year'+str(i) for i in range(1970,2020)])#mapping the players runs in accordance to the cummalative year wise runs
for i in d:
    value=i
    k=list(d[i])
    value=list(value.split('('))
    value[1]=value[1][:-1]
    value[0]=value[0][:-1]
    k=value+k
    res.append(k)

cum_res = copy(res)

for i in range(1,len(cum_res)):
    s=0
    for j in range(3,51):
        s+=int(cum_res[i][j])
        cum_res[i][j]=s

pd.DataFrame(res).to_excel('output.xlsx', header=False, index=False)#conversion of data frame into an xlsv format

pd.DataFrame(cum_res).to_excel('cum_output.xlsx', header=False, index=False)#conversion of cummalative data frame into an xlsv format
