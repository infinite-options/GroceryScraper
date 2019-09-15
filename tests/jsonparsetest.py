import json

with open('api_urls.json', 'r') as f:
    api_urls_dict = json.load(f)

for api_url in api_urls_dict:
    print(api_url['url'])
