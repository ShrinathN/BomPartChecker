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
DK_PART_ROW = 'Digi-Key_PN'
VALUE_ROW = 'Value'

dk_part_row = []
value_row = []
price_single_row = []
price_multi_row = []

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
price_table = []
time.sleep(2)
# if(len(price_table) <= 0):
dk_part_row.append(data[DK_PART_ROW][0])
value_row.append(data[VALUE_ROW][0])
while(True):
	try:
		price_table = firefox_window.find_elements_by_class_name('MuiGrid-grid-md-4')[0].find_elements_by_class_name('MuiTable-root')[0].find_elements_by_tag_name('tr')
		single_price = price_table[2].text
		multi_price = price_table[len(price_table) - 1].text
		break
	except:
		time.sleep(1)
		continue
print('Single Price :' + str(single_price))
print('Multi Price :' + str(multi_price))
price_single_row.append(single_price)
price_multi_row.append(multi_price)
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
	time.sleep(2)
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

	dk_part_row.append(data[DK_PART_ROW][i])
	value_row.append(data[VALUE_ROW][i])

	#santizing file name
	file_name = str(i) + '_' + data_sanitized[VALUE_ROW][i].replace('-', '').replace('.', '') + '_' + data_sanitized[DK_PART_ROW][i].replace('-', '').replace('.', '') + '.png'
	time.sleep(4)
	while(True):
		try:
			price_table = firefox_window.find_elements_by_class_name('MuiGrid-grid-md-4')[0].find_elements_by_class_name('MuiTable-root')[0].find_elements_by_tag_name('tr')
			single_price = price_table[2].text
			multi_price = price_table[len(price_table) - 1].text
			print('Single Price :' + str(single_price))
			print('Multi Price :' + str(multi_price))
			price_single_row.append(single_price)
			price_multi_row.append(multi_price)
			break
		except:
			time.sleep(1)
			continue
	firefox_window.save_screenshot(file_name)
	searchbox = firefox_window.find_elements_by_class_name('product-search-text')
	searchbox[0].click()

# price_single_row_final = []
# price_multi_row_final = []

# print('Now entering interactive console')
# code.interact(local=locals())

# for i in range(0, len(price_single_row)):
# 	tmp = price_single_row[i]
# 	tmp.replace('$', '').replace(',','').split()
# 	print(tmp)
# 	tmp = float(tmp[1]) / float(tmp[0])
# 	price_single_row_final.append(tmp)

# 	tmp = price_multi_row[i]
# 	tmp.replace('$', '').replace(',','').split()
# 	print(tmp)
# 	tmp = float(tmp[1]) / float(tmp[0])
# 	price_multi_row_final.append(tmp)

df = pd.DataFrame({
DK_PART_ROW : dk_part_row,
VALUE_ROW : value_row,
"PriceSingle" : price_single_row,
"PriceMulti" : price_multi_row
})

df.to_csv('output.csv')