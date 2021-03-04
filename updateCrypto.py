from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas
from datetime import date, datetime


today = datetime.now()
date = today.strftime("%d/%m/%Y")
time = today.strftime("%H:%M:%S")
print(date, time)

df = pandas.read_csv('crypto-log.csv')
df = df.dropna(how='all')

bp = df.groupby(['Coin'])['buy price'].sum()

ppc = {}
for key in df.Coin.unique():
    if key == key:
        pdf = df.loc[df['Coin'] == key]
        ppc[key] = (pdf['buy price'] * pdf['price per coin']).sum()/pdf['buy price'].sum()

cc = df.groupby(['Coin'])['How much'].sum()


oldCoinValue = {}

for coin in bp.keys():
    # filter out nan
    if coin == coin:
        oldCoinValue[coin] = abs(bp[coin]) 
        
allCoins = ''.join([k +',' for k in bp.keys()])
allCoins = allCoins[:-1:]

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
    'symbol':allCoins,
    'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': open('cmc_key.txt').read(),
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    newCoinValues = {}
        
    coinChange = {}

    for coin in bp.keys():
        newCoinValues[coin] = data['data'][coin]['quote']['USD']['price'] * cc[coin]
        coinChange[coin] = ((newCoinValues[coin] - oldCoinValue[coin]) / oldCoinValue[coin]) * 100
    
    ndf = pandas.DataFrame(columns=['Date (d/m/y)', 'Time', 'Coin', 'Quantity', 'Old value', 'New value', 'Avg ppc', 'Curr ppc', 'Value change ($)', 'Value change (%)'])
    
    for i, coin in enumerate(coinChange.keys()):
        ndf.loc[i] = [date, time, coin, cc[coin], oldCoinValue[coin], newCoinValues[coin], ppc[coin],  data['data'][coin]['quote']['USD']['price'], newCoinValues[coin] - oldCoinValue[coin], coinChange[coin]]
    print(ndf)
    
    toPrint = ''
    try:
        odf = pandas.read_csv('allData.csv')
        toPrint = pandas.concat([odf, ndf])
    except:
        toPrint = ndf
    toPrint.to_csv('allData.csv', columns=['Date (d/m/y)', 'Time', 'Coin', 'Quantity', 'Old value', 'New value', 'Avg ppc', 'Curr ppc'], index=False)
    
    totalChange = (sum(newCoinValues.values()) - sum(oldCoinValue.values()))/sum(oldCoinValue.values()) * 100
    if totalChange >=0:
        print('\nTotal:\t$' + str(sum(newCoinValues.values()) - sum(oldCoinValue.values())) + '\t+' + str(totalChange) + ' %')
    else:
        print('\nTotal:\t$' + str(sum(newCoinValues.values()) - sum(oldCoinValue.values())) + '\t' + str(totalChange) + ' %')
    
    print('Actual change: ' + str(sum(oldCoinValue.values())) + ' -> ' + str(sum(newCoinValues.values())))
    

    
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
  

