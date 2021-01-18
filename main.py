#!/bin/python3

import selenium.webdriver as driver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import sys
import code
import time

from scraper_modules import *

#variables


#format
if(len(sys.argv) < 2):
	print('main.py [BOM CSV file] [Row name with part numbers]')
	exit(-1)

class DigiKey_Scrapper:
	#constants
	DIGIKEY_LINK = "https://www.digikey.com/"

	def __init__(self, csv_file, digikey_part_number_column='Digi-Key_PN'):
		#getting all the part numbers etc from CSV file
		self.data = pd.read_csv(csv_file)
		self.number_rows = len(self.data)
		self.current_row = 0
		self.digikey_part_number_column = digikey_part_number_column
		#opening firefox and browsing to digikey website (also clicking the cookies button)
		self.firefox_window = driver.Firefox()
		self.firefox_window.maximize_window()
		self.firefox_window.get(self.DIGIKEY_LINK)
		self.firefox_window.find_element_by_class_name('button-desktop').click() #clicking the cookies accept button
	
	def browse_to_next_part(self):
		#meaning this is the first run
		if(self.current_row == 0):
			searchbox = self.firefox_window.find_elements_by_class_name('search-textbox')[1]
		#not the first run
		else:
			searchbox = self.firefox_window.find_elements_by_class_name('search-textbox')[0]
		time.sleep(0.1)
		searchbox.click()
		time.sleep(0.1)
		#entering the part number and pressing enter
		searchbox.send_keys(self.data[self.digikey_part_number_column][self.current_row])
		searchbox.send_keys(Keys.RETURN)
		#incrementing current_row
		self.current_row += 1
		return (self.current_row - 1) #returning current
			


def main():
	dks = DigiKey_Scrapper(sys.argv[1])
	while(dks.current_row < dks.number_rows):
		dks.browse_to_next_part()
		time.sleep(3)
		



# searchbox = firefox_window.find_elements_by_class_name('product-search-text')
# searchbox[1].click()
# try:
# 	searchbox[1].send_keys(data_sanitized[DK_PART_ROW][0])
# except:
# 	pass
# searchbox[1].send_keys(Keys.RETURN)
# file_name = '0_' + data_sanitized[VALUE_ROW][0].replace('-', '').replace('.', '') + '_' + data_sanitized[DK_PART_ROW][0].replace('-', '').replace('.', '') + '.png'
# time.sleep(2)
# firefox_window.save_screenshot(file_name)
# price_table = []
# time.sleep(2)
# # if(len(price_table) <= 0):
# dk_part_row.append(data[DK_PART_ROW][0])
# value_row.append(data[VALUE_ROW][0])
# while(True):
# 	try:
# 		price_table = firefox_window.find_elements_by_class_name('MuiGrid-grid-md-4')[0].find_elements_by_class_name('MuiTable-root')[0].find_elements_by_tag_name('tr')
# 		single_price = price_table[2].text
# 		multi_price = price_table[len(price_table) - 1].text
# 		break
# 	except:
# 		time.sleep(1)
# 		continue
# print('Single Price :' + str(single_price))
# print('Multi Price :' + str(multi_price))
# price_single_row.append(single_price)
# price_multi_row.append(multi_price)
# searchbox = firefox_window.find_elements_by_class_name('product-search-text')
# try:
# 	searchbox[0].click()
# except:
# 	pass

# for i in range(1, len(data_sanitized)):

# 	try:
# 		data_sanitized[VALUE_ROW][i]
# 	except:
# 		continue
# 	time.sleep(2)
# 	searchbox = firefox_window.find_elements_by_class_name('product-search-text')
# 	searchbox[0].click()
# 	try:
# 		searchbox[0].send_keys(data_sanitized[DK_PART_ROW][i])
# 	except:
# 		pass
# 	try:
# 		searchbox[0].send_keys(Keys.RETURN)
# 	except:
# 		pass

# 	dk_part_row.append(data[DK_PART_ROW][i])
# 	value_row.append(data[VALUE_ROW][i])

# 	#santizing file name
# 	file_name = str(i) + '_' + data_sanitized[VALUE_ROW][i].replace('-', '').replace('.', '') + '_' + data_sanitized[DK_PART_ROW][i].replace('-', '').replace('.', '') + '.png'
# 	time.sleep(4)
# 	while(True):
# 		try:
# 			price_table = firefox_window.find_elements_by_class_name('MuiGrid-grid-md-4')[0].find_elements_by_class_name('MuiTable-root')[0].find_elements_by_tag_name('tr')
# 			single_price = price_table[2].text
# 			multi_price = price_table[len(price_table) - 1].text
# 			print('Single Price :' + str(single_price))
# 			print('Multi Price :' + str(multi_price))
# 			price_single_row.append(single_price)
# 			price_multi_row.append(multi_price)
# 			break
# 		except:
# 			time.sleep(1)
# 			continue
# 	firefox_window.save_screenshot(file_name)
# 	searchbox = firefox_window.find_elements_by_class_name('product-search-text')
# 	searchbox[0].click()

# # price_single_row_final = []
# # price_multi_row_final = []

# # print('Now entering interactive console')
# # code.interact(local=locals())

# # for i in range(0, len(price_single_row)):
# # 	tmp = price_single_row[i]
# # 	tmp.replace('$', '').replace(',','').split()
# # 	print(tmp)
# # 	tmp = float(tmp[1]) / float(tmp[0])
# # 	price_single_row_final.append(tmp)

# # 	tmp = price_multi_row[i]
# # 	tmp.replace('$', '').replace(',','').split()
# # 	print(tmp)
# # 	tmp = float(tmp[1]) / float(tmp[0])
# # 	price_multi_row_final.append(tmp)

# df = pd.DataFrame({
# DK_PART_ROW : dk_part_row,
# VALUE_ROW : value_row,
# "PriceSingle" : price_single_row,
# "PriceMulti" : price_multi_row
# })

# df.to_csv('output.csv')

if(__name__ == "__main__"):
	main()