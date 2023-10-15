"""
Team
Nizovtseva Anastasia
Privalova Viktoria
"""


import requests
import pandas as pd


request = input('Enter your request: ')

NMBRS = '0123456789'
page_num = 1
params = {'q': request, 'submit': 'y', 'gender_section': 'women', 'page': page_num}
url = 'https://www.lamoda.ru/catalogsearch/result/'

response = requests.get(url, params=params)
r = response.text

pgs = r.find('pagination')
pages = int(r[pgs+30:pgs+31])

items0 = r[pgs+51:pgs+61]
items = ''

for letter in items0:
    if letter in NMBRS:
        items = items + letter
items = int(items)


items_in_page = []
for page in range(pages):
    if items >= 60:
        items_in_page.append(60)
        items = items - 60
    else:
        items_in_page.append(items)


articles = []
brands = []
products = []

for page in range(pages):
    page_num = page + 1
    params = {'q': request, 'submit': 'y', 'gender_section': 'women', 'page': page_num}
    url = 'https://www.lamoda.ru/catalogsearch/result/'
    response = requests.get(url, params=params)

    r = response.text
    index = items_in_page[page]

    for nums in range(index):
        art_finder = r.find('href="/p/')
        articles.append(r[art_finder+9:art_finder+21])
        r = r[art_finder+21:]

for page in range(pages):
    page_num = page + 1
    params = {'q': request, 'submit': 'y', 'gender_section': 'women', 'page': page_num}
    url = 'https://www.lamoda.ru/catalogsearch/result/'
    response = requests.get(url, params=params)

    r = response.text
    index = items_in_page[page]

    for nums in range(index):
        brand_finder = r.find('__brand-name">')
        brand = ''

        for index_1 in range(len(r[brand_finder+14:brand_finder+100])):
            if (r[brand_finder+14:brand_finder+100])[index_1] == '<':
                break
            else:
                brand = brand + (r[brand_finder+14:brand_finder+100])[index_1]

        brands.append(brand)

for page in range(pages):
    page_num = page + 1
    params = {'q': request, 'submit': 'y', 'gender_section': 'women', 'page': page_num}
    url = 'https://www.lamoda.ru/catalogsearch/result/'
    response = requests.get(url, params=params)

    r = response.text
    index = items_in_page[page]

    for nums in range(index):
        prdct_finder = r.find('__product-name">')
        product = ''

        for index_2 in range(len(r[prdct_finder+17:prdct_finder+100])):
            if (r[prdct_finder+17:prdct_finder+100])[index_2] == '<':
                break
            else:
                product = product + (r[prdct_finder+17:prdct_finder+100])[index_2]

        products.append(product)


countries = []
prices = []
discounts = []

for elem in articles:
    article = elem
    params = {'q': article, 'submit': 'y', 'gender_section': 'women'}
    url = 'https://www.lamoda.ru/catalogsearch/result/'

    response = requests.get(url, params=params)
    r1 = response.text

    cntr_finder = r1.find('"production_country"')
    country = ''
    for index_3 in range(len(r1[cntr_finder+60:cntr_finder+159])):
        if (r1[cntr_finder+60:cntr_finder+159])[index_3] == '"':
            break
        else:
            country = country + (r1[cntr_finder+60:cntr_finder+159])[index_3]

    countries.append(country)

    prc_finder = r1.find('"price":')
    price = ''
    for index_4 in range(len(r1[prc_finder+8:prc_finder+100])):
        if (r1[prc_finder+8:prc_finder+100])[index_4] == ',':
            break
        else:
            price = price + (r1[prc_finder+8:prc_finder+100])[index_4]

    prices.append(price)

    per_finder = r1.find('"percent":')
    if per_finder != -1:
        discount = ''
        for index_5 in range(len(r1[per_finder+10:per_finder+100])):
            if (r1[per_finder+10:per_finder+100])[index_5] == ',':
                break
            else:
                discount = discount + (r1[per_finder+10:per_finder+100])[index_5]
    else:
        discount = '0'

    discounts.append(discount)


df = pd.DataFrame({'Articles': articles, 'Products': products, 'Brand': brands, 'Price': prices,
                   'Discount': discounts, 'Country': countries})
pd.set_option('display.max_columns', 7)
pd.set_option('display.max_rows', len(articles))

sdf = df.sort_values(by=['Price'])

with open('Statistics.txt', 'w') as stat:
    stat.write(str(sdf))
