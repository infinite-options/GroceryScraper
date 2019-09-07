from flask import Flask, render_template
import requests

app = Flask(__name__)

# URL
wholefoods_url = 'https://products.wholefoodsmarket.com/api/search?sort=relevance&store=10259&skip=0&filters=%5B%7B%22ns%22%3A%22subcategory%22%2C%22key%22%3A%22fresh-fruit%22%2C%22value%22%3A%22produce.fresh-fruit%22%7D%5D'

# Request URL and parse JSON
response = requests.get(wholefoods_url)
response.raise_for_status() # Raise exception if response invalid
item = response.json()['list'][0]['name']
price = response.json()['list'][0]['store']['price']

# Home page routing
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', item=item, price=price)

# Enable debugging when running
if __name__ == '__main__':
    app.run(debug=True)
