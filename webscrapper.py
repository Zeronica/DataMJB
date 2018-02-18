import requests
import bs4 as bs
import pandas as pd
import re
headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'From': 'data-x@gmail.com' }
d=pd.DataFrame()
district=['pudong','minhang','baoshan','xuhui','songjiang','jiading'
         ,'jingan','putuo','yangpu','hongkou','changning','huangpu',
         'qingpu','fengxian','jinshan','chongming','shanghaizhoubian']
for o in district:
    p=1
    while p<=100:
        try:
            source = requests.get('https://shanghai.anjuke.com/community/'+o+'/p{}'.format(p), headers=headers).content
            soup = bs.BeautifulSoup(source,'html.parser')
            name=list()
            web=list()
            long=list()
            la=list()
            for i in soup.find_all(class_="li-itemmod"):
                name.append(i.find('img').get('alt'))
                web.append(i.find('a').get('href'))
                for j in i.find_all('a'):
                    if 'l1' in j.get('href'):
                        kk=j.get('href')
                long.append(re.findall(r'l1=(\S*?)&',kk)[0])
                la.append(re.findall(r'l2=(\S*?)&',kk)[0])
            dd=pd.DataFrame(name)

            dd['link']=web
            dd['long']=long
            dd['la']=la
            d = d.append(dd,ignore_index=True)
            p=p+1
            print('Page{} '.format(p-1)+'in ',o, ' is already done')
        except:
            q=False
            print('error')
