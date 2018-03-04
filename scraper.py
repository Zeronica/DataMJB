import requests
import bs4 as bs
import pandas as pd
import numpy as np

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'From': 'data-x@gmail.com'
}
def populate_row(row_index, data):
    link = data['link'][row_index]
    source = requests.get(link, headers=headers).content
    soup = bs.BeautifulSoup(source, 'html.parser')
    parms = soup.find(class_="basic-parms-mod")
    results = [i.contents[0] for i in parms.find_all("dd")]
    data.loc[row_index, 'Property type'] = results[0]
    data.loc[row_index, 'Property costs'] = results[1]
    data.loc[row_index, 'Total area'] = results[2]
    data.loc[row_index, 'Number of units'] = results[3]
    data.loc[row_index, 'Year built'] = results[4]
    data.loc[row_index, 'Parking spots'] = results[5]
    data.loc[row_index, 'Volume rate'] = results[6]
    data.loc[row_index, 'Green rating'] = results[7]
    data.loc[row_index, 'Developer Company'] = results[8]
    data.loc[row_index, 'Property management company'] =results[9]

def populate_batch_row(start = 0, batch_size = 1000):
    data = pd.read_csv('data_populated_all.csv')

    end = start + batch_size

    for i in range(start, end):
        try:
            populate_row(i, data)
        except requests.ConnectionError:
            continue
        if i % 100 == 0:
            print("done with row ", i)

    data.to_csv('data_populated_all.csv')
    print("written to file")

data = pd.read_csv('data_populated_all.csv')

for i in range(4000, len(data), 1000):
    populate_batch_row(i, 1000)
