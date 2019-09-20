from selenium import webdriver

url = 'https://shop.safeway.com/aisles/fruits-vegetables/fresh-vegetables-herbs.2708.html?page=1&sort=salesRank'
driver = webdriver.PhantomJS()
driver.get(url)
p_element = driver.find_element_by_id
