import requests
import pandas as pd


NMBRS = '0123456789'
zapros = 'елочная игрушка стекло'
page_num = 1
params = {'q': zapros, 'submit': 'y', 'gender_section': 'women', 'page': page_num}
url = 'https://www.lamoda.ru/catalogsearch/result/'
response = requests.get(url, params=params)
r = response.text

a = r.find('pagination')
pages = int(r[a+30:a+31])

print(pages)

items0 = r[a+51:a+61]
items = ''
for letter in items0:
    if letter in NMBRS:
        items = items + letter
items = int(items)

print(items)

items_in_page = []
for p in range(pages):
    if items >= 60:
        items_in_page.append(60)
        items = items - 60
    else:
        items_in_page.append(items)


articles = []
brands = []
products = []
for j in range(pages):
    page_num = j + 1
    params = {'q': zapros, 'submit': 'y', 'gender_section': 'women', 'page': page_num}
    url = 'https://www.lamoda.ru/catalogsearch/result/'
    response = requests.get(url, params=params)
    r = response.text
    index = items_in_page[j]
    for i in range(index):
        a = r.find('href="/p/')
        articles.append(r[a+9:a+21])
        r = r[a+21:]

for j in range(pages):
    page_num = j + 1
    params = {'q': zapros, 'submit': 'y', 'gender_section': 'women', 'page': page_num}
    url = 'https://www.lamoda.ru/catalogsearch/result/'
    response = requests.get(url, params=params)
    r = response.text
    index = items_in_page[j]
    for i in range(index):
        a = r.find('__brand-name">')
        brand = ''

        for w in range (len(r[a+14:a+100])):
            if (r[a+14:a+100])[w] == '<':
                break
            else:
                brand = brand + (r[a+14:a+100])[w]

        brands.append(brand)

for j in range(pages):
    page_num = j + 1
    params = {'q': zapros, 'submit': 'y', 'gender_section': 'women', 'page': page_num}
    url = 'https://www.lamoda.ru/catalogsearch/result/'
    response = requests.get(url, params=params)
    r = response.text
    index = items_in_page[j]
    for i in range(index):
        a = r.find('__product-name">')
        product = ''

        for w in range(len(r[a+17:a+100])):
            if (r[a+17:a+100])[w] == '<':
                break
            else:
                product = product + (r[a+17:a+100])[w]

        products.append(product)

print(products)
print(brands)
print(articles)

countries = []
prices = []
discounts = []

for elem in articles:
    article = elem
    params = {'q': article, 'submit': 'y', 'gender_section': 'women'}
    url = 'https://www.lamoda.ru/catalogsearch/result/'
    response = requests.get(url, params=params)
    r1 = response.text

    a = r1.find('"production_country"')
    country = ''
    for w in range(len(r1[a+60:a+159])):
        if (r1[a+60:a+159])[w] == '"':
            break
        else:
            country = country + (r1[a+60:a+159])[w]

    countries.append(country)

    b = r1.find('"price":')
    price = ''
    for w in range(len(r1[b+8:b+100])):
        if (r1[b+8:b+100])[w] == ',':
            break
        else:
            price = price + (r1[b+8:b+100])[w]

    prices.append(price)

    c = r1.find('"percent":')
    if c != -1:
        discount = ''
        for w in range(len(r1[c+10:c+100])):
            if (r1[c+10:c+100])[w] == ',':
                break
            else:
                discount = discount + (r1[c+10:c+100])[w]
    else:
        discount = '0'

    discounts.append(discount)

print(countries)
print(prices)
print(discounts)


df = pd.DataFrame({'Articles': articles, 'Brand': brands, 'Price': prices, 'Discount': discounts, 'Country': countries})

sdf = df.sort_values(by=['Price'], ascending=False)
print(sdf)

with open('Statistics.txt', 'w') as stat:
    print(sdf, file=stat)
