import pandas
from datetime import datetime, date, timedelta
from updateCrypto import updateCryptoData
import regex as re

updateCryptoData()
print('-------------- end update -----------------')

data = pandas.read_csv('allData.csv')

today = datetime.now()
date = today.strftime("%d/%m/%Y")
time = today.strftime("%H:%M:%S")

yesterday = today - timedelta(days=1)
yesterDate = yesterday.strftime("%d/%m/%Y")

tdf = data.loc[data['Date (d/m/y)'] == date]
ydf = data.loc[data['Date (d/m/y)'] == yesterDate]

# print(tdf)
# print(ydf)

# select where times are the same to whatever accuracy is possible
sameTimes = tdf.loc[tdf['Time'].astype(str) == time]
numsIncluded = 8
while sameTimes.empty and numsIncluded > 1:
    sameTimes = tdf.loc[tdf['Time'].astype(str).str[:numsIncluded:] == time[:numsIncluded:]]
    numsIncluded -=1
    
ysameTimes = ydf.loc[ydf['Time'].astype(str) == time]
numsIncluded = 8
while ysameTimes.empty and numsIncluded > 1:
    ysameTimes = ydf.loc[ydf['Time'].astype(str).str[:numsIncluded:] == time[:numsIncluded:]]
    numsIncluded -=1
    
print(sameTimes)
print(ysameTimes)









