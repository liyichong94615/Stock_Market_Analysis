import plotly.offline as py
import plotly.io as pio
import plotly.graph_objs as go

import re, time,csv,datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplfinance as mpf
import matplotlib.dates as mpd
import urllib.request
from lxml import etree



t = time.localtime() 
year = range(t[0],2019,-1) 
season = range(4,0,-1) 


def getData(url):
    
    f = urllib.request.urlopen(url)
    content = f.read().decode('utf8')

    html = etree.HTML(content)
    tr_nodes = html.xpath('//table[@class="table_bg001 border_box limit_sale"]/tr')
  
    ## 'th' is inside first 'tr'
    header = [i[0].text for i in tr_nodes[0].xpath("th")]
    ## Get text from rest all 'tr'
    td_content = [[td.text for td in tr.xpath('td')] for tr in tr_nodes[1:]]
    return td_content


def get_stock_price(code):
    url1 = "http://quotes.money.163.com/trade/lsjysj_"
    url2 = ".html?year="
    url3 = "&season="
    urllist = []
    
    for k in year:
        for v in season:
            urllist.append(url1+str(code)+url2+str(k)+url3+str(v))
           

    price = []
    for url in urllist:
        price.extend(getData(url))
        print(url)
        
    return price


price = get_stock_price('000002')
header = ['0Date', '1Opening price', '2Highest price', '3Lowest price', '4Closing price', '5Ups and downs', '6Quote', '7Volume', '8Transaction amount', '9Amplitude', '10Turnover rate']


pio.renderers.default = "iframe"


date = [row[0] for row in price]
Open = [row[1] for row in price]
High = [row[2] for row in price]
Low = [row[3] for row in price]
Close = [row[4] for row in price]


trace = go.Candlestick(
    x=date,
    open=Open,
    high=High,
    low=Low,
    close=Close,
    increasing=dict(line=dict(color='#2ebd84')),
    decreasing=dict(line=dict(color='#e0294a')))



data = [trace]

market = "Stock"

layout = go.Layout(
        title='Stock Market Data Analysis - ' + market,
        yaxis=dict(
            title='Stock market price',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        xaxis=dict(
            title='Date',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )

figure = {'data': data, 'layout': layout}

py.plot(figure, filename='stock.html')



