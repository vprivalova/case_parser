import requests


url = ''
r = requests.get(url)
text = r.text
print(text)
