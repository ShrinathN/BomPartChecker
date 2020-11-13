#!/bin/python3

import selenium.webdriver as driver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import sys
import code
import time

#format
# main.py [BOM CSV file] [Row name with part numbers]

#constants
DIGIKEY_LINK = "https://www.digikey.com/"
DK_PART_ROW = 'DK Part'
VALUE_ROW = 'Value'

#start
firefox_window = driver.Firefox()
firefox_window.maximize_window()
firefox_window.get("https://www.digikey.com/")

data = pd.read_csv(sys.argv[1])
data_sanitized = data[[DK_PART_ROW, VALUE_ROW]]
data_sanitized = data_sanitized.dropna()

searchbox = firefox_window.find_elements_by_class_name('product-search-text')
searchbox[1].click()
try:
	searchbox[1].send_keys(data_sanitized[DK_PART_ROW][0])
except:
	pass
searchbox[1].send_keys(Keys.RETURN)
file_name = '0_' + data_sanitized[VALUE_ROW][0].replace('-', '').replace('.', '') + '_' + data_sanitized[DK_PART_ROW][0].replace('-', '').replace('.', '') + '.png'
time.sleep(2)
firefox_window.save_screenshot(file_name)
searchbox = firefox_window.find_elements_by_class_name('product-search-text')
try:
	searchbox[0].click()
except:
	pass

for i in range(1, len(data_sanitized)):
	try:
		data_sanitized[VALUE_ROW][i]
	except:
		continue

	searchbox = firefox_window.find_elements_by_class_name('product-search-text')
	searchbox[0].click()
	try:
		searchbox[0].send_keys(data_sanitized[DK_PART_ROW][i])
	except:
		pass
	try:
		searchbox[0].send_keys(Keys.RETURN)
	except:
		pass


	#santizing file name
	file_name = str(i) + '_' + data_sanitized[VALUE_ROW][i].replace('-', '').replace('.', '') + '_' + data_sanitized[DK_PART_ROW][i].replace('-', '').replace('.', '') + '.png'
	time.sleep(4)
	firefox_window.save_screenshot(file_name)
	searchbox = firefox_window.find_elements_by_class_name('product-search-text')
	searchbox[0].click()