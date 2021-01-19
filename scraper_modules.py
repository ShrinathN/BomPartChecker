#!/bin/python3

import time
import code

'''
This is a part of DigiKey scraper system
Every function is an independent unit that can rip off a particular piece of information from a product page
'''

class DigiKey_Scrapper:

	def __init__(self, 
	scrap_manufacturer_part_number=False,
	scrap_description=False,
	scrap_manufacturer=False,
	):
		self._scrap_manufacturer_part_number = scrap_manufacturer_part_number
		self._scrap_description = scrap_description,
		self._scrap_manufacturer = scrap_manufacturer

		#initializing arrays for various modules
		if(self._scrap_manufacturer_part_number):
			self.scrap_manufacturer_part_number_array = []
		if(self._scrap_description):
			self.scrap_description_array = []
		if(self._scrap_manufacturer):
			self.scrap_manufacturer_array = []		


	#ADD NEW SCRAPPER MODULES IN THIS FUNCTION
	def scrape_for_page(self):
		self._wait_until_load()
		if(self._scrap_manufacturer_part_number):
			self._get_manufacturer_part_number()
			print('Scrapped manufacturer part number')
		
		if(self._scrap_manufacturer):
			self._get_manufacturer()
			print('Scrapped manufacturer')
		
		if(self._scrap_description):
			self._get_description()
			print('Scrapped Description')

	def set_driver(self, driver):
		self.driver = driver
	
	def set_data(self, data):
		self.data = data

	def save_as_csv(self, file_name):
		try:
			if(self._scrap_manufacturer_part_number):
				self.data['manufacturer_part_number'] = self.scrap_manufacturer_part_number_array

			if(self._scrap_description):
				self.data['description'] = self.scrap_description_array

			if(self._scrap_manufacturer):
				self.data['manufacturer'] = self.scrap_manufacturer_array

			self.data.to_csv(file_name)
		except:
			code.interact(local=locals())
	
	def _wait_until_load(self):
		loaded = ''
		while(loaded != 'complete'):
			loaded = self.driver.execute_script('return document.readyState')
			time.sleep(0.5)

	#===================================================
	#ALL THE DIFFERENT SCRAPER MODULES DOWN BELOW!!!!!
	#===================================================

	#this will get the manufacturer part number
	def _get_manufacturer_part_number(self):
		#Manufacturer Product Number
		# all_divs = []
		# while(len(all_divs) == 0):
		# 	time.sleep(0.3)
		all_divs = self.driver.find_elements_by_tag_name('div')
		for i in range(len(all_divs)):
			if(all_divs[i].text == 'Manufacturer Product Number'):
				self.scrap_manufacturer_part_number_array.append(all_divs[i + 1].text)
				break

	#this will get the digikey page description
	def _get_description(self):
		#Description
		# all_divs = []
		# while(len(all_divs) == 0):
		# 	time.sleep(0.3)
		all_divs = self.driver.find_elements_by_tag_name('div')
		for i in range(len(all_divs)):
			if(all_divs[i].text == 'Description'):
				self.scrap_description_array.append(all_divs[i + 1].text)
				break

	def _get_manufacturer(self):
		#Manufacturer
		# all_divs = []
		# while(len(all_divs) == 0):
		# 	time.sleep(0.3)
		all_divs = self.driver.find_elements_by_tag_name('div')
		for i in range(len(all_divs)):
			if(all_divs[i].text == 'Manufacturer'):
				self.scrap_manufacturer_array.append(all_divs[i + 1].text)
				break
