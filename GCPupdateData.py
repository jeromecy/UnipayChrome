from DB import DB
import country
import datetime
import socket
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

socket.setdefaulttimeout(30)

today = datetime.date.today()
ISOFORMAT='%Y-%m-%d'

headers = { 'Host': 'www.unionpayintl.com',
           'Proxy-Connection': 'keep-alive',
           'Content-Length': '59',
           'Accept': '*/*',
           'Origin': 'http://www.unionpayintl.com',
           'X-Requested-With': 'XMLHttpRequest',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://www.unionpayintl.com/upiweb-card/serviceCenter/rate?language=cn',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'
        }

url     = 'http://www.unionpayintl.com/cardholderServ/serviceCenter/rate/search'
base    = "CNY"
tran    = "AUD"


# baseCurrency = country.base
# transactionCurrency = country.trans

session = requests.Session()
db      = DB()


deltadays = datetime.timedelta(days=2190)
date      = today-deltadays
j         = 0

while(date < today):
    if(date.weekday()<5):
        pop = session.post(url, headers = headers , data = {
                'curDate': str(date),
                'baseCurrency': base,
                'transactionCurrency': tran
                })
    #try:
    #    pop.json()
    #except ValueError:
    #    print('Decoding JSON has failed')		
    sql = "insert into `datarate`(`date`,`base`,`trans`,`rate`) values ('%s','%s','%s',%f)" % (str(date),base,tran,pop.json()['exchangeRate'])
    db.query(sql)
    db.commit()
    j += 1
    date  = date + datetime.timedelta(days=1)

print('done')








while k<len(baseCurrency):
    base=baseCurrency[k]
    i=0
    while i<len(transactionCurrency):
        tran=transactionCurrency[i]
        data= {'baseCurrency': base, 'transactionCurrency':transactionCurrency[i], 'curDate':date,'go':'BIZTOOL_MERCHANT_PG_exchangeRateEn'}
        if base==tran:
            price=1.000
            print "the rate on",date,"is 1 ",base," = 1",tran
        else:             
            request = urllib2.Request(url=url,data=urllib.urlencode(data),headers=headers)                
            try:
                response = urllib2.urlopen(request,timeout=30).read()
                regex = '                \t\t'+'(.+?)&nbsp;'+base
                pattern = re.compile(regex)
                price_temp = re.findall(pattern,response)[0]
                price=float(price_temp)
                #print "the rate on",date,"is 1 ",base," = ",price,tran
            except urllib2.URLError as e:
                price=0.000
                print type(e)
            except socket.timeout as e:
                price=0.000
                print type(e)
            except httplib.IncompleteRead as e:
                price=0.000
                print type(e)

#sql = "insert into unionpay(date,base,transact,currency) values ('%s','%s','%s',%s)" % (date,base,tran,price)
        sql = "insert into `unionpay`(`date`,`base`,`transact`,`currency`) values ('%s','%s','%s',%f)" % (date,base,tran,price)

        try:  
            db.query(sql)
            db.commit()
        except Exception, e:  
            print e  
        
                    
        i+=1     
    k+=1
