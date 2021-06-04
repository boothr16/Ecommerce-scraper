import requests
import random
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from time import sleep
from datetime import datetime

class ProductFinder:

	def __init__(self):
		self.product = ''

	def SetProduct(self):
		self.product = input('Enter an item to search for: ')
		self.product.replace(' ', '+')

	def GetHTML(self, URL: str) -> BS:
		HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
		'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '\
		'Safari/537.36'} # bypass
		page = requests.get(URL, headers=HEADERS) # ping webpage
		return BS(page.text, 'lxml') # parse HTML structure

	def CheckBB(self):
		URL = 'https://www.bestbuy.com/site/searchpage.jsp?st=' + self.product \
		+ '&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys'
		soup = self.GetHTML(URL)
		items = soup.find_all('li', class_ = 'sku-item') # returns LIST of items on first page
		
		print('\nITEMS IN STOCK AT BEST BUY')
		for item in items:
			# item_status == NULL if item is out of stock
			item_status = item.find('button', class_ = 'btn btn-primary btn-sm btn-block btn-leading-ficon add-to-cart-button')
			if item_status: # if item is in stock
				item_name = item.find('h4', class_ = 'sku-header').a.text # scrape name
				item_link = 'www.bestbuy.com' + item.find('h4', class_ = 'sku-header').a['href'] # scrape link
				print(f'Item name: {item_name}')
				print(f'Item link: {item_link}')
				print('')

	def CheckNewegg(self):
		URL = 'https://www.newegg.com/p/pl?d=' + self.product + '&N=4131'
		soup = self.GetHTML(URL)
		items = soup.find_all('div', class_ = 'item-container')
		
		print('\nITEMS IN STOCK AT NEWEGG')
		for item in items:
			item_status = item.find('p', class_ = 'item-promo')
			if item_status: # if item_status exists, it holds deal info or OOS info
				if item_status.text == 'OUT OF STOCK':
					continue # do not list in output
			item_name = item.find('a', class_ = 'item-title').text
			item_link = item.find('a', class_ = 'item-title')['href'].replace(' ', '%20')
			print(f'Item name: {item_name}')
			print(f'Item link: {item_link}')
			print('')

	def ScrapePages(self):
		WAIT_TIME_MINUTES = 0.01
		random.seed(datetime.now())
		while True:
			print('Importing Product Data...')
			self.CheckBB()
			self.CheckNewegg()
			print('Import complete.')
			print(f'Waiting {WAIT_TIME_MINUTES} minutes for next import...')
			sleep((WAIT_TIME_MINUTES * 60) + random.uniform(1,3))