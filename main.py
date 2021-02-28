#!/bin/python3

import selenium.webdriver as driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
import sys
import code
import time
import threading

from scraper_modules import *

#variables
TIME_DELAY_INTERNET_SPEED = 3 #this is the scraping delay in seconds, adjust according to your internet speed

#format
if(len(sys.argv) < 2):
	print('main.py [BOM CSV file]')
	exit(-1)

class DigiKey_Scrapper_Driver:
	#constants
	DIGIKEY_LINK = "https://www.digikey.com/"

	def __init__(self, csv_file, digikey_part_number_column='Digi-Key_PN', value_column='Value'):
		#getting all the part numbers etc from CSV file
		self.data = pd.read_csv(csv_file)
		self.number_rows = len(self.data)
		self.current_row = 0
		self.value_column = value_column
		self.digikey_part_number_column = digikey_part_number_column

		self.first_run = True
		#opening firefox and browsing to digikey website (also clicking the cookies button)
		self.firefox_window = driver.Firefox()
		self.firefox_window.maximize_window()
		self.firefox_window.get(self.DIGIKEY_LINK)
		self.firefox_window.find_element_by_class_name('button-desktop').click() #clicking the cookies accept button

	def _wait_until_load(self):
		loaded = ''
		while(loaded != 'complete'):
			loaded = self.firefox_window.execute_script('return document.readyState')
			time.sleep(0.5)
		time.sleep(0.5)

	def get_current_part_value(self):
		return self.data['Value'][self.current_row - 1]
	
	def browse_to_next_part(self):
		#meaning this is the first run
		if(self.first_run):
			searchbox = self.firefox_window.find_elements_by_class_name('search-textbox')[1]
			self.first_run = False
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
		#ANNOYING DELAY!!!! PLEASE ADJUST
		# time.sleep(5)
		self._wait_until_load()
		return (self.current_row - 1) #returning current

	def get_driver(self):
		return self.firefox_window

	def get_data(self):
		return self.data

	def save_screenshot(self, filename):
		f = open(filename, 'wb')
		f.write(self.firefox_window.get_screenshot_as_png())
		f.close()


def main():
	dks = DigiKey_Scrapper_Driver(sys.argv[1])
	# dks.get_driver().implicitly_wait(5)

	scrapper_object = DigiKey_Scrapper(True, True, True, True, True)
	scrapper_object.set_data(dks.get_data())

	# threading.Thread(target=show_stat, args=(dks.get_driver(),)).start()

	while(dks.current_row < dks.number_rows):
		dks.browse_to_next_part()
		scrapper_object.set_driver(dks.get_driver())
		time.sleep(TIME_DELAY_INTERNET_SPEED)
		scrapper_object.scrape_for_page()
		if(os.listdir().count('images') == 0):
			os.mkdir('images')
		dks.save_screenshot('images/' + 'p' + str(dks.current_row - 1) + '_' + dks.get_current_part_value() + '.png')

	scrapper_object.save_as_csv('output.csv')



if(__name__ == "__main__"):
	main()