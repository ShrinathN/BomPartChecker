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
	scrap_datasheet=False,
	scrap_digikey_page=False
	):
		self._scrap_manufacturer_part_number = scrap_manufacturer_part_number
		self._scrap_description = scrap_description,
		self._scrap_manufacturer = scrap_manufacturer
		self._scrap_datasheet = scrap_datasheet
		self._scrap_digikey_page = scrap_digikey_page

		self._number_fields_to_scrap = 0
		#initializing arrays for various modules
		if(self._scrap_manufacturer_part_number):
			self.scrap_manufacturer_part_number_array = []
			self._number_fields_to_scrap += 1
		if(self._scrap_description):
			self.scrap_description_array = []
			self._number_fields_to_scrap += 1
		if(self._scrap_manufacturer):
			self.scrap_manufacturer_array = []
			self._number_fields_to_scrap += 1
		if(self._scrap_datasheet):
			self.scrap_datasheet_array = []
			# self._number_fields_to_scrap += 1	 # not a normal table field
		if(self._scrap_digikey_page):
			self.scrap_digikey_page_array = []


	#ADD NEW SCRAPPER MODULES IN THIS FUNCTION
	def scrape_for_page(self):
		print('Waiting for page to load...', end='')
		self._wait_until_load()
		print('Loaded!\nWaiting for divs to load...', end='')
		#wait until 200+ divs are found
		all_divs = []
		while(len(all_divs) < 200):
			all_divs = self.driver.find_elements_by_tag_name('div')
			time.sleep(0.4)
		time.sleep(0.4) #400ms delay for good measure
		all_divs = self.driver.find_elements_by_tag_name('div') #refreshing divs
		print('Loaded!')
		print('Scrapping! Div ')

		fields_scrapped = 0
		for i in range(220,len(all_divs)): #this should ideally start from 0, but this is just a bit more optimized for my purposes
			print('{} / {}       '.format(str(i), str(len(all_divs)))) #this the the current DIV scanning

			#============================================
			#ADD ALL THE DIFFERENT SCRAPPER MODULES HERE
			#============================================

			#description
			if(self._scrap_description):
				if(all_divs[i].text == 'Description'):
					self.scrap_description_array.append(all_divs[i + 1].text)
					fields_scrapped += 1
					print('Scrapped Description!')
			#manufacturer
			if(self._scrap_manufacturer):
				if(all_divs[i].text == 'Manufacturer'):
					self.scrap_manufacturer_array.append(all_divs[i + 1].text)
					fields_scrapped += 1
					print('Scrapped Manufacturer!')
			#manufacturer part number
			if(self._scrap_manufacturer_part_number):
				if(all_divs[i].text == 'Manufacturer Product Number'):
					self.scrap_manufacturer_part_number_array.append(all_divs[i + 1].text)
					fields_scrapped += 1
					print('Scrapped Manufacturer Product Number!')

			#============================================
			#END OF SCRAPPER MODULES
			#============================================

			#will exit when all enabled module info pieces are found
			if(self._number_fields_to_scrap == fields_scrapped):
				break
		
		#datasheet
		if(self._scrap_datasheet):
			self.scrap_datasheet_array.append(self.driver.find_elements_by_class_name('print-hide')[1].get_attribute('href'))
			print('Scrapped Part Datasheet!')
			print(self.scrap_datasheet_array[-1])
		
		#digikey details page
		if(self._scrap_digikey_page):
			self.scrap_digikey_page_array.append(self.driver.current_url)

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
			
			if(self._scrap_datasheet):
				self.data['Data Sheets'] = self.scrap_datasheet_array
			
			if(self._scrap_digikey_page):
				self.data['DigiKey Details Page'] = self.scrap_digikey_page_array

			self.data.to_csv(file_name)
		except:
			code.interact(local=locals())
	
	def _wait_until_load(self):
		loaded = ''
		while(loaded != 'complete'):
			loaded = self.driver.execute_script('return document.readyState')
			time.sleep(0.5)
		time.sleep(0.5)