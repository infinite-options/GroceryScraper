from flask import Flask, render_template
import requests

app = Flask(__name__)

# URL
wholefoods_url = 'https://products.wholefoodsmarket.com/api/search?sort=relevance&store=10259&skip=0&filters=%5B%7B%22ns%22%3A%22category%22%2C%22key%22%3A%22produce%22%2C%22value%22%3A%22produce%22%7D%2C%7B%22ns%22%3A%22subcategory%22%2C%22key%22%3A%22fresh-vegetables%22%2C%22value%22%3A%22produce.fresh-vegetables%22%7D%5D'
# raleys_url = 'https://shop.raleys.com/api/v2/store_products?_nocache=1567892729784&category_id=2&category_ids=2&limit=60&offset=0&sort=popular'
# target_url = 'https://redsky.target.com/v2/plp/collection/13562231,14919690,13728423,14919033,13533833,13459265,14917313,13519319,13533837,14919691,13479115,47778362,15028201,51467685,50846848,50759802,50879657,13219631,13561421,52062271,14917361,51803965,13474244,13519318?key=eb2551e4accc14f38cc42d32fbc2b2ea&pricing_store_id=2088&multichannel_option=basics&storeId=321'

# Request URL and parse JSON
response_wholefoods = requests.get(wholefoods_url)
response_wholefoods.raise_for_status() # Raise exception if response invalid
# response_raleys = requests.get(raleys_url)
# response_raleys.raise_for_status()

# Initialize items and prices lists
items = []
prices = []
stores = []

# Add items and prices
for i in range(20):
    items = items + (response_wholefoods.json()['list'][i]['name'])
    prices = prices + (response_wholefoods.json()['list'][i]['store']['price'])
    stores = stores + ('Whole Foods')
    # items_raleys = items_raleys + ((response_raleys.json()['list'][i]['name']),(response_raleys.json()['list'][i]['store']['price']))

# Home page routing
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', items=items, prices=prices, stores=stores)

# Enable debugging when running
if __name__ == '__main__':
    app.run(debug=True)
