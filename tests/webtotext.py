import requests
import html2text

url = 'https://shop.safeway.com/aisles/fruits-vegetables/fresh-vegetables-herbs.2708.html?page=1&sort=salesRank'
data = requests.get(url)

#with open('filetext.txt', 'wb') as out_f:
#    out_f.write(data.text.encode('utf-8'))

pagedata = data.text.encode('utf-8')
rendered_content = html2text.html2text(pagedata)

f = open('filetext.txt', 'wb')
f.write(rendered_content)
f.close()
