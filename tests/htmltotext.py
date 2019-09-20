from urllib.request import urlopen
import html2text
#url = 'https://shop.safeway.com/aisles/fruits-vegetables/fresh-vegetables-herbs.2708.html?page=1&sort=salesRank'
url = 'https://shop.raleys.com/shop/categories/19'
page = urlopen(url)
html_content = page.read().decode('utf-8')
rendered_content = html2text.html2text(html_content)
file = open('filetext.txt', 'w')
file.write(rendered_content)
file.close()
