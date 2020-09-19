import time
from selenium import webdriver
#from selenium.webdriver.common.by import By
import pandas as pd

url = 'https://shop.raleys.com/shop/categories/3'
# Optional argument, if not specified will search path.
# Install chromedriver.exe
driver = webdriver.Chrome(
    '## chromedriver path')
driver.get(url)
time.sleep(5)  # Let the user actually see something!
#search_box = driver.find_element_by_name('q')
# search_box.send_keys('ChromeDriver')
# search_box.submit()

lists = driver.find_elements_by_xpath("//li[@ng-switch = 'item.item_type']")
price_list = []
print(len(lists))
for item in lists:
    # print('------------------------------')
    # print(item.find_element_by_xpath('.//').get_attribute('innerHTML'))
    l1 = []
    title = item.find_element_by_xpath(
        ".//div[@class = 'cell-title-text ng-binding']").get_attribute('innerHTML')
    price = item.find_element_by_xpath(
        ".//div[@class = 'product-prices']/.//div[1]/.//div[2]/.//span[1][contains(text(),'$')]").get_attribute('innerHTML')
    l1.append(title)
    l1.append(price)
    price_list.append(l1)

print(price_list)
data = price_list
print(type(data))
df = pd.DataFrame(data, columns=["Product", "Price"])
print('-------------------------')
print(df)

html = df.to_html()

text_file = open("index.html", "w")
text_file.write(html)
text_file.close()

# for item in lists:
#    title = item.find_elements_by_xpath("//div[@class = 'cell-title-text ng-binding']")
#    price = item.find_elements_by_xpath("//div[@class = 'product-prices']//span[1]//span[contains(text(),'$')]")
#    for j in title:
#        print("title:- {}".format(j.get_attribute('innerHTML')))
#    for k in price:
#        print("price:- {}".format(k.get_attribute('innerHTML')))
#    print('-------Done-------')
#    break

#title = driver.find_elements_by_xpath("//div[@class = 'cell-title-text ng-binding']")
#price = driver.find_elements_by_xpath("//div[@class = 'product-prices']/.//div[1]/.//div[2]/.//span[1][contains(text(),'$')]")
# for j in title:
#    print("title:- {}".format(j.get_attribute('innerHTML')))
# for k in price:
#    print("price:- {}".format(k.get_attribute('innerHTML')))
# print(price_list)
# print(len(title),len(price))

time.sleep(5)  # Let the user actually see something!
driver.quit()
