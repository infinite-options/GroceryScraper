import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url = 'https://shop.safeway.com/bin/safeway/product/aemaisle?aisleId=1_23_2&storeId=1483'
response = requests.get(url)

if response is not None:
    soup = BeautifulSoup(response, "html.parser")
    for item in soup.select('$'):
        print
